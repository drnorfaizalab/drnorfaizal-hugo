#!/usr/bin/env python
"""
translate_testimonials.py — Translate missing 'bm' fields in data/testimonials.yaml
using the Gemini API.

Usage:
    python scripts/translate_testimonials.py

Requirements:
    pip install google-genai python-dotenv pyyaml
    GEMINI_API_KEY set in environment or .env file
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

try:
    from google import genai
    from google.genai import types as gentypes
    import yaml
except ImportError:
    sys.exit("Missing dependencies: pip install google-genai python-dotenv pyyaml")

# ── Config ────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")

YAML_PATH    = PROJECT_ROOT / "data" / "testimonials.yaml"
GEMINI_MODEL = "gemini-2.5-pro"

SYSTEM_PROMPT = """\
You are a bilingual translator for Dr. Nor Faizal Ahmad Bahuri, an Oxford-trained \
Consultant Neurosurgeon in Kuala Lumpur.

Translate patient testimonials from English into modern, conversational \
Bahasa Melayu — the kind a professional Malaysian would speak, not formal \
government language. Keep the patient's authentic voice. Preserve medical \
terms in English where there is no natural Bahasa equivalent. Return ONLY \
the translated text, no explanation or commentary."""


def translate(client, text: str) -> str:
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        config=gentypes.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        contents=text,
    )
    return response.text.strip()


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        sys.exit("GEMINI_API_KEY not found in environment or .env file.")

    if not YAML_PATH.exists():
        sys.exit(f"File not found: {YAML_PATH}")

    with open(YAML_PATH, "r", encoding="utf-8") as f:
        testimonials = yaml.safe_load(f)

    client = genai.Client(api_key=api_key)
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
