# Host note: late publication of review records (window 34)

The host did not run `publish.py` after each accepted review stage, although window 33 did. The review records were therefore written together after FINAL_REVIEW(5).

`publish.py` checks that the live translation hash equals `STATE.current_translation_sha256`. After later fixes, that holds only for the latest frozen stage. For the earlier stages, `publish_late.py` is used. It is `publish.py` with only that live-hash check removed. Every other check is unchanged: the child is archived and lineage-verified, `output_valid` and `read_boundary_valid` are both true, and the raw output is validated with `validate_result_bytes` against that stage's own frozen envelope (`candidate_identity`).

Stages were published in chronological order: r0a1, r1a1, r2a1, f2a3, r3a1, f3a2, r4a1, f4a2, r5a1. f5a2 was published last with the unmodified `publish.py`.

f2a2 was invalid (4 of 29 verdicts). It has no review record; its raw output is kept in `.ai/reviews/`, and the dispatch is recorded in STATE with `output_valid=false`.
