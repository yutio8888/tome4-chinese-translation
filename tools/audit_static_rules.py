#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pure rule helpers for the static terminology audit."""
from __future__ import annotations

from collections.abc import Iterable


def normalize_typo_pairs(
    pairs: Iterable[tuple[str, str]],
) -> list[tuple[str, str]]:
    """Conservatively filter typo pairs and remove exact duplicates stably."""
    normalized = []
    seen = set()
    for bad, good in pairs:
        pair = (bad, good)
        if len(bad) < 2 or bad == good or pair in seen:
            continue
        seen.add(pair)
        normalized.append(pair)
    return normalized
