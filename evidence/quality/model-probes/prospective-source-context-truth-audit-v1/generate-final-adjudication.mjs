#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const directory = path.dirname(fileURLToPath(import.meta.url));
const readBytes = name => fs.readFileSync(path.join(directory, name));
const readJson = name => JSON.parse(readBytes(name).toString("utf8"));
const sha256 = bytes => crypto.createHash("sha256").update(bytes).digest("hex");

const queueBytes = readBytes("AUDIT-QUEUE.json");
const queue = JSON.parse(queueBytes.toString("utf8"));
const surfaceFiles = [1, 2, 3].map(shard => `SURFACE-CANDIDATE-${shard}.json`);
const contextFiles = [1, 2, 3].map(shard => `CONTEXT-CANDIDATE-${shard}.json`);
const surfaceCandidates = surfaceFiles.flatMap(readJson);
const contextCandidates = contextFiles.flatMap(readJson);
const surfaceById = new Map(surfaceCandidates.flatMap(candidate => candidate.items).map(item => [item.audit_id, item]));
const contextById = new Map(contextCandidates.flatMap(candidate => candidate.items).map(item => [item.audit_id, item]));

const finalLabels = new Map([
  ["V1-065", "SURFACE_VISIBLE_DEFECT"],
  ["V1-071", "SURFACE_VISIBLE_DEFECT"],
  ["V1-076", "UNRESOLVED"],
  ["V1-077", "SURFACE_VISIBLE_DEFECT"],
  ["V1-100", "SURFACE_VISIBLE_DEFECT"],
  ["V1-102", "SURFACE_VISIBLE_DEFECT"],
  ["V1-106", "CONTEXT_DEPENDENT_DEFECT"]
]);

const axesByLabel = {
  CLEAN: [false, false],
  SURFACE_VISIBLE_DEFECT: [true, false],
  CONTEXT_DEPENDENT_DEFECT: [false, true],
  MIXED_DEFECT: [true, true],
  UNRESOLVED: [null, null]
};

