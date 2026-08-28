import crypto from "node:crypto";
import fs from "node:fs";

export const FROZEN = Object.freeze({
  productionCommit: "1666481409f4c0d63d66e84659f6b6145d8d25d0",
  inventoryRows: 30308,
  inventoryRawSha256: "fceec52bdc2888542024f059c842a85230d8ecb396992be43b1bf8310aef5ea3",
  inventoryCanonicalSha256: "bf9153e83aba7318741f065d8541ae74783eebc5d4552ec38627a4313456b215",
  inventorySchemaSha256: "483b4bc93b8c3816dc6b29c58e5e68dd931521c93dbcb25423c08ac99233a0ac",
  translationInputsSha256: "051423b82b6594b42d9777f2e9f487e49014e7a82401187bd09c14d9d181c4da",
  hanCharacters: 722375,
  minimumAdjacentLineHan: 20,
  minimumBigramFrequency: 2,
  frequentBigramThreshold: 5,
  minimumPmi: 4,
  knownCalibrationRevision: "2bcc427d50b01aadbb1229339812de295cf389975dca23cb16950d6a9e998ba2"
});

export const sha256Bytes = value => crypto.createHash("sha256").update(value).digest("hex");
export const sha256File = file => sha256Bytes(fs.readFileSync(file));
export const countNewlines = value => (value.match(/\n/gu) ?? []).length;
const hanCount = value => (value.match(/\p{Script=Han}/gu) ?? []).length;
const openingQuotes = new Set(["“", "「", "『", "《", "〈"]);
const closingQuotes = new Set(["”", "」", "』", "》", "〉"]);

export function readInventory(file) {
  const raw = fs.readFileSync(file);
  const rows = raw.toString("utf8").trimEnd().split("\n").filter(Boolean).map((line, index) => {
    try {
      return JSON.parse(line);
    } catch (error) {
      throw new Error(`invalid inventory JSON at line ${index + 1}: ${error.message}`);
    }
  });
  return {
    rows,
    raw_sha256: sha256Bytes(raw),
    canonical_sha256: sha256Bytes(JSON.stringify(rows))
  };
}

export function buildHanStatistics(rows) {
  const characterFrequency = new Map();
  const bigramFrequency = new Map();
  let hanCharacters = 0;
  for (const row of rows) {
    for (const run of row.target.match(/\p{Script=Han}+/gu) ?? []) {
      const characters = [...run];
      for (const character of characters) {
        characterFrequency.set(character, (characterFrequency.get(character) ?? 0) + 1);
        hanCharacters += 1;
      }
      for (let index = 0; index + 1 < characters.length; index += 1) {
        const bigram = `${characters[index]}${characters[index + 1]}`;
        bigramFrequency.set(bigram, (bigramFrequency.get(bigram) ?? 0) + 1);
      }
    }
  }
  return {hanCharacters, characterFrequency, bigramFrequency};
}

export function pmiFor(stats, left, right) {
  const frequency = stats.bigramFrequency.get(`${left}${right}`) ?? 0;
  const leftFrequency = stats.characterFrequency.get(left) ?? 0;
  const rightFrequency = stats.characterFrequency.get(right) ?? 0;
  if (!frequency || !leftFrequency || !rightFrequency || !stats.hanCharacters) return Number.NEGATIVE_INFINITY;
  return Math.log2((frequency * stats.hanCharacters) / (leftFrequency * rightFrequency));
}

function quotedTwoHanToken(leftLine, rightLine) {
  const leftCharacters = [...leftLine];
  const rightCharacters = [...rightLine];
  if (leftCharacters.length < 2 || rightCharacters.length < 2) return false;
  return openingQuotes.has(leftCharacters.at(-2)) && closingQuotes.has(rightCharacters[1]);
}

