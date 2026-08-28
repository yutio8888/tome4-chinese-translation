# Translation reference annotation

Review every supplied item in its given order. Compare the source and target, using bounded_fixed_context only as evidence for meaning, placeholders, runtime behavior, speaker intent, and register. Do not infer facts that the supplied fields do not support.

Assign exactly one label to every item:

- CLEAN: the target has no material translation defect supported by the supplied evidence.
- SURFACE_VISIBLE_DEFECT: a material defect is visible from source and target without relying on bounded context.
- CONTEXT_DEPENDENT_DEFECT: a material defect is established only with the bounded context.
- UNRESOLVED: the supplied evidence is insufficient for a determinate label.

For every item, provide a concise evidence statement. A defect label requires one or more bounded defect atoms. Each atom must state its kind, claim, and supporting evidence. For CONTEXT_DEPENDENT_DEFECT, source_evidence_sha256s must cite the supplied source_evidence[].sha256 for that same item; do not calculate, invent, substitute, or cite any other hash. Each source_evidence text is byte-equal to the corresponding item's bounded_fixed_context, and its lowercase SHA-256 is over the exact UTF-8 bytes of text. CLEAN must have no defect atoms, source-evidence hashes, or limitations. Surface-visible defects must have no source-evidence hashes or limitations. Context-dependent defects must have no limitations. UNRESOLVED must state a non-empty limitation.

Return exactly one JSON document conforming to the supplied response schema. Take response schema_version, status, parent_queue_sha256, and shard_file_sha256 from the response schema consts. Take shard_id, item_count, item_ids, and item order from the shard. Do not add fields or prose outside the JSON document.
