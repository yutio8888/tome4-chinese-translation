// The single append-only ledger. execution/LEDGER.jsonl, one JSON object per line,
// keys exactly {attempt, cell, started_at, finished_at, exit, stdout_sha256, stderr_sha256}
// in that fixed order.
//
//   START  row: finished_at / exit / stdout_sha256 / stderr_sha256 are all null
//   FINISH row: all seven fields are non-null
//
// All run state is DERIVED from these rows. There is no STATE.json in this package and
// no mtime is ever read: deriveState() is the only view of what has been run.
import fs from 'node:fs';
import path from 'node:path';
import {sha256,parseNoDuplicate,walk,hex64} from './lib.mjs';
import {envelopeExtractable} from './parser.mjs';
export const LEDGER_PATH='execution/LEDGER.jsonl';
export const ROW_KEYS=['attempt','cell','started_at','finished_at','exit','stdout_sha256','stderr_sha256'];
// V4 has no retries: every qualification and run cell has exactly one possible attempt.
export const MAX_ATTEMPTS=1;
// C15: the two qualification processes are journaled in THIS ledger, under these cell ids,
// before they are spawned. Every process counter in the package (preflight, runner budget
// arithmetic, post-run) is therefore derived from ledger rows and never from a constant in
// EVIDENCE.json. `qualification-models-list` is the one non-inference process (SPEC 6).
export const QUALIFICATION_CELLS=['qualification-models-list','qualification-synthetic'];
export const NON_INFERENCE_CELLS=['qualification-models-list'];
export const isQualificationCell=cell=>QUALIFICATION_CELLS.includes(cell);
// SPEC 6: exactly 4 agy processes are authorized for the whole pilot, qualification included.
export const PILOT_AGY_PROCESS_CEILING=4;
export const stem=(cell,attempt)=>`${cell}-attempt-${attempt}`;
// Capture paths remain a pure function of (cell, attempt), preserving the append-only evidence
// shape even though v4 permits only attempt 1.
export const capturePaths=(cell,attempt)=>{const dir=isQualificationCell(cell)?'qualification/captures':'execution/captures';return{stdout:`${dir}/${stem(cell,attempt)}.stdout.bin`,stderr:`${dir}/${stem(cell,attempt)}.stderr.bin`}};
export const ledgerLine=row=>`${JSON.stringify(Object.fromEntries(ROW_KEYS.map(k=>[k,row[k]??null])))}\n`;
export const isoNow=()=>new Date().toISOString();
const isIso=x=>typeof x==='string'&&/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/u.test(x);

// C13: NO_RUN is reported only when execution/ is entirely empty (absent, or zero files).
export function executionEmpty(root){
  const dir=path.join(root,'execution');
  if(!fs.existsSync(dir))return true;
  return walk(dir).length===0;
}
export function readRows(root){
  const p=path.join(root,LEDGER_PATH);
  if(!fs.existsSync(p))return{rows:[],errors:[]};
  const buf=fs.readFileSync(p),text=buf.toString('utf8'),errors=[],rows=[];
  if(text.length&&!text.endsWith('\n'))errors.push('LEDGER_TRAILING_PARTIAL_LINE');
  const lines=text.length?text.slice(0,-1).split('\n'):[];
  lines.forEach((line,i)=>{
    let row;try{row=parseNoDuplicate(line,`LEDGER_LINE_${i+1}`)}catch(e){errors.push(e.message);return}
    const keys=Object.keys(row);
    if(JSON.stringify(keys)!==JSON.stringify(ROW_KEYS)){errors.push(`LEDGER_ROW_KEYS:${i+1}`);return}
    if(!Number.isInteger(row.attempt)||row.attempt<1||row.attempt>MAX_ATTEMPTS)errors.push(`LEDGER_ATTEMPT_RANGE:${i+1}`);
    if(typeof row.cell!=='string'||!row.cell)errors.push(`LEDGER_CELL:${i+1}`);
    if(!isIso(row.started_at))errors.push(`LEDGER_STARTED_AT:${i+1}`);
    const finished=row.finished_at!==null;
    if(finished&&(!isIso(row.finished_at)||!Number.isInteger(row.exit)||!hex64(row.stdout_sha256)||!hex64(row.stderr_sha256)))errors.push(`LEDGER_FINISH_ROW:${i+1}`);
    if(!finished&&(row.exit!==null||row.stdout_sha256!==null||row.stderr_sha256!==null))errors.push(`LEDGER_START_ROW:${i+1}`);
    if(ledgerLine(row)!==`${line}\n`)errors.push(`LEDGER_NONCANONICAL_LINE:${i+1}`);
    rows.push(row);
  });
  return{rows,errors};
}
export function appendRow(root,row){
  const line=ledgerLine(row),p=path.join(root,LEDGER_PATH);
  fs.mkdirSync(path.dirname(p),{recursive:true});
  fs.appendFileSync(p,line);
  return sha256(line);
}
export const startRow=(cell,attempt,started_at=isoNow())=>({attempt,cell,started_at,finished_at:null,exit:null,stdout_sha256:null,stderr_sha256:null});
export const finishRow=(start,{exit,stdout_sha256,stderr_sha256,finished_at=isoNow()})=>({attempt:start.attempt,cell:start.cell,started_at:start.started_at,finished_at,exit,stdout_sha256,stderr_sha256});

