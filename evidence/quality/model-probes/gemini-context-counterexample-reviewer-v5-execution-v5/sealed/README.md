# Sealed scoring partition

This directory holds the scoring reference and is never model-facing: no file under
`sealed/` is read by the renderer or reaches a request.

No mutation is authored in execution-v5, so the reference that `freezer.mjs` produces here
(`REFERENCE.json`, a generated artifact, absent until freeze) contains 64 `CLEAN_CONTROL`
rows with zero atoms. It is read only by `scorer.mjs`, only after RAW exists, and only via
its hash binding in `frozen/REQUEST-MANIFEST.json`.