export function scanRows(rows, stats = buildHanStatistics(rows)) {
  const counters = {
    raw_han_lf_han_boundaries: 0,
    raw_revisions: new Set(),
    indented_boundaries: 0,
    no_target_newline_excess: 0,
    short_adjacent_lines: 0,
    below_lexical_threshold: 0
  };
  const candidates = [];
  for (const row of rows) {
    if (countNewlines(row.source) !== row.structure?.newlines?.source) throw new Error(`${row.revision_id}: source newline metadata drift`);
    if (countNewlines(row.target) !== row.structure?.newlines?.target) throw new Error(`${row.revision_id}: target newline metadata drift`);
    const targetNewlineExcess = row.structure.newlines.target - row.structure.newlines.source;
    const lines = row.target.split("\n");
    for (let lineIndex = 0; lineIndex + 1 < lines.length; lineIndex += 1) {
      const leftMatch = lines[lineIndex].match(/(?<left>\p{Script=Han})$/u);
      const rightMatch = lines[lineIndex + 1].match(/^(?<indent>[ \t]*)(?<right>\p{Script=Han})/u);
      if (!leftMatch || !rightMatch) continue;
      counters.raw_han_lf_han_boundaries += 1;
      counters.raw_revisions.add(row.revision_id);
      const indent = rightMatch.groups.indent.length;
      const left = leftMatch.groups.left;
      const right = rightMatch.groups.right;
      const bigram = `${left}${right}`;
      const bigramFrequency = stats.bigramFrequency.get(bigram) ?? 0;
      const pmi = pmiFor(stats, left, right);
      const leftLineHan = hanCount(lines[lineIndex]);
      const rightLineHan = hanCount(lines[lineIndex + 1]);
      if (indent !== 0) counters.indented_boundaries += 1;
      if (targetNewlineExcess <= 0) counters.no_target_newline_excess += 1;
      if (Math.max(leftLineHan, rightLineHan) < FROZEN.minimumAdjacentLineHan) counters.short_adjacent_lines += 1;
      if (bigramFrequency < FROZEN.minimumBigramFrequency || pmi < FROZEN.minimumPmi) counters.below_lexical_threshold += 1;
      if (
        indent !== 0 ||
        targetNewlineExcess <= 0 ||
        Math.max(leftLineHan, rightLineHan) < FROZEN.minimumAdjacentLineHan ||
        bigramFrequency < FROZEN.minimumBigramFrequency ||
        pmi < FROZEN.minimumPmi
      ) continue;
      const quoted = quotedTwoHanToken(lines[lineIndex], lines[lineIndex + 1]);
      const tier = quoted ? "Q_QUOTED_TWO_HAN_TOKEN" : bigramFrequency >= FROZEN.frequentBigramThreshold ? "A_FREQUENT_BIGRAM" : "B_LOW_SUPPORT_BIGRAM";
      candidates.push({
        tier,
        revision_id: row.revision_id,
        revision_uid: row.revision_uid,
        component: row.component,
        section: row.section,
        source_tag: row.source_tag,
        profile: row.profile,
        risk_flags: row.risk_flags,
        occurrences: row.occurrences,
        boundary: {line_ordinal_zero_based: lineIndex, bigram, rendered: `${left}\\n${right}`},
        lexical_support: {bigram_frequency: bigramFrequency, pmi, han_character_count: stats.hanCharacters},
        structural_support: {
          source_newlines: row.structure.newlines.source,
          target_newlines: row.structure.newlines.target,
          target_newline_excess: targetNewlineExcess,
          left_line_han_characters: leftLineHan,
          right_line_han_characters: rightLineHan,
          quoted_two_han_token: quoted
        },
        target_excerpt: {left_line: lines[lineIndex], right_line: lines[lineIndex + 1]},
        source_sha256: sha256Bytes(row.source),
        target_sha256: sha256Bytes(row.target),
        status: "CANDIDATE_NOT_GROUND_TRUTH"
      });
    }
  }
  const tierOrder = new Map([["Q_QUOTED_TWO_HAN_TOKEN", 0], ["A_FREQUENT_BIGRAM", 1], ["B_LOW_SUPPORT_BIGRAM", 2]]);
  candidates.sort((left, right) => tierOrder.get(left.tier) - tierOrder.get(right.tier) || left.revision_id.localeCompare(right.revision_id) || left.boundary.line_ordinal_zero_based - right.boundary.line_ordinal_zero_based);
  return {
    candidates: candidates.map((candidate, index) => ({candidate_id: `LB${String(index + 1).padStart(3, "0")}`, ...candidate})),
    counts: {
      raw_han_lf_han_boundaries: counters.raw_han_lf_han_boundaries,
      raw_revisions: counters.raw_revisions.size,
      overlapping_filter_failures: {
        indented_boundaries: counters.indented_boundaries,
        no_target_newline_excess: counters.no_target_newline_excess,
        short_adjacent_lines: counters.short_adjacent_lines,
        below_lexical_threshold: counters.below_lexical_threshold
      }
    }
  };
}
