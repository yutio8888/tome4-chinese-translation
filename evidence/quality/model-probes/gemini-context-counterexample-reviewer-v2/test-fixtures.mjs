#!/usr/bin/env node
// v2 fail-closed fixture entry point; deliberately performs no route or model call.
await import('./test-source-binding.mjs');
await import('./test-assignment.mjs');
await import('./test-zero-call.mjs');
await import('./test-schemas.mjs');
