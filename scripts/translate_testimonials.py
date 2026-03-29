#!/usr/bin/env python3
"""
translate_testimonials.py — Translate missing 'bm' fields in data/testimonials.yaml
using the Claude API.

Usage:
    python scripts/translate_testimonials.py

Requirements:
    pip install anthropic python-dotenv pyyaml
    ANTHROPIC_API_KEY set in environment or .env file
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

try:
    import anthropic
    import yaml
except ImportError:
    sys.exit("Missing dependencies: pip install anthropic python-dotenv pyyaml")

# ── Config ────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")

YAML_PATH  = PROJECT_ROOT / "data" / "testimonials.yaml"
CLAUDE_MODEL = "claude-opus-4-6"

SYSTEM_PROMPT = """\
You are a bilingual translator for Dr. Nor Faizal Ahmad Bahuri, an Oxford-trained \
Consultant Neurosurgeon in Kuala Lumpur.

Translate patient testimonials from English into modern, conversational \
Bahasa Melayu — the kind a professional Malaysian would speak, not formal \
government language. Keep the patient's authentic voice. Preserve medical \
terms in English where there is no natural Bahasa equivalent. Return ONLY \
the translated text, no explanation or commentary."""


def translate(client: anthropic.Anthropic, text: str) -> str:
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": text}],
    )
    return message.content[0].text.strip()


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("ANTHROPIC_API_KEY not found in environment or .env file.")

    if not YAML_PATH.exists():
        sys.exit(f"File not found: {YAML_PATH}")

    with open(YAML_PATH, "r", encoding="utf-8") as f:
        testimonials = yaml.safe_load(f)

    client = anthropic.Anthropic(api_key=api_key)
    changed = 0

    for t in testimonials:
        if not t.get("bm") and t.get("en"):
            print(f"Translating: {t['name']}...")
            t["bm"] = translate(client, t["en"])
            changed += 1

    if changed:
        with open(YAML_PATH, "w", encoding="utf-8") as f:
            yaml.dump(testimonials, f, allow_unicode=True, sort_keys=False,
                      default_flow_style=False)
        print(f"\nDone. {changed} translation(s) added to {YAML_PATH}")
    else:
        print("Nothing to translate — all entries already have 'bm'.")


if __name__ == "__main__":
    main()
