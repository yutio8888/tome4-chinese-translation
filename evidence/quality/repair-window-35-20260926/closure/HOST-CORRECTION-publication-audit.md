# Host correction: publication audit scratch path (window 35)

`HOST-EXECUTOR-AUDIT-publication.json` in evidence commit `00d7052607ba1b88870f7f6a40836dbc1781d0bd` lists `/tmp/install-w34-publication.sh (scratch)` among the `writes` of `publication-01`. That entry was carried over from the window 34 close script and is wrong.

The native tool log of the window 35 publication child (`publication-01-native-tools.json`) shows the scratch file it actually wrote: `/tmp/install_w35_publication.sh`. That file is outside the repository and the workspace, and reviewer or executor `/tmp` scratch writes are authorized. The other `writes` entries, the PASS status and the pack verification (`VERIFY-PACK.json`, `DONE_VERIFIED`) are unaffected.

The audit JSON is left unchanged because it is part of the recorded closure; this note supersedes that one entry.
