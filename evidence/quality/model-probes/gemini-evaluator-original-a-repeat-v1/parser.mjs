import {exactKeys, parseNoDuplicate} from './lib.mjs';

const claims = new Set(['SUBJECT', 'REFERENT', 'EVENT', 'CONDITION', 'SCOPE', 'DIRECTION', 'POLARITY', 'OWNERSHIP', 'ACTION', 'STATE', 'TIMING', 'OMISSION', 'ADDITION', 'FORMAT', 'OTHER']);

export function extractAgy(stdout) {
  const envelope = parseNoDuplicate(Buffer.from(stdout).toString('utf8'), 'AGY');
  if (!envelope || typeof envelope !== 'object' || Array.isArray(envelope) || envelope.status !== 'SUCCESS') throw Error('AGY_ENVELOPE_STATUS');
  const hasStructured = envelope.structured_output != null, hasResponse = envelope.response != null;
  if (!hasStructured && !hasResponse) throw Error('AGY_CHANNEL_MISSING');
  let output;
  if (hasStructured) {
    if (typeof envelope.structured_output !== 'object' || Array.isArray(envelope.structured_output)) throw Error('AGY_STRUCTURED_TYPE');
    output = envelope.structured_output;
    if (hasResponse) {
      if (typeof envelope.response !== 'string') throw Error('AGY_RESPONSE_TYPE');
      const secondary = parseNoDuplicate(envelope.response, 'AGY_RESPONSE');
      if (JSON.stringify(secondary?.items) !== JSON.stringify(output?.items)) throw Error('AGY_CHANNEL_MISMATCH');
    }
  } else {
    if (typeof envelope.response !== 'string') throw Error('AGY_RESPONSE_TYPE');
    output = parseNoDuplicate(envelope.response, 'AGY_RESPONSE');
  }
  return output;
}

export function parseOutput(output, input) {
  const errors = [], ids = input.items.map(x => x.item_id);
  if (!exactKeys(output, ['items']) || !Array.isArray(output.items) || output.items.length !== 16) return {valid: false, errors: ['OUTPUT_ITEMS'], normalized: null};
  const normalized = [];
  output.items.forEach((item, i) => {
    if (!exactKeys(item, ['item_id', 'candidates']) || item.item_id !== ids[i] || !Array.isArray(item.candidates) || item.candidates.length > 4) {
      errors.push(`ITEM:${i}`); return;
    }
    const row = {item_id: item.item_id, candidates: []};
    item.candidates.forEach((candidate, j) => {
      if (!exactKeys(candidate, ['verdict', 'claim_type', 'target_span', 'correction', 'evidence']) || !['FINDING', 'UNCERTAIN'].includes(candidate.verdict) || !claims.has(candidate.claim_type)) {
        errors.push(`CANDIDATE:${i}:${j}`); return;
      }
      for (const key of ['target_span', 'correction', 'evidence']) if (typeof candidate[key] !== 'string' || candidate[key].length < 1 || candidate[key].length > 500) errors.push(`FIELD:${i}:${j}:${key}`);
      row.candidates.push({...candidate});
    });
    normalized.push(row);
  });
  return {valid: errors.length === 0, errors, normalized: errors.length ? null : {items: normalized}};
}

export function parseCapture(stdout, input) {
  try { return parseOutput(extractAgy(stdout), input); }
  catch (error) { return {valid: false, errors: [error.message], normalized: null}; }
}
