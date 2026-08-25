# P2 Tome Texts — handoff at the b37 pause (2026-08-25)

Consolidated pickup document. Supersedes
[`p2-tome-texts-handoff-2026-08-23.md`](p2-tome-texts-handoff-2026-08-23.md) as the entry point;
that file remains the per-batch log and is still the place to read *why* a specific batch decided
what it did.

**Status: PAUSED at the b37 boundary on maintainer instruction.** Continuous batch mode is
suspended. Resuming needs an explicit instruction.

Working tree is clean at `bde9a61`. Every batch below reached `DONE_VERIFIED` and passed
`tools/ci-gates.sh` 12/12 including the strict addon build.

## 1. Coverage

| Area | Sections | Pairs | Status |
|---|---|---|---|
| `data/texts/` | 132 | 176 | Complete |
| `data/chats/` | 100 | 1260 | Complete (b6–b35) |
| `data/lore/` | 34 | 582 | 9 done (b36–b37); **25 sections / 492 pairs left** |
| `data/quests/` | 52 | 514 | **Zero coverage — and never scoped into P2** |

### Remaining `data/lore/` sections

`elvala`(17), `fearscape`(5), `fun`(19), `high-peak`(11), `infinite-dungeon`(21), `iron-throne`(21),
`keepsake`(34), `kor-pul`(7), `last-hope`(71), `maze`(6), `misc`(110), `noxious-caldera`(7),
`old-forest`(10), `orc-prides`(37), `rhaloren`(8), `sandworm`(6), `scintillating-caves`(13),
`shertul`(41), `slazish`(7), `spellblaze`(3), `spellhunt`(9), `sunwall`(6), `tannen`(9),
`trollmire`(5), `zigur`(9)

**About 9 more slices.** `misc.lua` (110) and `last-hope.lua` (71) each need their own batch; the
other 311 pairs make roughly 7 at the ~45 pairs/batch this track has settled into.

**Next slice (b38):** `elvala`, `fearscape`, `fun`, `high-peak` — 52 pairs. Both `elvala.lua` and
`high-peak.lua` were cleaned by the Angolwen ruling, so they are ready.

### The `data/quests/` question

514 pairs across 52 sections, no tracked coverage, and the roadmap named only `data/chats/` and
`data/lore/`. It is narrative content of exactly the kind this track exists to review, and quest
files have already proved load-bearing here — `east-portal.lua` held one of the Angolwen variants,
and several b30 and b34 adjudications turned on reading quest code. **Whether it belongs in P2 is an
open maintainer decision**, worth roughly 12 further slices.

## 2. Known gaps

**Five `data/chats/` sections have no tracked workset:** `gates-of-morning-main`, `jewelry-store`,
`last-hope-melinda-father`, `last-hope-weapon-store`, `limmir-valley-moon`. They *were* reviewed —
all sort before `sorcerer-fight.lua`, the b6–b21 completion point, and `limmir-valley-moon` is
recorded as verified-with-no-change at b21. What is missing is the tracked audit anchor, from the
b19–b21 lapse of leaving worksets only in ignored `.ai/`. **A documentation gap, not a review gap.**
Reconstructing those anchors is a separate task and has not been undertaken.

## 3. Settled by maintainer ruling (2026-08-25)

| Term | Decision | Scope | Commit |
|---|---|---|---|
| `Angolwen` | 安格利文 | 10 occurrences / 6 sections | `de44127` |
| `Maj'Eyal` | 马基·埃亚尔 (interpunct) | 55 / 33 sections | `de44127` |
| `Sholtar` | 肖尔塔 | 6 / 3 sections, new row | `bde9a61` |
| `Atamathon` | 巨型傀儡 (was 傀儡之王) | 5 | `bde9a61` |
| `Spellblade` | 法术之刃 (was 魔宗利刃) | 2 | `bde9a61` |

Terminology rows now total **712**.

Nothing is currently awaiting a maintainer decision except the `data/quests/` scope above.

## 4. Per-batch workflow

Unchanged from [`agent-workflow.md`](agent-workflow.md); summarised here so a batch can be started
cold.

1. **Freeze** the workset to tracked `evidence/quality/p2-batches/`. Build from
   `tools/i18n context --component tome --section <s> --json --limit 500`, and **assert the item
   count equals the lexical `t()` count** per section (`contextual_anchor_preflight._allowed_calls`).
   Byte-verify every English key against the pinned commit, escape-aware.
2. **Survey** terminology and corpus consistency for the names in the window. Record findings in
   PLAN as leads, not as instructions to apply blind.
3. **Write** SPEC / PLAN / SCOPE / STATE and adapt the envelope builder. Verify the revision-key
   prefix and `--limit 500` **before** dispatch.
4. **EXECUTOR** dispatch. Verify its claims against the pinned source yourself — do not accept them.
5. **Envelope → `contextual_anchor_preflight.py` → REVIEWER** under `translation_contextual_v1`
   with the contract's exact three-line prompt.
