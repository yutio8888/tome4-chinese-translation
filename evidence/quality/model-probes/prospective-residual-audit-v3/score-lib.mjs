function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function gcd(a, b) {
  let x = a < 0n ? -a : a;
  let y = b < 0n ? -b : b;
  while (y !== 0n) [x, y] = [y, x % y];
  return x;
}

function rational(numerator, denominator = 1n) {
  let n = BigInt(numerator);
  let d = BigInt(denominator);
  assert(d !== 0n, "zero rational denominator");
  if (d < 0n) [n, d] = [-n, -d];
  const divisor = gcd(n, d);
  return {n: n / divisor, d: d / divisor};
}

function add(a, b) {
  return rational(a.n * b.d + b.n * a.d, a.d * b.d);
}

function divide(a, b) {
  assert(b.n !== 0n, "division by zero rational");
  return rational(a.n * b.d, a.d * b.n);
}

function multiply(a, b) {
  return rational(a.n * b.n, a.d * b.d);
}

function sum(values) {
  return values.reduce((total, value) => add(total, value), rational(0n));
}

function serialize(value) {
  return {
    numerator: value.n.toString(),
    denominator: value.d.toString(),
    fraction: `${value.n}/${value.d}`,
    decimal: Number(value.n) / Number(value.d)
  };
}

function ratioOrNull(numerator, denominator) {
  return denominator.n === 0n ? null : serialize(divide(numerator, denominator));
}

function itemWeight(referenceItem) {
  const exact = referenceItem.design_weight_exact;
  assert(exact && /^-?\d+$/.test(exact.numerator) && /^\d+$/.test(exact.denominator), `${referenceItem.audit_id}: exact weight missing`);
  return rational(BigInt(exact.numerator), BigInt(exact.denominator));
}

export function validateResponse(response, orderedIds) {
  const errors = [];
  if (!response || typeof response !== "object" || Array.isArray(response)) return ["response is not an object"];
  if (JSON.stringify(Object.keys(response).sort()) !== JSON.stringify(["revisions"])) errors.push("top-level keys are not exactly revisions");
  if (!Array.isArray(response.revisions)) return [...errors, "revisions is not an array"];
  if (response.revisions.length !== orderedIds.length) errors.push(`expected ${orderedIds.length} revisions, got ${response.revisions.length}`);
  for (let index = 0; index < response.revisions.length; index += 1) {
    const revision = response.revisions[index];
    if (!revision || typeof revision !== "object" || Array.isArray(revision)) {
      errors.push(`revision ${index} is not an object`);
      continue;
    }
    if (JSON.stringify(Object.keys(revision).sort()) !== JSON.stringify(["evidence", "observation", "revision_id", "verdict"])) errors.push(`revision ${index} has unexpected keys`);
    if (revision.revision_id !== orderedIds[index]) errors.push(`revision ${index} expected ${orderedIds[index]}, got ${revision.revision_id}`);
    if (!["NO_DEFECT", "DEFECT"].includes(revision.verdict)) errors.push(`revision ${index} invalid verdict`);
    if (typeof revision.observation !== "string" || !revision.observation.trim()) errors.push(`revision ${index} invalid observation`);
    if (revision.verdict === "NO_DEFECT" && revision.observation !== "NO_DEFECT") errors.push(`revision ${index} NO_DEFECT observation must be exactly NO_DEFECT`);
    if (revision.verdict === "DEFECT" && revision.observation === "NO_DEFECT") errors.push(`revision ${index} DEFECT observation must not be NO_DEFECT`);
    if (typeof revision.evidence !== "string" || !revision.evidence.trim()) errors.push(`revision ${index} invalid evidence`);
  }
  return errors;
}

export function matchAtom(revision, atom) {
  if (revision.verdict !== atom.matcher.required_verdict) return false;
  const observation = revision.observation.normalize("NFKC").toLowerCase();
  const evidence = revision.evidence.normalize("NFKC").toLowerCase();
  const normalizedTerms = values => values.map(value => value.normalize("NFKC").toLowerCase());
  const relationTerms = normalizedTerms(atom.matcher.observation_required_any_relation_term);
  const scopeAnchors = normalizedTerms(atom.matcher.observation_scope_required_all_anchors);
  const formatTerms = normalizedTerms(atom.matcher.observation_required_any_format_term);
  const observationClauses = observation.split(/[。；;!?！？\n]/u);
  const scopedFormatMatch = observationClauses.some(clause =>
    formatTerms.some(term => clause.includes(term)) &&
    (relationTerms.some(term => clause.includes(term)) || scopeAnchors.every(term => clause.includes(term)))
  );
  const negated = normalizedTerms(atom.matcher.observation_forbidden_negation_terms).some(term => observation.includes(term));
  const negatedByPattern = (atom.matcher.observation_forbidden_negation_regexes ?? []).some(pattern => new RegExp(pattern, "u").test(observation));
  const exactEvidenceMatch = new RegExp(atom.matcher.evidence_required_exact_split_regex, "u").test(evidence);
  const evidenceAnchorsMatch = normalizedTerms(atom.matcher.evidence_descriptive_required_all_anchors).every(term => evidence.includes(term));
  const evidenceRelationMatch = normalizedTerms(atom.matcher.evidence_descriptive_required_any_relation_term).some(term => evidence.includes(term));
  const evidenceNegated = normalizedTerms(atom.matcher.evidence_forbidden_negation_terms).some(term => evidence.includes(term));
  const evidenceNegatedByPattern = (atom.matcher.evidence_forbidden_negation_regexes ?? []).some(pattern => new RegExp(pattern, "u").test(evidence));
  const descriptiveEvidenceMatch = evidenceAnchorsMatch && evidenceRelationMatch;
  return scopedFormatMatch && !negated && !negatedByPattern && !evidenceNegated && !evidenceNegatedByPattern && (exactEvidenceMatch || descriptiveEvidenceMatch);
}