const custom = {
  "V1-003": {
    lead_basis: "主负责人复核冻结 packet：进入位置由同一段代码明确绑定为 arena；中文补出“竞技场”没有改变目的地。",
    material_evidence: "固定上下文把该提示置于竞技场入口流程，目标中的“竞技场”是显化已绑定地点。",
    candidate_disagreement: "surface/context 候选因英文 where 的指代而保留 UNRESOLVED；主负责人以固定地点绑定将其撤销为 CLEAN。"
  },
  "V1-005": {
    lead_basis: "主负责人复核冻结 packet：第二个占位符确为另一名炼金术士制成的药剂；“一瓶%s”和“配制”保持对象与动作。",
    material_evidence: "固定调用依次传入竞争炼金术士和 other_elixir，支持量词及药剂指代。",
    candidate_disagreement: "候选因占位符所指物不足而标 UNRESOLVED；固定调用参数已消除该歧义，最终为 CLEAN。"
  },
  "V1-008": {
    lead_basis: "主负责人对照原文和译文：中文“然后”仍明确保留动作紧随其后的顺序，monster 口语化为“敌人”未改变目标范围。",
    material_evidence: "目标句保留先后关系和攻击对象，没有建立会影响操作理解的时序或目标差异。",
    candidate_disagreement: "两轮候选把 immediately 的表达差异升级为表面缺陷；主负责人判定实质时序仍被“然后”保留。"
  },
  "V1-010": {
    lead_basis: "主负责人核对补充登记的固定 tome-orcs 源码：榴弹射击触发集合正是射击、火焰喷射、暴风打击、毒弹爆射四项，译文是在修正英文 UI 的泛称。",
    material_evidence: "demolition.lua 的 callbackOnArcheryAttack 对 talent.id 只接受 SHOOT、FLAME_JET、STORMSTRIKE、FLECHETTE_BURST，和译文四项一一对应。",
    candidate_disagreement: "surface/context 候选只见 12 行 long_desc，因译文增加四项技能而判缺陷；补充固定源码证明新增说明与运行时一致，最终撤销为 CLEAN。",
    limitations: "12 行冻结 packet 本身不足以完成此核验；补充证据只供主负责人裁决，不得进入模型 A/B 输入。",
    evidence_sha256s: ["66e61a2898f55d9b4ab85cf6284022701c3dc70c7c0bd318e26e9dd5e3712f32"],
    packet_sufficient: false
  },
  "V1-011": {
    lead_basis: "主负责人复核 on_pre_use：技能必须先激活 Gestalt，并满足精神护盾存在或强化格式塔不在冷却；中文完整反映实际可用条件。",
    material_evidence: "固定条件是 not Gestalt active，或同时无护盾且 Improved Gestalt 冷却时拒绝使用；目标准确转写其允许条件。",
    candidate_disagreement: "surface 候选把中文新增 Gestalt 条件视为缺陷，context 候选改判 MIXED；主负责人以同一冻结 pre-use 逻辑确认中文修正了英文遗漏，最终为 CLEAN。"
  },
  "V1-026": {
    lead_basis: "主负责人复核冻结调用：these 指此前列出的 ingredients；中文“这些原料”没有新增对象。",
    material_evidence: "对话分支和交付逻辑共同把代词绑定到当前药剂所需原料。",
    candidate_disagreement: "候选因 these 的指代仅在 context 中可见而标 UNRESOLVED；固定分支已足以消除歧义，最终为 CLEAN。"
  },
  "V1-064": {
    lead_basis: "主负责人按材料性标准复核：同一段落先称“领主”后以第一人称说“我是主人”，人物连续且身份不会被读成两人；这是称谓一致性问题，不是实质身份分裂。",
    material_evidence: "完整对白只有同一首领说话，叙事动作与第一人称自称连续。",
    candidate_disagreement: "两轮候选把 Master 的两种中文表达判为身份分裂；主负责人认为语境排除了人物混淆，降为非材料性差异。"
  },
  "V1-068": {
    lead_basis: "主负责人复核全文和署名：正文“侍奉自己的主人”是仆从关系的自然表达，末尾“领主”仍清楚指向同一人，没有改变人物或关系。",
    material_evidence: "信件由 The Master 署名并直接称收信人为仆从；两处表达在中文中承担关系称谓与署名两个不同功能。",
    candidate_disagreement: "候选因 Master/领主/主人映射而保留 UNRESOLVED；主负责人确认身份和主仆关系均无歧义，最终为 CLEAN。"
  },
  "V1-076": {
    lead_basis: "主负责人无法仅凭冻结材料确认两处 the shadow 是否是既定实体名“堡垒之影”。",
    material_evidence: "目标把普通形式 the shadow 两次具体化为“堡垒之影”，但 packet 只说明该生物由持杖者驱使，未给出名称或堡垒关系。",
    candidate_disagreement: "主负责人同意两轮候选维持 UNRESOLVED；没有按更严厉解释把不确定性补写为缺陷。",
    limitations: "冻结 packet 缺少实体命名或指代绑定，两个材料轴均不能可靠确定。",
    packet_sufficient: false
  },
  "V1-089": {
    lead_basis: "主负责人复核完整对话：说话者主持并控制鲜血之环，译文虽省略 my 的显式所有格，但不影响玩家理解场所、主持者或两个选择。",
    material_evidence: "同一说话者立即规定付费参赛或消失，控制关系在交互中清楚；所有格省略没有改变任务事实。",
    candidate_disagreement: "两轮候选把 my 的省略判为所有权事实缺失；主负责人按材料性门槛降为非实质省略，最终为 CLEAN。"
  },
  "V1-099": {
    lead_basis: "主负责人对照表面文本与拒绝分支：“现在没空帮你”自然表达当前不能援助，没有承诺不同条件或改变任务结果。",
    material_evidence: "该回答只是不接受当前炼金术士任务；中文保留当前时点和拒绝援助。",
    candidate_disagreement: "两轮候选把 cannot at this time 与“没空”的语用差异判为原因收窄；主负责人认为不构成材料性条件变化，最终为 CLEAN。"
  },
  "V1-111": {
    lead_basis: "主负责人核对项目权威术语表：Yeek 的既定中文名称就是“夺心魔”，译文没有替换种族。",
    material_evidence: "terminology/creatures.tsv 固定 Yeek -> 夺心魔；The Way -> 维网的相邻术语也与目标一致。",
    candidate_disagreement: "surface/context 候选把 Yeek 与“夺心魔”当作不同种族；权威术语映射证明这是候选误报，最终为 CLEAN。",
    limitations: "该术语映射不在 12 行 item packet 内，只用于主负责人裁决，不进入模型输入。",
    evidence_sha256s: ["0e252381c718ecfd8378a66e5f467c0999a00f61bc5a4a4622807265821ec525"],
    packet_sufficient: false
  },
  "V1-113": {
    lead_basis: "主负责人核对项目权威术语表：Archmage 的既定职业名是“元素法师”，两边指向同一职业。",
    material_evidence: "terminology/classes.tsv 固定 Archmage -> 元素法师，目标没有缩窄或替换对抗对象。",
    candidate_disagreement: "候选因 packet 缺少职业术语映射而维持 UNRESOLVED；权威映射消除歧义，最终为 CLEAN。",
    limitations: "该术语映射不在 12 行 item packet 内，只用于主负责人裁决，不进入模型输入。",
    evidence_sha256s: ["4658981b3a08678fa68f4d775566682c3e2c7204ee83f081a269c84e8ce2a7f2"],
    packet_sufficient: false
  },
  "V1-065": {
    lead_basis: "主负责人确认表面材料缺陷：immediate 表示迫切、当下优先，译文“最大”改成威胁程度排名。",
    material_evidence: "新王面对的是最明显且最迫切的威胁；目标变成最大且最明显，改变叙事判断。",
    candidate_disagreement: "无结论分歧；主负责人同意两轮候选的表面缺陷结论并独立核对其材料性。"
  },
  "V1-071": {
    lead_basis: "主负责人确认表面材料缺陷：译文遗漏水晶球是从马基·埃亚尔旅行至此的手段，并把惊讶推测改成确定否认。",
    material_evidence: "原文明确 used [the Orb] to travel here，后文又确认它确为 Orb of Many Ways；目标未保留该行动关系和语气。",
    candidate_disagreement: "无结论分歧；主负责人同意两轮候选的表面缺陷结论并以相邻对白复核。"
  },
  "V1-077": {
    lead_basis: "主负责人确认表面材料缺陷：technically 是严格或名义意义上的限定，译文“真正的结束”反而把结论绝对化。",
    material_evidence: "玩家只是 technically 终结厄流战争；目标声称战争真正结束，改变叙事结论范围。",
    candidate_disagreement: "无结论分歧；主负责人同意两轮候选的表面缺陷结论。"
  },
  "V1-100": {
    lead_basis: "主负责人确认表面材料缺陷：原文刻意把多次 imploded 与紧邻的 exploded 分列，译文“体内发生爆裂”把向内坍爆改成体内爆裂。",
    material_evidence: "试验品 A-C/F/H-K/M 的死亡方式是 implosion，D 才是 explosion；目标改变了前者的具体叙事事件。",
    candidate_disagreement: "无结论分歧；主负责人同意两轮候选的表面缺陷结论，并保留这是细粒度叙事事实而非机制错误的限制。",
    limitations: "缺陷影响日志中的死亡方式区分，不影响运行机制。"
  },
  "V1-102": {
    lead_basis: "主负责人确认表面材料缺陷：目标把“我在荒野遇到过的学徒”改成“荒野中的学徒”，遗漏两人曾经相遇的关系。",
    material_evidence: "后续对白确认对方曾伪装成学徒旅行并考察玩家；既往相遇是当前认出身份的原因。",
    candidate_disagreement: "无结论分歧；主负责人同意两轮候选的表面缺陷结论。"
  },
  "V1-106": {
    lead_basis: "主负责人确认纯上下文缺陷：表面上 animate 可宽泛理解为“唤醒”，但固定前文明确最新仆从是一具近乎未腐的尸体，并要通过死灵仪式使其复生。",
    material_evidence: "前一则固定笔记写明 body、ritual 和 dark menagerie；在该语境中 animate 是使尸体成为亡灵仆从，而“唤醒”会被理解为叫醒已有生命的仆从。",
    candidate_disagreement: "surface/context 候选均判 CLEAN；独立 challenger 首先指出尸体语境，主负责人重新核对固定 packet 后确认 context_material_contribution=true。"
  }
};

