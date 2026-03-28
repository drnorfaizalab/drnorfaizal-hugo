#!/usr/bin/env python3
"""
Translate missing 'bm' fields in data/testimonials.yaml using Google Translate.
Usage: python scripts/translate_testimonials.py
"""

import yaml
from deep_translator import GoogleTranslator

YAML_PATH = "data/testimonials.yaml"

def translate(text):
    return GoogleTranslator(source="en", target="ms").translate(text)

with open(YAML_PATH, "r", encoding="utf-8") as f:
    testimonials = yaml.safe_load(f)

changed = 0
for t in testimonials:
    if not t.get("bm") and t.get("en"):
        print(f"Translating: {t['name']}...")
        t["bm"] = translate(t["en"])
        changed += 1

if changed:
    with open(YAML_PATH, "w", encoding="utf-8") as f:
        yaml.dump(testimonials, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
    print(f"\nDone. {changed} translation(s) added to {YAML_PATH}")
else:
    print("Nothing to translate — all entries already have 'bm'.")
