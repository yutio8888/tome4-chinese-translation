import {exactKeys,parseNoDuplicate,sha256} from './lib.mjs';

const claims = new Set(['SUBJECT','REFERENT','EVENT','CONDITION','SCOPE','DIRECTION','POLARITY','OWNERSHIP','ACTION','STATE','TIMING','OMISSION','ADDITION','FORMAT','OTHER']);

function jsonType(value) {
  if (value === null) return 'null';
  if (Array.isArray(value)) return 'array';
  return typeof value;
}

export function extractAgy(stdout) {
  const envelope = parseNoDuplicate(Buffer.from(stdout).toString('utf8'), 'AGY');
  if (!envelope || typeof envelope !== 'object' || Array.isArray(envelope)) throw Error('AGY_ENVELOPE_OBJECT');
  if (envelope.status !== 'SUCCESS') throw Error('AGY_ENVELOPE_STATUS');
  if (!Object.hasOwn(envelope, 'structured_output')) throw Error('AGY_STRUCTURED_MISSING');
  const payload = envelope.structured_output;
  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) throw Error('AGY_STRUCTURED_TYPE');

  const responsePresent = Object.hasOwn(envelope, 'response');
  const response = responsePresent ? envelope.response : undefined;
  const responseIsString = responsePresent && typeof response === 'string';
  return {
    payload,
    envelope_metadata: {
      authoritative_channel: 'structured_output',
      response_present: responsePresent,
      response_type: responsePresent ? jsonType(response) : null,
      response_utf8_bytes: responseIsString ? Buffer.byteLength(response, 'utf8') : null,
      response_sha256: responseIsString ? sha256(Buffer.from(response, 'utf8')) : null
    }
  };
}

export function parseOutput(output, input, schemaName) {
  const errors = [], ids = input.items.map(x => x.item_id), field = schemaName === 'S2' ? 'evidence_quote' : 'evidence';
  if (!exactKeys(output, ['items']) || !Array.isArray(output.items) || output.items.length !== 16) return {valid:false, errors:['OUTPUT_ITEMS'], normalized:null};
  const rows = [];
  output.items.forEach((item, i) => {
    if (!exactKeys(item, ['item_id','candidates']) || item.item_id !== ids[i] || !Array.isArray(item.candidates) || item.candidates.length > 4) { errors.push(`ITEM:${i}`); return; }
    const row = {item_id:item.item_id, candidates:[]};
    item.candidates.forEach((candidate, j) => {
      if (!exactKeys(candidate, ['verdict','claim_type','target_span','correction',field]) || !['FINDING','UNCERTAIN'].includes(candidate.verdict) || !claims.has(candidate.claim_type)) { errors.push(`CANDIDATE:${i}:${j}`); return; }
      for (const key of ['target_span','correction',field]) if (typeof candidate[key] !== 'string' || candidate[key].length < 1 || candidate[key].length > 500) errors.push(`FIELD:${i}:${j}:${key}`);
      row.candidates.push({verdict:candidate.verdict, claim_type:candidate.claim_type, target_span:candidate.target_span, correction:candidate.correction, evidence:candidate[field], emitted_evidence_field:field, registered_evidence_field:field});
    });
    rows.push(row);
  });
  return {valid:errors.length === 0, errors, normalized:errors.length ? null : {items:rows}};
}

export function parseCapture(stdout, input, schemaName) {
  try {
    const extracted = extractAgy(stdout), parsed = parseOutput(extracted.payload, input, schemaName);
    return {...parsed, envelope_metadata:parsed.valid ? extracted.envelope_metadata : null};
  } catch (error) {
    return {valid:false, errors:[error.message], normalized:null, envelope_metadata:null};
  }
}
