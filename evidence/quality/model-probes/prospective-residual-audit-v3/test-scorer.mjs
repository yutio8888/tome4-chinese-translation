import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {scoreResponse} from "./score-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const holdout = JSON.parse(fs.readFileSync(path.join(here, "PUBLIC-HOLDOUT.json"), "utf8"));
const reference = JSON.parse(fs.readFileSync(path.join(here, "SEALED-REFERENCE.json"), "utf8"));
const atomMap = JSON.parse(fs.readFileSync(path.join(here, "SEALED-ATOM-MAP.json"), "utf8"));
const fixture = JSON.parse(fs.readFileSync(path.join(here, "SCORER-FIXTURE.json"), "utf8"));

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

for (const testCase of fixture.cases) {
  const revisions = holdout.items.map(item => ({
    revision_id: item.revision_id,
    verdict: "NO_DEFECT",
    observation: "NO_DEFECT",
    evidence: "No objective defect is asserted by this synthetic fixture."
  }));
  const byId = new Map(revisions.map(item => [item.revision_id, item]));
  for (const mutation of testCase.mutations) Object.assign(byId.get(mutation.revision_id), mutation);
  if (testCase.structure_mutation === "swap-first-two") [revisions[0], revisions[1]] = [revisions[1], revisions[0]];
  const testReference = structuredClone(reference);
  const testAtomMap = structuredClone(atomMap);
  if (testCase.contract_mutation === "ZERO_FIRST_REFERENCE_WEIGHT") testReference.items[0].design_weight_exact.numerator = "0";
  if (testCase.contract_mutation === "ATOM_POINTS_TO_R001") testAtomMap.atoms[0].audit_id = "R001";
  if (testCase.contract_mutation === "DROP_ALL_ATOMS") testAtomMap.atoms = [];
  let result;
  let threw = false;
  try { result = scoreResponse({response: {revisions}, holdout, reference: testReference, atomMap: testAtomMap}); }
  catch { threw = true; }
  if (testCase.expected.throws) {
    assert(threw, `${testCase.case_id}: expected hidden-contract rejection`);
    continue;
  }
  assert(!threw, `${testCase.case_id}: unexpected throw`);
  assert(result.valid === testCase.expected.valid, `${testCase.case_id}: validity mismatch`);
  if (!result.valid) continue;
  const metrics = result.metrics;
  const confusion = metrics.binary_nomination_unweighted;
  assert(metrics.primary_atom_detection.atoms_detected === testCase.expected.atoms_detected, `${testCase.case_id}: atom detection mismatch`);
  assert(metrics.candidates.item_count === testCase.expected.candidates, `${testCase.case_id}: candidate count mismatch`);
  assert(metrics.primary_atom_detection.off_target_positive_item_ids.length === testCase.expected.off_target, `${testCase.case_id}: off-target count mismatch`);
  assert(metrics.candidates.false_positive_item_count === testCase.expected.false_positives, `${testCase.case_id}: false-positive count mismatch`);
  for (const cell of ["TP", "FN", "FP", "TN"]) assert(confusion[cell] === testCase.expected[cell], `${testCase.case_id}: ${cell} mismatch`);
  const weighted = metrics.binary_nomination_weighted;
  for (const cell of ["TP", "FN", "FP", "TN"]) {
    const expected = testCase.expected[`weighted_${cell}`];
    if (expected !== undefined) assert(weighted.confusion[cell].fraction === expected, `${testCase.case_id}: weighted ${cell} mismatch`);
  }
  if (testCase.expected.candidate_mass_rate !== undefined) assert(weighted.candidate_mass_rate.fraction === testCase.expected.candidate_mass_rate, `${testCase.case_id}: candidate mass rate mismatch`);
}

process.stdout.write(`${JSON.stringify({status: "PASS", fixture_cases: fixture.cases.length}, null, 2)}\n`);