export function validateScoringContract({holdout, reference, atomMap}) {
  const errors = [];
  const check = (condition, message) => { if (!condition) errors.push(message); };
  const expectedIds = Array.from({length: 40}, (_, index) => `R${String(index + 1).padStart(3, "0")}`);
  const holdoutIds = Array.isArray(holdout?.items) ? holdout.items.map(item => item.revision_id) : [];
  const referenceIds = Array.isArray(reference?.items) ? reference.items.map(item => item.audit_id) : [];
  check(holdout?.item_count === 40 && holdoutIds.length === 40, "holdout must contain exactly 40 items");
  check(JSON.stringify(holdoutIds) === JSON.stringify(expectedIds), "holdout IDs/order mismatch");
  check(new Set(holdoutIds).size === holdoutIds.length, "holdout IDs are not unique");
  check(referenceIds.length === 40, "reference must contain exactly 40 items");
  check(JSON.stringify(referenceIds) === JSON.stringify(expectedIds), "reference IDs/order mismatch");
  check(new Set(referenceIds).size === referenceIds.length, "reference IDs are not unique");
  for (const item of reference?.items ?? []) {
    check(item.scorable === true, `${item.audit_id}: scorable must be true`);
    check(item.y === 0 || item.y === 1, `${item.audit_id}: y must be 0 or 1`);
    const exact = item.design_weight_exact;
    check(exact && /^\d+$/u.test(exact.numerator) && /^\d+$/u.test(exact.denominator) && BigInt(exact.numerator) > 0n && BigInt(exact.denominator) > 0n, `${item.audit_id}: weight must be a positive rational`);
  }
  const atoms = Array.isArray(atomMap?.atoms) ? atomMap.atoms : [];
  const atomIds = atoms.map(atom => atom.atom_id);
  const atomAuditIds = atoms.map(atom => atom.audit_id);
  check(new Set(atomIds).size === atomIds.length, "atom IDs are not unique");
  check(new Set(atomAuditIds).size === atomAuditIds.length, "positive items must have exactly one atom");
  const positiveIds = (reference?.items ?? []).filter(item => item.y === 1).map(item => item.audit_id).sort();
  check(JSON.stringify([...atomAuditIds].sort()) === JSON.stringify(positiveIds), "positive reference and atom coverage mismatch");
  const referenceById = new Map((reference?.items ?? []).map(item => [item.audit_id, item]));
  for (const atom of atoms) {
    check(referenceById.get(atom.audit_id)?.y === 1, `${atom.atom_id}: atom must point to a positive reference item`);
    check(atom.matcher?.required_verdict === "DEFECT", `${atom.atom_id}: matcher verdict must be DEFECT`);
    check(Array.isArray(atom.matcher?.observation_required_any_relation_term) && atom.matcher.observation_required_any_relation_term.length > 0, `${atom.atom_id}: observation relation terms missing`);
    check(Array.isArray(atom.matcher?.observation_scope_required_all_anchors) && atom.matcher.observation_scope_required_all_anchors.length > 0, `${atom.atom_id}: observation scope anchors missing`);
    check(Array.isArray(atom.matcher?.observation_required_any_format_term) && atom.matcher.observation_required_any_format_term.length > 0, `${atom.atom_id}: observation format terms missing`);
    check(typeof atom.matcher?.evidence_required_exact_split_regex === "string", `${atom.atom_id}: evidence split regex missing`);
    check(Array.isArray(atom.matcher?.evidence_descriptive_required_all_anchors) && atom.matcher.evidence_descriptive_required_all_anchors.length > 0, `${atom.atom_id}: evidence anchors missing`);
    check(Array.isArray(atom.matcher?.evidence_descriptive_required_any_relation_term) && atom.matcher.evidence_descriptive_required_any_relation_term.length > 0, `${atom.atom_id}: evidence relation terms missing`);
    check(Array.isArray(atom.matcher?.evidence_forbidden_negation_terms), `${atom.atom_id}: evidence negation terms missing`);
    check(Array.isArray(atom.matcher?.evidence_forbidden_negation_regexes), `${atom.atom_id}: evidence negation regexes missing`);
  }
  return errors;
}

