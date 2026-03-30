#!/usr/bin/env python
"""
new_insight.py — Hugo content pipeline for Dr Nor Faizal

Step 1:  python scripts/new_insight.py <slug>      → creates draft.yaml
Step 2:  fill in draft.yaml
Step 3:  python scripts/new_insight.py <slug>      → calls Gemini, saves index.en.md + index.bm.md
"""

import os
import sys
import re
import time
import argparse
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

try:
    import yaml
except ImportError:
    sys.exit("Missing: pip install pyyaml python-dotenv google-generativeai")

try:
    from google import genai
    from google.genai import types as gentypes
except ImportError:
    sys.exit("Missing: pip install google-genai")

# ── Config ─────────────────────────────────────────────────────────────────────
HUGO_ROOT    = Path(__file__).parent.parent
INSIGHTS_DIR = HUGO_ROOT / "content" / "insights"
load_dotenv(HUGO_ROOT / ".env")

GEMINI_MODEL = "gemini-2.5-pro"

BRAND_CONTEXT = """\
You are the editorial voice of Dr Nor Faizal Ahmad Bahuri — Consultant Neurosurgeon \
& Interventional Pain Specialist at KPJ Tawakkal Specialist Hospital, Kuala Lumpur. \
Oxford DPhil. He writes in batik scrubs, not white coats.

Brand voice:
- Human first, credentials second
- Warm authority — never clinical distance, never corporate speak
- Specific and precise — he names the procedure, the nerve, the moment
- Storytelling that earns trust before asking for anything
- 80/20 thinking: cut the noise, keep only what matters

He treats: brain & spine tumours, chronic headaches, migraines, chronic pain, \
interventional pain procedures. His patients are Malaysians and Indonesians seeking \
the highest standard of specialist care.\
"""

DRAFT_TEMPLATE = """\
# Fill in every field. Run the script again when done to generate the post.

slug: "{slug}"
date: "{date}"
author: "Dr Nor Faizal Ahmad Bahuri"

# Titles
title_en: ""
title_bm: ""   # leave blank — Gemini will suggest

# Categories and tags
categories:
  - ""   # e.g. Pain Management | Neuro-Oncology | Headache | Spine
tags:
  - ""   # e.g. migraine, spinal-cord-stimulation, brain-tumour

# SEO
seo_focus_keyword: ""   # e.g. "chronic back pain Malaysia"

# CTA
cta_type: "appointment"   # appointment | whatsapp | download | none
show_appointment_button: true

# ── YOUR RAW THOUGHTS ──────────────────────────────────────────────────────────
# Write freely — bullet points, fragments, Manglish, BM, EN.
# Gemini will restructure and polish.
raw_thoughts: |
  What is this post about?

  Why does this matter to my patient or GP?

  Key clinical point / story / insight:

  Anything personal or human about this topic?

  What should the reader DO after reading this?
"""

HUGO_FRONTMATTER = """\
---
title: "{title}"
date: {date}
draft: false
author: "Dr Nor Faizal Ahmad Bahuri"
categories: {categories}
tags: {tags}
description: "{description}"
seo:
  focusKeyword: "{seo_keyword}"
cta:
  type: {cta_type}
  label: "{cta_label}"
  url: "/contact"
---

"""

EN_SYSTEM = BRAND_CONTEXT + """

Your job: write a polished, publication-ready Hugo Markdown post (index.en.md).

Rules:
1. Front matter: fill all fields from the draft.
2. Body: warm, authoritative, story-led. No bullet-point dumps.
3. Word count: 400–700 words.
4. End with a CTA matching cta_type.
5. Output the COMPLETE Markdown file only — no preamble, no commentary.

Front matter format:
---
title: "..."
date: YYYY-MM-DDTHH:MM:SS+08:00
draft: false
author: "Dr Nor Faizal Ahmad Bahuri"
categories: [...]
tags: [...]
description: "..."
seo:
  focusKeyword: "..."
cta:
  type: appointment
  label: "Book a Consultation"
  url: "/contact"
---
"""

BM_SYSTEM = BRAND_CONTEXT + """

Your job: write the Bahasa Melayu version of this post (index.bm.md).

Rules:
- Modern, conversational BM — educated Malaysian friend tone, NOT formal/government
- Translate concepts faithfully; adapt idioms naturally
- Medical terms: BM equivalent where natural, English in parentheses where needed
- Same story arc and CTA as the English version
- Same Hugo front matter structure, title/description in BM
- Output the COMPLETE Markdown file only — no preamble, no commentary.
"""


