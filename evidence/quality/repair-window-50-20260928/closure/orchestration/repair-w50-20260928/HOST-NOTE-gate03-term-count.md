# Gate 03 terminology row count

The first FINAL-GATES run failed only 03-toolchain-unit-tests:
`test_real_terminology_is_fully_mapped` expects the real glossary row count
(732). This window adds two talents.tsv rows by SPEC, so the count is 734.
The host (not the EXECUTOR) updated both assertions in
tests/i18n/test_toolchain_static_audit.py to 734, following the window 48
precedent (6d56a09f), confirmed the module passes, and reran all gates.
Both new rows map to the talents domain (T.GAME.TALENT); unmapped stays 0.
