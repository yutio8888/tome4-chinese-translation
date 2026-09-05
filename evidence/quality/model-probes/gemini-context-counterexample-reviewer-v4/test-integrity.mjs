#!/usr/bin/env node
import assert from 'node:assert/strict';
import {downstreamArtifactPath,frozenAllowedArtifact} from './lib.mjs';
// Release queues are permitted only at the package root; every downstream class is denied recursively.
for(const p of ['SURFACE-AUDIT-QUEUE.json','CONTEXT-AUDIT-QUEUE.json','RELEASE-STATE.json','AUDIT-RELEASE-STATE.json'])assert.equal(frozenAllowedArtifact(p),true);
for(const p of ['nested/CONTEXT-AUDIT-QUEUE.json','schemas/nested/REVIEWER-SCHEMA.json','schemas/OTHER.json','nested/RAW-x.json','nested/RESULT.json','nested/REQUEST-x.txt','nested/MUTATIONS.json','nested/CLEAN-ADJUDICATION.json','nested/CANDIDATE-x.json','nested/SELECTION-x.json','nested/EXECUTION-CLI-x.json','nested/POST-RUN-x.json'])assert.equal(downstreamArtifactPath(p),true,p);
for(const p of ['CONTEXT-AUDIT-QUEUE.json','schemas/REVIEWER-SCHEMA.json','README.md'])assert.equal(downstreamArtifactPath(p),false,p);
console.log(JSON.stringify({status:'PASS',tests:['root-exact artifact policy','recursive downstream denylist','enumerated schema allowlist']},null,2));
