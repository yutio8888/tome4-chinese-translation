#!/usr/bin/env python3
"""Prepare every frozen lane, then record first live binding (see README)."""
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import review_lifecycle as lifecycle
from review_prompts import build_surface_prompt as build_prompt



if __name__ == '__main__':
    lifecycle.dispatch_main('surface', build_prompt, 'codex/gpt-6-astra', 'auto')