# ── Helpers ────────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text


def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        sys.exit("GEMINI_API_KEY not found in .env")
    return genai.Client(api_key=api_key)


def list_models():
    client = get_client()
    print("Available models:")
    for m in client.models.list():
        print(f"  {m.name}")


def gemini_generate(system: str, prompt: str) -> str:
    client = get_client()
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                config=gentypes.GenerateContentConfig(system_instruction=system),
                contents=prompt,
            )
            text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[-1]
        if text.endswith("```"):
            text = text.rsplit("\n", 1)[0]
        return text.strip()
        except Exception as e:
            if "404" in str(e):
                print(f"\nModel '{GEMINI_MODEL}' not found.")
                list_models()
                sys.exit(1)
            if "503" in str(e) and attempt < 2:
                wait = 10 * (attempt + 1)
                print(f"Gemini busy, retrying in {wait}s...")
                time.sleep(wait)
                continue
            raise


# ── Step 1: Create draft ───────────────────────────────────────────────────────

def create_draft(slug: str) -> None:
    post_dir = INSIGHTS_DIR / slug
    post_dir.mkdir(parents=True, exist_ok=True)
    draft_path = post_dir / "draft.yaml"

    if draft_path.exists():
        print(f"draft.yaml already exists at {draft_path}")
        print(f"Fill it in, then run the script again to generate the post.")
        return

    content = DRAFT_TEMPLATE.format(
        slug=slug,
        date=datetime.now().strftime("%Y-%m-%d"),
    )
    draft_path.write_text(content, encoding="utf-8")
    print(f"Draft created: {draft_path}")
    print(f"Fill in the draft, then run: python scripts/new_insight.py {slug}")


# ── Step 2: Generate EN + BM posts via Gemini ─────────────────────────────────

def generate_posts(slug: str) -> None:
    post_dir  = INSIGHTS_DIR / slug
    draft_path = post_dir / "draft.yaml"

    if not draft_path.exists():
        print(f"No draft.yaml found. Run first without --generate to create one.")
        sys.exit(1)

    draft_text = draft_path.read_text(encoding="utf-8")

    # Strip comment lines before parsing
    clean = "\n".join(
        line for line in draft_text.splitlines()
        if not line.strip().startswith("#")
    )
    draft = yaml.safe_load(clean) or {}

    raw_thoughts = draft.get("raw_thoughts", "").strip()
    if not raw_thoughts or len(raw_thoughts) < 50:
        print("raw_thoughts is empty — fill in draft.yaml first.")
        sys.exit(1)

    now_ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")

    prompt_en = f"Date: {now_ts}\n\nDRAFT:\n{draft_text}"

    # ── Generate English post ──
    en_path = post_dir / "index.en.md"
    if en_path.exists():
        print(f"Skipping index.en.md (already exists)")
        en_md = en_path.read_text(encoding="utf-8")
    else:
        print("Generating index.en.md ...")
        en_md = gemini_generate(EN_SYSTEM, prompt_en)
        en_path.write_text(en_md, encoding="utf-8")
        print(f"Saved: {en_path}")

    # ── Generate Bahasa post ──
    bm_path = post_dir / "index.bm.md"
    if bm_path.exists():
        print(f"Skipping index.bm.md (already exists)")
    else:
        print("Generating index.bm.md ...")
        prompt_bm = f"DRAFT:\n{draft_text}\n\nENGLISH POST:\n{en_md}"
        bm_md = gemini_generate(BM_SYSTEM, prompt_bm)
        bm_path.write_text(bm_md, encoding="utf-8")
        print(f"Saved: {bm_path}")

    print(f"\nDone. Preview: hugo server -D")
    print(f"Deploy:  git add . && git commit -m 'insight: {slug}' && git push")


# ── CLI ────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Dr Faizal Hugo Content Pipeline")
    parser.add_argument("slug", nargs="?", help="Post slug, e.g. my-migraine-post")
    parser.add_argument("--list-models", action="store_true", help="List available Gemini models")
    args = parser.parse_args()

    if args.list_models:
        list_models()
        return

    slug = args.slug
    if not slug:
        raw = input("Post slug: ").strip()
        if not raw:
            sys.exit("Slug cannot be empty.")
        slug = slugify(raw)

    slug = slugify(slug)
    draft_path = INSIGHTS_DIR / slug / "draft.yaml"

    if draft_path.exists():
        generate_posts(slug)
    else:
        create_draft(slug)


if __name__ == "__main__":
    main()
