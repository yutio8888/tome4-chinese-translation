const prose = /[.!?。！？]|because|since|therefore|means|indicates|shows|the translation|the source|the target|因为|所以|说明|表示|译文|原文/iu;

export function metrics(normalized, input) {
  const source = new Map(input.items.map(x => [x.item_id, x])), candidates = [];
  for (const row of normalized.items) for (const candidate of row.candidates) {
    const item = source.get(row.item_id);
    const evidenceMember = item.source.includes(candidate.evidence) || item.target.includes(candidate.evidence);
    candidates.push({candidate, item, evidenceMember, targetMember: item.target.includes(candidate.target_span), proseProxy: prose.test(candidate.evidence)});
  }
  const n = candidates.length, evidence = candidates.filter(x => x.evidenceMember).length, target = candidates.filter(x => x.targetMember).length;
  const proseValid = candidates.filter(x => x.evidenceMember && x.proseProxy).length, proseInvalid = candidates.filter(x => !x.evidenceMember && x.proseProxy).length;
  return {
    status: n === 0 ? 'UNINFORMATIVE_ZERO_CANDIDATES' : 'DESCRIPTIVE',
    candidate_count: n,
    evidence_membership_count: evidence,
    evidence_membership_rate: n ? evidence / n : null,
    target_span_membership_count: target,
    target_span_membership_rate: n ? target / n : null,
    evidence_mean_character_length: n ? candidates.reduce((sum, x) => sum + x.candidate.evidence.length, 0) / n : null,
    explanatory_prose_proxy_membership_valid_count: proseValid,
    explanatory_prose_proxy_membership_invalid_count: proseInvalid
  };
}

export function interpret(runRows) {
  if (runRows.length !== 3 || runRows.some(x => !x.process_success || !x.envelope_schema_valid || !x.metrics || x.metrics.candidate_count === 0)) return 'INCOMPLETE_FOR_THREE_RUN_RULE';
  const full = runRows.map(x => x.metrics.evidence_membership_rate === 1);
  if (full.every(Boolean)) return 'NOT_REPRODUCED_STOCHASTICITY_PLAUSIBLE';
  if (full.every(x => !x)) return 'CONSISTENTLY_REPRODUCED';
  return 'RUN_TO_RUN_VARIABILITY';
}
