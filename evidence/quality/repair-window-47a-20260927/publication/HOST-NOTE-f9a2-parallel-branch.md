f9a2 (FINAL cycle 9) harvest rejected with "ambiguous Claude branch": Opus issued parallel Read
calls and Claude logged one tool_use block (same message id, apiBlockIndex 3) as a side branch
off the chain, with its tool_result child hanging off that branch. Host extended
review_lifecycle._parse_native_final to accept exactly that shape (off-chain assistant node made
only of tool_use blocks, parent on the chain, message id equal to an on-chain non-final assistant
message; its tool_result children), with a regression test. A dry parse of the f9a2 log now
succeeds. The f9a2 attempt stays recorded as INVALID (not counted); its observations were
verified and adjudicated in ADJUDICATION-F9.json. The fix ships with the w47a tool commit.
