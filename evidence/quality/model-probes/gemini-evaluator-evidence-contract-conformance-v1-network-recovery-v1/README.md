# Gemini evaluator evidence-contract conformance v1 — network recovery v1

This is a fresh, one-cell recovery package for `combined-p1-s2-a-network-retry-1`. It copies only the predecessor's static request, S2 schema, repaired parser/metric semantics, and pinned route contract. It does not import predecessor code or dynamic execution evidence.

## Fixed scope

- one cell, one agy process, one inference, `MAX_ATTEMPTS=1`;
- no retry, context cell, model listing, qualification, or replication;
- exact request SHA-256 `46a6358dab506eca4f0a69b8af0232227da813bebed722173c9972a2d95eda99` and 6,958 UTF-8 bytes;
- exact S2 schema SHA-256 `1dce33b98f259190a73df85dca957feb7f73e93f62501f22c02e512ef3cfc138`;
- predecessor tree SHA-256 `df8798c8c42315f1ded923c632084140738a5e1e52059e86f4abdc5d329a2dad` remains immutable.

Membership failure is a descriptive metric, not structural invalidity. Any recovery result is a single unreplicated sample and is not evidence of model effectiveness. Cross-task synthesis must remain descriptive.

## Zero-call preparation

```bash
node freezer.mjs --check
node build-manifest.mjs --check
node tests/test-package.mjs
node preflight.mjs
```

Before task-owned gates exist, preflight must report `NO_GO_REQUIRED_GATES`, `NO_RUN`, and `0/0` process/inference counts. `PACKAGE_REVIEW.json` and `EXECUTION_AUTHORIZATION.json` are read only from the task directory outside this package and are never generated here.

## Authorized production command

Only after both gates validate:

```bash
node run.mjs --cell combined-p1-s2-a-network-retry-1
node post-run.mjs --write
```

Do not rerun the command after any START or outcome. `RESULT.json` and `execution/` are generated artifacts excluded from the static manifest.