// Failure classification is retained in the derived view for diagnostics, but v4 never replays
// a failed cell: MAX_ATTEMPTS=1 makes every first attempt terminal. The capture is consulted only
// when it exists AND still hashes to the value journaled in the FINISH row; an absent or
// hash-drifted capture is left as FINISHED_SUCCESS so deriveRaw / reconstruct report the capture
// fault instead of masking it as a parse failure. The non-inference `models` process emits no
// envelope and is classified by exit status alone.
function finishedState(root,row){
  if(row.exit!==0)return'FINISHED_RETRYABLE';
  if(NON_INFERENCE_CELLS.includes(row.cell))return'FINISHED_SUCCESS';
  const p=path.join(root,capturePaths(row.cell,row.attempt).stdout);
  if(!fs.existsSync(p))return'FINISHED_SUCCESS';
  const bytes=fs.readFileSync(p);
  if(sha256(bytes)!==row.stdout_sha256)return'FINISHED_SUCCESS';
  return envelopeExtractable(bytes)?'FINISHED_SUCCESS':'FINISHED_RETRYABLE';
}
// C08/C09: the whole runner view, derived from ledger rows only.
export function deriveState(root){
  const {rows,errors}=readRows(root),cells={};
  for(const row of rows){
    const c=cells[row.cell]??=({attempts:{},order:[]});
    const a=c.attempts[row.attempt];
    if(row.finished_at===null){
      if(a)errors.push(`LEDGER_DUPLICATE_START:${row.cell}:${row.attempt}`);
      else{c.attempts[row.attempt]={...row,state:'STARTED_NO_FINISH'};c.order.push(row.attempt)}
    }else{
      if(!a){errors.push(`LEDGER_FINISH_WITHOUT_START:${row.cell}:${row.attempt}`);continue}
      if(a.state!=='STARTED_NO_FINISH'){errors.push(`LEDGER_DUPLICATE_FINISH:${row.cell}:${row.attempt}`);continue}
      if(a.started_at!==row.started_at)errors.push(`LEDGER_START_TIME_MISMATCH:${row.cell}:${row.attempt}`);
      c.attempts[row.attempt]={...row,state:finishedState(root,row)};
    }
  }
  const out={};
  for(const [cell,c] of Object.entries(cells)){
    const attempts=c.order.map(n=>c.attempts[n]);
    // C09: v4 permits only the single attempt sequence [1].
    if(JSON.stringify(c.order)!=='[1]')errors.push(`ATTEMPT_SEQUENCE:${cell}:${JSON.stringify(c.order)}`);
    const ambiguous=attempts.some(a=>a.state==='STARTED_NO_FINISH');
    const success=attempts.find(a=>a.state==='FINISHED_SUCCESS')??null;
    let next=null,blocked=null;
    if(ambiguous){blocked='AMBIGUOUS_STARTED_BLOCKS_REPLAY'}
    else if(success){blocked='ALREADY_SUCCEEDED'}
    else if(c.order.length>=MAX_ATTEMPTS){blocked='ATTEMPT_RULE_EXHAUSTED'}
    else blocked='ATTEMPT_STATE_UNRECOGNIZED';
    out[cell]={attempts,attempt_numbers:c.order,successful_attempt:success?success.attempt:null,ambiguous,next_attempt:next,blocked_reason:blocked};
  }
  // Every START row is one spawned agy process (SPEC 6 counting: exit status is irrelevant).
  const starts=rows.filter(r=>r.finished_at===null);
  return{no_run:executionEmpty(root)&&rows.length===0,rows:rows.length,started_rows:starts.length,finished_rows:rows.filter(r=>r.finished_at!==null).length,agy_processes_spawned:starts.length,inference_calls_made:starts.filter(r=>!NON_INFERENCE_CELLS.includes(r.cell)).length,cells:out,errors};
}
// The only place an attempt number is chosen. In v4 it returns 1 only for a never-seen cell;
// once a first attempt exists it can never return a second attempt.
export function nextAttempt(state,cell){
  const c=state.cells[cell];
  if(!c)return{attempt:1,blocked:null};
  return{attempt:null,blocked:c.blocked_reason??'ATTEMPT_RULE_EXHAUSTED'};
}
