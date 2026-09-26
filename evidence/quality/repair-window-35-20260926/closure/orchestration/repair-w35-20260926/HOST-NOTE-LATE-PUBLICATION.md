# Host note: late publication of review records (window 35)

The host did not run `publish.py` after each accepted review stage (the same omission as window 34). The review records were written together after FINAL_REVIEW(2).

For the earlier stages r0a1, r1a1 and r2a1, `publish_late.py` was used, in chronological order. It is copied unchanged from window 34 and is `publish.py` with only the live-translation-hash check removed. Every other check still applies: the child is archived and lineage-verified, `output_valid` and `read_boundary_valid` are both true, and the raw output is validated with `validate_result_bytes` against that stage's own frozen envelope (`candidate_identity`). f2a2 was published last with the unmodified `publish.py`.

There were no invalid attempts in this window.
