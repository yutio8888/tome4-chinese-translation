#!/usr/bin/env node

import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {buildTargetBinding} from "./bind-targets.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");
const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`, "utf8");
if (process.argv.length !== 4 || process.argv[2] !== "--inventory") throw new Error("usage: node verify-target-bind.mjs --inventory INVENTORY_JSONL");
const outputs = buildTargetBinding(path.resolve(process.argv[3]));
for (const [name, value] of Object.entries(outputs)) assert.deepEqual(fs.readFileSync(path.join(here, name)), jsonBytes(value), `${name}: rebuild drift`);
const registry = outputs["TARGET-BINDING-REGISTRY.json"];
const queue = outputs["CLEAN-AUDIT-SURFACE-QUEUE.json"];
const report = outputs["TARGET-BIND-REPORT.json"];
assert.equal(registry.records.length, 240);
assert.equal(queue.items.length, 120);
assert.equal(new Set(registry.records.map(record => record.screen_id)).size, 240);
assert.equal(new Set(queue.items.map(item => item.audit_id)).size, 120);
assert.equal(queue.items.every(item => Object.keys(item).sort().join(",") === "audit_id,profile,response,source,target"), true);
assert.equal(JSON.stringify(queue).includes("revision_id"), false);
assert.equal(JSON.stringify(queue).includes("source_context"), false);
assert.equal(report.hashes.target_binding_registry, sha256(jsonBytes(registry)));
assert.equal(report.hashes.surface_queue, sha256(jsonBytes(queue)));
console.log(JSON.stringify({status: "PASS", bound: 240, surface_items: 120, hashes: report.hashes}, null, 2));
