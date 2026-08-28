#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const directory = path.dirname(fileURLToPath(import.meta.url));
const repositoryRoot = execFileSync("git", ["rev-parse", "--show-toplevel"], {cwd: directory, encoding: "utf8"}).trim();
const argv = process.argv.slice(2);
const orcsIndex = argv.indexOf("--orcs-repo");
if (orcsIndex === -1 || !argv[orcsIndex + 1]) throw new Error("usage: node verify-lead-supplemental.mjs --orcs-repo PATH");
const orcsRoot = path.resolve(argv[orcsIndex + 1]);
const registry = JSON.parse(fs.readFileSync(path.join(directory, "LEAD-SUPPLEMENTAL-EVIDENCE.json"), "utf8"));
const sha256 = bytes => crypto.createHash("sha256").update(bytes).digest("hex");

if (registry.status !== "FROZEN_BEFORE_FINAL_ADJUDICATION" || registry.items.length !== 3) throw new Error("supplemental registry contract mismatch");
for (const item of registry.items) {
  const root = item.repository_alias === "tome-orcs" ? orcsRoot : repositoryRoot;
  const file = path.join(root, item.relative_path);
  const bytes = fs.readFileSync(file);
  if (sha256(bytes) !== item.artifact_sha256) throw new Error(`${item.audit_id}: artifact hash mismatch`);
  const text = bytes.toString("utf8");
  if (!text.includes(item.line_anchor)) throw new Error(`${item.audit_id}: line anchor missing`);
  if (item.repository_alias === "tome-orcs") {
    const head = execFileSync("git", ["rev-parse", "HEAD"], {cwd: orcsRoot, encoding: "utf8"}).trim();
    if (head !== item.commit) throw new Error(`${item.audit_id}: source commit mismatch`);
    for (const talent of ["T_SHOOT", "T_FLAME_JET", "T_STORMSTRIKE", "T_FLECHETTE_BURST"]) {
      if (!text.includes(talent)) throw new Error(`${item.audit_id}: ${talent} missing`);
    }
  } else {
    const line = text.split(/\r?\n/u).find(value => value.startsWith(`${item.line_anchor}\t`));
    if (!line) throw new Error(`${item.audit_id}: terminology row missing`);
    if (item.audit_id === "V1-111" && !line.startsWith("Yeek\t夺心魔\t")) throw new Error("V1-111: terminology mapping mismatch");
    if (item.audit_id === "V1-113" && !line.startsWith("Archmage\t元素法师\t")) throw new Error("V1-113: terminology mapping mismatch");
  }
}

process.stdout.write(`${JSON.stringify({status: "PASS", items: registry.items.length}, null, 2)}\n`);