export function scoreResponse({response, holdout, reference, atomMap}) {
  const contractErrors = validateScoringContract({holdout, reference, atomMap});
  assert(contractErrors.length === 0, `invalid hidden scoring contract: ${contractErrors.join("; ")}`);
  const orderedIds = holdout.items.map(item => item.revision_id);
  const validationErrors = validateResponse(response, orderedIds);
  if (validationErrors.length > 0) return {valid: false, validation_errors: validationErrors, metrics: null};
  assert(reference.items.length === orderedIds.length, "reference coverage mismatch");
  assert(JSON.stringify(reference.items.map(item => item.audit_id)) === JSON.stringify(orderedIds), "reference order mismatch");
  const responseById = new Map(response.revisions.map(item => [item.revision_id, item]));
  const atomMatches = atomMap.atoms.map(atom => ({
    atom_id: atom.atom_id,
    audit_id: atom.audit_id,
    matched: matchAtom(responseById.get(atom.audit_id), atom)
  }));
  const matchedAtomIds = atomMatches.filter(item => item.matched).map(item => item.atom_id);
  const candidateIds = response.revisions.filter(item => item.verdict === "DEFECT").map(item => item.revision_id);
  const offTargetPositiveIds = reference.items.filter(item => item.y === 1 && responseById.get(item.audit_id).verdict === "DEFECT" && !atomMatches.some(atom => atom.audit_id === item.audit_id && atom.matched)).map(item => item.audit_id);
  const falsePositiveIds = reference.items.filter(item => item.y === 0 && responseById.get(item.audit_id).verdict === "DEFECT").map(item => item.audit_id);
  const weights = new Map(reference.items.map(item => [item.audit_id, itemWeight(item)]));
  const cellWeight = (y, prediction) => sum(reference.items.filter(item => item.scorable && item.y === y && (responseById.get(item.audit_id).verdict === "DEFECT" ? 1 : 0) === prediction).map(item => weights.get(item.audit_id)));
  const tp = cellWeight(1, 1);
  const fn = cellWeight(1, 0);
  const fp = cellWeight(0, 1);
  const tn = cellWeight(0, 0);
  const positive = add(tp, fn);
  const negative = add(tn, fp);
  const predictedPositive = add(tp, fp);
  const total = add(positive, negative);
  const recall = positive.n === 0n ? null : divide(tp, positive);
  const specificity = negative.n === 0n ? null : divide(tn, negative);
  const precision = predictedPositive.n === 0n ? null : divide(tp, predictedPositive);
  const f1Denominator = add(add(multiply(rational(2n), tp), fp), fn);
  const f1 = f1Denominator.n === 0n ? null : divide(multiply(rational(2n), tp), f1Denominator);
  const balancedAccuracy = recall === null || specificity === null ? null : divide(add(recall, specificity), rational(2n));
  const candidateMass = sum(candidateIds.map(id => weights.get(id)));
  const falsePositiveMass = sum(falsePositiveIds.map(id => weights.get(id)));
  const matchedPositiveIds = [...new Set(atomMatches.filter(atom => atom.matched).map(atom => atom.audit_id))];
  const matchedAtomMass = sum(matchedPositiveIds.map(id => weights.get(id)));

  return {
    valid: true,
    validation_errors: [],
    metrics: {
      primary_atom_detection: {
        atoms_total: atomMatches.length,
        atoms_detected: matchedAtomIds.length,
        recall: atomMatches.length === 0 ? null : serialize(rational(BigInt(matchedAtomIds.length), BigInt(atomMatches.length))),
        matches: atomMatches,
        off_target_positive_item_ids: offTargetPositiveIds
      },
      candidates: {
        item_count: candidateIds.length,
        item_ids: candidateIds,
        false_positive_item_count: falsePositiveIds.length,
        false_positive_item_ids: falsePositiveIds,
        atom_match_efficiency_unweighted: candidateIds.length === 0 ? null : serialize(rational(BigInt(matchedAtomIds.length), BigInt(candidateIds.length))),
        atom_match_efficiency_weighted: candidateMass.n === 0n ? null : serialize(divide(matchedAtomMass, candidateMass))
      },
      binary_nomination_unweighted: {
        TP: reference.items.filter(item => item.y === 1 && responseById.get(item.audit_id).verdict === "DEFECT").length,
        FN: reference.items.filter(item => item.y === 1 && responseById.get(item.audit_id).verdict === "NO_DEFECT").length,
        FP: falsePositiveIds.length,
        TN: reference.items.filter(item => item.y === 0 && responseById.get(item.audit_id).verdict === "NO_DEFECT").length
      },
      binary_nomination_weighted: {
        confusion: {TP: serialize(tp), FN: serialize(fn), FP: serialize(fp), TN: serialize(tn)},
        recall: recall === null ? null : serialize(recall),
        specificity: specificity === null ? null : serialize(specificity),
        precision: precision === null ? null : serialize(precision),
        f1: f1 === null ? null : serialize(f1),
        balanced_accuracy: balancedAccuracy === null ? null : serialize(balancedAccuracy),
        candidate_mass: serialize(candidateMass),
        candidate_mass_rate: ratioOrNull(candidateMass, total),
        false_positive_mass: serialize(falsePositiveMass),
        false_positive_mass_rate: ratioOrNull(falsePositiveMass, total)
      }
    }
  };
}
