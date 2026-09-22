#!/usr/bin/env python3
"""Prepare every frozen lane, then record first live binding (see README)."""
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import review_lifecycle as lifecycle
from review_prompts import build_contextual_prompt as build_prompt



if __name__ == '__main__':
    lifecycle.dispatch_main('contextual', build_prompt, 'claude/claude-opus-5', 'bypassPermissions')
