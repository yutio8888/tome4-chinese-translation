# Context evidence targeted case-control pilot v1

Status: `NO_INFERENCE/FRAME_BUILD_ONLY`.

This directory freezes only the historical-exposure registry and the candidate frame for a later source/target-only versus fixed-evidence experiment. It makes no model call, performs no source audit, creates no evidence packet, and assigns no reference label.

## What is proved

`build.mjs` reconstructs the 1,396 canonical task/revision rows in the v3 production frame from the fingerprinted terminal contextual-REVIEWER inputs. It verifies every reconstructed source and target against the hashes in v3 `CANONICAL-MEMBERSHIP.json`.

It then freezes two tracked corpora:

- 14 structured outbound/identity files, 543,016 bytes, manifest SHA-256 `021b7911ff9ca06e2e18cf3d45e86db6262267f8156c7527e0d692a73ada0aa6`;
- 122 Git-tracked RAW files, 25,470,879 bytes, manifest SHA-256 `ace4cce4ba5f61e98776a6577a34c2ff7f8e5efef487e773b1104386452272b3`. The basename rule includes names beginning `RAW-` and names exactly equal to `RAW.stdout` or `RAW.stderr`.

Exposure is fail-closed at exact-pair level. A pair is removed if a structured outbound contains the exact source/target pair, an identity artifact binds a canonical identity, an outbound contains an exact source-only or target-only alias, or the candidate is found in tracked RAW under the frozen length/encoding rule. A separate conservative structured rule removes a pair when any non-empty source or target occurs literally inside a strictly longer string leaf anywhere in a frozen outbound input JSON artifact. Structured known-input containment has no length floor; even a short exact substring is direct exposure evidence. Strict longer-than keeps equality in the exact-pair/alias rules. Duplicate task/revision rows sharing the same exact pair are removed together.

The RAW-only scan retains a separate 12-Unicode-code-point floor to avoid treating short common fragments in mixed input/output/reasoning logs as meaningful RAW evidence. That RAW floor does not weaken or filter structured known-input exclusion.

The measured reconstruction is:

- base: 1,396 rows, 1,332 exact pairs, 46 tasks;
- after structured exact pairs/identity: 1,343 rows;
- after longer outbound string-leaf containment: 1,292 rows (51 newly exposed rows across 35 pairs);
- after explicit input aliases: 1,289 rows;
- final `CONFIRMED_TRACKED_INPUT_NOVEL`: 1,289 rows, 1,250 exact pairs, 45 tasks;
- task-identifier-pure subset: 6 rows across 5 tasks. A row is in this subset only when its task ID is absent as a literal from every frozen input/identity artifact; one of the five tasks contributes two rows.

Within its actual scan population, `PRIOR-EXPOSURE-REGISTRY.json` retains every positive RAW hit, its path, occurrence count, byte offset, classification, and structured outbound anchor. That population is limited to pairs remaining after structured exact-pair/identity and exact-field-alias exclusion, with earlier longer-string containment pairs deliberately included so their RAW evidence is retained; pairs already removed by the other two structured layers are not RAW-scanned. The corrected RAW corpus has 22 literal-match records across 4 scanned pairs; all 4 pairs are also independently excluded by the longer-string-leaf rule, so the RAW layer removes no additional final rows. The registry also reports the stricter `FAIL_CLOSED_ANY_RAW_LITERAL_NOVEL` tier, which excludes unresolved RAW matches even if they appear only in assistant output/reasoning. The current frozen corpus has no unresolved-only RAW hits, so the confirmed and fail-closed tiers have the same remaining membership; the two definitions remain separate.

`NOVEL-FRAME.json` uses the more conservative `FAIL_CLOSED_ANY_RAW_LITERAL_NOVEL` tier and groups its 1,289 remaining canonical rows into 1,250 exact source/target pairs. In this frozen corpus it is byte-for-byte the same membership set as the confirmed-input tier because there are no unresolved-only RAW hits. The later pilot must sample pair units rather than treating duplicated pairs as independent observations.

## Important limitation

“Novel” here means novel only against the listed, Git-tracked corpus. It does not prove that content never appeared in a deleted file, ignored file, provider-side log, unsaved session, another checkout, or model memory. Logical RAW paths contain provider/model provenance, so these artifacts must not be sent to an external model verbatim.

The structured containment rule is intentionally conservative. Any non-empty candidate field embedded in a larger prompt, source-context packet, or serialized input string is treated as prior exposure even when the surrounding leaf is not itself named `source` or `target`.

## Rebuild and gates

Use the production checkout that still contains the terminal input files fingerprinted by the provenance snapshot:

```bash
node build.mjs --repo /path/to/production-checkout
node test-builder.mjs
node verify.mjs --repo /path/to/production-checkout
python3 -m json.tool EXPERIMENT.json >/dev/null
python3 -m json.tool PRIOR-EXPOSURE-REGISTRY.json >/dev/null
python3 -m json.tool NOVEL-FRAME.json >/dev/null
git diff --check
```

The builder reads but never writes the production checkout. Absolute paths are accepted only as runtime arguments and are not persisted.