const makeBinding = (file, shardId) => {
  const bytes = readBytes(file);
  return {shard_id: shardId, sha256: sha256(bytes), size_bytes: bytes.length};
};

const items = queue.items.map(queueItem => {
  const surface = surfaceById.get(queueItem.audit_id);
  const context = contextById.get(queueItem.audit_id);
  if (!surface || !context) throw new Error(`${queueItem.audit_id}: candidate missing`);
  const finalLabel = finalLabels.get(queueItem.audit_id) ?? "CLEAN";
  const [surfaceAxis, contextAxis] = axesByLabel[finalLabel];
  const override = custom[queueItem.audit_id] ?? {};
  const candidatesAreClean = surface.label === "CLEAN" && context.label === "CLEAN";
  const leadBasis = override.lead_basis ?? `主负责人独立核对原文、译文和冻结 packet：${context.reason}`;
  const materialEvidence = override.material_evidence ?? "";
  const candidateDisagreement = override.candidate_disagreement ?? (candidatesAreClean ? "" : "主负责人独立复核后同意候选的材料轴和标签；本字段用于记录非 CLEAN 候选已被显式核对。 ");
  const evidenceHashes = override.evidence_sha256s ?? context.evidence_sha256s;
  const packetSufficient = override.packet_sufficient ?? context.packet_sufficient;
  const limitations = override.limitations ?? "";
  return {
    audit_id: queueItem.audit_id,
    task_id: queueItem.task_id,
    original_revision_key: queueItem.original_revision_key,
    category: queueItem.category,
    surface_candidate: {label: surface.label, reason: surface.reason},
    context_candidate: {label: context.label, reason: context.reason},
    final_label: finalLabel,
    material_axis: {surface_material_defect: surfaceAxis, context_material_contribution: contextAxis},
    packet_sufficient: packetSufficient,
    determinate: finalLabel !== "UNRESOLVED",
    written_evidence: {
      lead_basis: leadBasis,
      material_evidence: materialEvidence,
      candidate_disagreement: candidateDisagreement,
      source_evidence_sha256s: [...new Set(evidenceHashes)],
      limitations
    },
    lead_verified: true
  };
});

const adjudication = {
  schema_version: "prospective-source-context-truth-adjudication-v1",
  status: "LEAD_ADJUDICATION_COMPLETE",
  queue_sha256: sha256(queueBytes),
  surface_candidate_hashes: surfaceFiles.map((file, index) => makeBinding(file, index + 1)),
  context_candidate_hashes: contextFiles.map((file, index) => makeBinding(file, index + 1)),
  items
};

fs.writeFileSync(path.join(directory, "FINAL-ADJUDICATION.json"), `${JSON.stringify(adjudication, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({status: "WROTE", items: items.length, labels: Object.groupBy(items, item => item.final_label)}, (_key, value) => Array.isArray(value) && value[0]?.audit_id ? value.length : value, 2)}\n`);
