# ToME4 translation quality evaluator rubric v2

Contract: `mqm-pilot-v2`. This rubric does not reinterpret v1 assessments.

Evaluate every bundled revision independently. Report observable defects and impact facts;
do not choose severity, a rule, a grade, or a final quality vector. Use only the bounded
source, target, structure, terminology, and neighboring context in the bundle.

For each finding:

1. Choose one declared `error_code`, `defect_class`, and `phenomenon`.
2. Provide short source and target evidence as `quote` plus 1-based `occurrence`.
   Offsets are host-owned. For a true omission, target quote may be empty only with
   `meaning_change.type=omitted`. For an issue affecting the entire item use
   `{ "quote": "", "occurrence": 0, "whole_item": true }`.
3. State the meaning change and fill every impact fact with `yes`, `no`, or `unknown`.
   Insufficient evidence is `unknown`, never guessed as `no`.
4. Keep propagation (`amplification_scope`) separate from per-item impact.
5. Anchors are comparison aids only. An empty anchor set is valid.

The host rejects unknown fields, missing or duplicate revisions/findings, invalid evidence,
logical contradictions, and evaluator output containing host-owned fields such as
`derived_severity`, `rule_id`, grades, provider/model identity, or offsets.

Important distinctions:

- A number, range, condition, or term error is not automatically major; report the actual
  consequences in the fact fields.
- Blind model findings are limited to substantive defects. Every finding must use
  `is_defect=yes` and `is_substantive=yes`.
- Presentation/style observations with correct core meaning are host-owned and must not be
  emitted by the model. This includes terminal punctuation alone, spacing around markup or
  CJK text, paired-punctuation style, and a merely less-natural synonym. Leave the item
  clean unless the evidence shows a substantive meaning change.
- Optional improvements and alternative acceptable phrasings are not findings; do not emit
  an `is_defect=no` observation.
- Technical failure claims require host confirmation before blocker/major derivation.
- A model technical finding without a confirming bundled deterministic gate is invalid.
- `context_sufficient=false` does not mean clean; use `unknown` for unsupported facts.