6. **Adjudicate** every finding as `confirmed` or `advisory` with a written ground; fix round for
   the confirmed ones.
7. **Gates**, `ai_state_check.py` → `DONE_VERIFIED`, commit, then update this handoff and memory.

**Terminology batches differ:** they use `code_legacy_v1` / `normal_review` (a *diff* review), not
`translation_contextual_v1`, and they additionally run the three terminology audits. See §6.

## 5. Standing rulings that constrain future batches

- **Per occurrence, not per word.** One English word can carry two relations, and both renderings
  can be correct in the same file. `the Master` is 领主 as a character but 主人 as the minions'
  owner (b32, b37); `a control rod` stays generic while the gated branch uses the item name (b26,
  b27); `inscriptions` is the category 刻印, not its subtype 纹身 (b36).
- **Entity-name rows are the anchor.** When a proper noun splits, find the `entity name` row before
  counting occurrences — it settles the question (b32 Krogar, b34 Briagh and Grand Keeper, b37 the
  Master).
- **A generic indefinite noun does not become an item name** just because the referent is real. Ask
  whether anything *gates* on the item here, not whether it is that item (b32).
- **Split proper names are unified within a batch, never globally** — a global rename is a
  maintainer decision.
- **Shared runtime keys constrain the whole target.** If an English key appears in an out-of-scope
  section, editing one side splits it. Revert and report; never edit the other side. Propagate only
  when leaving it would *newly* desynchronise a previously consistent pair (b30, b34, b37).
- **Review rounds do not converge on unanimity.** Two readers over identical text produce disjoint
  finding sets. Phrase acceptance criteria as defect resolution, not reviewer agreement.
- **New findings on unchanged, previously-OK text default to decline** unless carrying pinned-source
  evidence — but this applies to a *later round contradicting an earlier pass*, not to first-round
  findings on untouched lines (b26, b29, b30).

## 6. Traps that have actually cost rework

- **Substring matching hides name drift, in both directions.** A count for `布莱亚` reported 8/8
  consistent because `布莱亚弗` contains it (b34). Conversely a "stale b36 reference" was the string
  `b34` inside a commit hash. Use negative lookahead or exact-token counts.
- **Replacement order matters when one form contains another.** `肖塔` is a substring of `肖塔尔`;
  replacing the shorter first would have produced `肖尔塔尔` — a corruption that reads plausibly and
  passes every gate, because nothing checks transliteration sanity.
- **`tools/i18n context` defaults to `--limit 50` and truncates silently** (b26).
- **Survey appellations whole.** b34 aligned `Briagh` but missed `Great Sand Wyrm` in the same line.
- **Check whether a section is UI before judging register.** `ward.lua` labels are bound to engine
  `DamageType` constants, so the `T.GAME.DAMAGE` rows govern (b33); same for `trap-priming.lua`
  (b31).
- **Give the executor the constraint, never a copyable example translation** — b31 offered one and
  it was copied verbatim, dropping two elements of the source.
- **`ai_state_check` requires every DONE task to carry a review contract** with a bound, archived
  record. `deferred_findings` must be empty; escalated declines belong in `host_observations`.
  For `code_legacy_v1` the record needs `candidate_locator` with exactly `spec_path` and
  `diff_path`, the diff named `CODE_DIFF-<phase>-<cycle>-<attempt>.patch` matching the record, and
  `candidate_ref` = SHA256(spec ‖ NUL ‖ diff). `STATE.mode` must be `implement` or `review_only`.
- **Adding a terminology row changes the hardcoded count** in
  `test_real_terminology_is_fully_mapped` and the assertion must be bumped in the same commit.
  *Modifying* a row does not — if the count moves there, something is wrong and the assertion should
  not be touched.
- **A `nil`-tagged row joins `audit_dynamic`'s unused list once promoted to `preferred`.** The audit
  binds by tag. Benign and precedented; diff the lists before treating a delta as a regression.

### Verification technique worth reusing

For any mechanical rename, **sentinel normalisation** proves nothing else changed: replace both the
old and new renderings with sentinels in HEAD and in the working tree, then compare. Byte-identity
(or matching SHA-256) proves no collateral edit to any other text, key, tag or line — far stronger
and cheaper than reading a large diff by eye.

## 7. Where the records live

- **Tracked evidence:** `evidence/quality/p2-batches/` — one frozen workset and one adjudication
  file per batch. The adjudication files carry the host's reasoning, including declines and their
  grounds, and are the durable record.
- **Ignored working state:** `.ai/task/<id>/` (SPEC, PLAN, SCOPE, STATE, envelope builder) and
  `.ai/reviews/<id>/` (review records). Not committed.
- **Per-batch narrative log:** [`p2-tome-texts-handoff-2026-08-23.md`](p2-tome-texts-handoff-2026-08-23.md).
- **Pinned source:** `commit:624a67329fe2ad440c5b344785a9c73fcf22ae63` in the sibling `t-engine4`
  checkout. It is the final arbiter over translations, terminology and model findings alike.
