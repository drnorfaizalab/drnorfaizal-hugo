#!/usr/bin/env python3
"""
new_insight.py — Dr Nor Faizal's Hugo Content Creation Pipeline
================================================================
Usage:
  python new_insight.py                    # Interactive: prompts for slug
  python new_insight.py my-topic-slug      # Direct: uses provided slug

Workflow:
  1. Creates content/insights/<slug>/ directory
  2. Writes a pre-filled YAML template → draft.yaml
  3. You fill in the template (thoughts, photos, metadata)
  4. Run again with --process flag to:
     a. Claude polishes it → index.en.md
     b. Claude translates it → index.bm.md

Flags:
  --process   Process an existing draft.yaml through Claude
  --slug      Specify slug directly (or pass as positional arg)
  --all       Process ALL drafts that have draft.yaml but no index.en.md
"""

import os
import sys
import re
import argparse
import textwrap
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# ── Dependencies ──────────────────────────────────────────────────────────────
try:
    import anthropic
except ImportError:
    print("❌  anthropic package not found. Run: pip install anthropic python-dotenv")
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("❌  pyyaml not found. Run: pip install pyyaml")
    sys.exit(1)

# ── Config ────────────────────────────────────────────────────────────────────
load_dotenv(Path(__file__).parent.parent / ".env")

HUGO_ROOT = Path(__file__).parent.parent   # script lives in scripts/, root is one up
INSIGHTS_DIR = HUGO_ROOT / "content" / "insights"
CLAUDE_MODEL = "claude-opus-4-6"

# System prompt that encodes Dr FAB's brand voice
SYSTEM_PROMPT = """\
You are the editorial voice of Dr Nor Faizal Ahmad Bahuri — Consultant Neurosurgeon \
& Interventional Pain Specialist at KPJ Tawakkal Specialist Hospital, Kuala Lumpur. \
Oxford DPhil. He writes in batik scrubs, not white coats.

Brand voice principles:
- Human first, credentials second
- Warm authority — never clinical distance, never corporate speak
- Specific and precise — he names the procedure, the nerve, the moment
- Storytelling that earns trust before asking for anything
- 80/20 thinking: cut the noise, keep only what matters
- Bahasa Melayu version: modern, conversational BM — not formal or stiff. \
  Think educated Malaysian friend, not government pamphlet.

He treats: brain & spine tumours, chronic headaches, migraines, chronic pain, \
interventional pain procedures. His patients are Malaysians and Indonesians seeking \
the highest standard of specialist care."""


def slugify(text: str) -> str:
    """Convert freeform text to a URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text


# ── STEP 1: Create draft template ─────────────────────────────────────────────
DRAFT_TEMPLATE = """\
# ============================================================
#  DR FAIZAL — INSIGHT DRAFT
#  Fill in every field. Leave a field blank if unsure.
#  Run:  python new_insight.py --process --slug {slug}
#  to let Claude process this into polished EN + BM posts.
# ============================================================

metadata:
  title_en: ""           # English title (punchy, human, < 70 chars)
  title_bm: ""           # Bahasa title (leave blank — Claude will suggest)
  date: "{date}"         # Publication date (YYYY-MM-DD)
  author: "Dr Nor Faizal Ahmad Bahuri"
  categories:
    - ""                 # e.g. Pain Management | Neuro-Oncology | Headache | Spine
  tags:
    - ""                 # e.g. migraine, spinal-cord-stimulation, brain-tumour
  description_en: ""     # 1–2 sentence teaser for EN (leave blank — Claude will write)
  description_bm: ""     # 1–2 sentence teaser for BM (leave blank — Claude will write)

  # SEO
  seo_focus_keyword: ""  # Single keyword phrase, e.g. "chronic back pain Malaysia"
  canonical_url: ""      # Leave blank unless republishing from elsewhere

  # Social / OG
  og_image: ""           # Filename in this folder, e.g. hero.jpg
  og_image_alt: ""       # Describe the image for accessibility

  # Referral / CTA
  cta_type: "appointment"     # appointment | whatsapp | download | none
  cta_label_en: "Book a Consultation"
  cta_label_bm: "Buat Temujanji"

# ------------------------------------------------------------
#  YOUR RAW THOUGHTS
#  Write freely — bullet points, fragments, Manglish, BM, EN.
#  Claude will restructure and polish. Do NOT over-write here.
# ------------------------------------------------------------

raw_thoughts: |
  What is this post about? (one sentence)

  Why does this matter to my patient or GP?

  Key clinical point / story / insight:

  Anything personal or human about this topic?

  What should the reader DO after reading this?

# ------------------------------------------------------------
#  PHOTOS IN THIS FOLDER
#  List filenames and describe each one briefly.
# ------------------------------------------------------------

photos:
  - file: ""
    caption_en: ""
    caption_bm: ""

# ------------------------------------------------------------
#  INTERNAL NOTES (not published)
# ------------------------------------------------------------
notes: |
  (optional: draft deadline, source papers, procedure codes, etc.)
"""


def create_draft(slug: str) -> Path:
    post_dir = INSIGHTS_DIR / slug
    post_dir.mkdir(parents=True, exist_ok=True)

    draft_path = post_dir / "draft.yaml"
    if draft_path.exists():
        print(f"⚠️   draft.yaml already exists at {draft_path}")
        print("     Edit it, then run with --process to generate the posts.")
        return draft_path

    content = DRAFT_TEMPLATE.format(
        slug=slug,
        date=datetime.now().strftime("%Y-%m-%d"),
    )
    draft_path.write_text(content, encoding="utf-8")
    print(f"✅  Draft created: {draft_path}")
    print(f"\n📝  Next steps:")
    print(f"     1. Open and fill in:  {draft_path}")
    print(f"     2. Add any photos to: {post_dir}/")
    print(f"     3. Run:  python new_insight.py --process --slug {slug}")
    return draft_path


# ── STEP 2: Process draft through Claude ──────────────────────────────────────

EN_PROMPT = """\
You are given a YAML draft written by Dr Nor Faizal. Your job:

1. Write a polished, publication-ready Hugo Markdown file (index.en.md).
2. Use the YAML front matter format shown below.
3. The body should be warm, authoritative, story-led. Avoid bullet-point dumps.
4. Suggested word count: 400–700 words for a standard insight post.
5. Embed a clear CTA at the end that matches cta_type in the draft.
6. Include suggested photo placements as Hugo shortcodes: {{< figure src="filename" alt="..." caption="..." >}}
7. Output ONLY the complete Markdown file — no preamble, no commentary.

Hugo front matter format to use:
---
title: "..."
date: YYYY-MM-DDTHH:MM:SS+08:00
draft: false
author: "Dr Nor Faizal Ahmad Bahuri"
categories: [...]
tags: [...]
description: "..."
image: "..."
imageAlt: "..."
seo:
  focusKeyword: "..."
cta:
  type: appointment
  label: "Book a Consultation"
  url: "/contact"
---

DRAFT YAML:
{draft_yaml}
"""

BM_PROMPT = """\
You are given:
1. A YAML draft by Dr Nor Faizal
2. The finished English Markdown post

Your job: Write the Bahasa Melayu version as index.bm.md.

Rules:
- Modern, conversational BM — educated Malaysian friend tone, NOT formal/government
- Translate concepts faithfully; adapt idioms naturally (don't translate literally)
- Medical terms: use BM equivalent where natural, keep English term in parentheses where needed
- Same story arc and CTA as the English version
- Same Hugo front matter structure, with title/summary in BM
- Output ONLY the complete Markdown file.

DRAFT YAML:
{draft_yaml}

ENGLISH POST:
{english_post}
"""


def call_claude(client: anthropic.Anthropic, prompt: str) -> str:
    """Streaming API call — avoids timeout on long posts, returns full text."""
    with client.messages.stream(
        model=CLAUDE_MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
        print()  # newline after streaming
        return stream.get_final_message().content[0].text


def process_draft(slug: str, dry_run: bool = False) -> None:
    post_dir = INSIGHTS_DIR / slug
    draft_path = post_dir / "draft.yaml"

    if not draft_path.exists():
        print(f"❌  No draft.yaml found at {draft_path}")
        print(f"     Run without --process first to create one.")
        sys.exit(1)

    draft_yaml = draft_path.read_text(encoding="utf-8")

    # Strip comment lines for cleaner context sent to Claude
    clean_yaml = "\n".join(
        line for line in draft_yaml.splitlines()
        if not line.strip().startswith("#")
    )

    # Stamp with processing time so same-day posts are ordered granularly
    now_ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    clean_yaml = re.sub(r'date:\s*"?[\d\-T:+]+"?', f'date: "{now_ts}"', clean_yaml)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌  ANTHROPIC_API_KEY not found in environment / .env file")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # ── English post ──────────────────────────────────────────────────────────
    print("🤖  Generating English post (index.en.md)…")
    en_post = call_claude(client, EN_PROMPT.format(draft_yaml=clean_yaml))

    en_path = post_dir / "index.en.md"
    if not dry_run:
        en_path.write_text(en_post, encoding="utf-8")
        print(f"✅  Saved: {en_path}")
    else:
        print("── DRY RUN — English post preview ──")
        print(en_post[:800], "\n[...truncated]")

    # ── Bahasa Melayu post ────────────────────────────────────────────────────
    print("🤖  Generating Bahasa Melayu post (index.bm.md)…")
    bm_post = call_claude(
        client, BM_PROMPT.format(draft_yaml=clean_yaml, english_post=en_post)
    )

    bm_path = post_dir / "index.bm.md"
    if not dry_run:
        bm_path.write_text(bm_post, encoding="utf-8")
        print(f"✅  Saved: {bm_path}")
    else:
        print("── DRY RUN — BM post preview ──")
        print(bm_post[:800], "\n[...truncated]")

    if not dry_run:
        print(f"\n🎉  Done! Posts are ready to review:")
        print(f"     EN: {en_path}")
        print(f"     BM: {bm_path}")
        print(f"\n💡  Preview locally:  hugo server -D")
        print(f"     Deploy:           git add . && git commit -m 'insight: {slug}' && git push")


# ── STEP 3: Batch process all pending drafts ──────────────────────────────────

def process_all() -> None:
    if not INSIGHTS_DIR.exists():
        print(f"❌  Insights directory not found: {INSIGHTS_DIR}")
        sys.exit(1)

    pending = []
    for draft_path in INSIGHTS_DIR.glob("*/draft.yaml"):
        slug = draft_path.parent.name
        en_path = draft_path.parent / "index.en.md"
        if not en_path.exists():
            pending.append(slug)

    if not pending:
        print("✅  No pending drafts found.")
        return

    print(f"📋  Found {len(pending)} pending draft(s): {', '.join(pending)}")
    for slug in pending:
        print(f"\n── Processing: {slug} ──")
        process_draft(slug)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Dr Faizal Hugo Content Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
        Examples:
          python new_insight.py                              # interactive slug prompt
          python new_insight.py my-migraine-insight         # create draft
          python new_insight.py --process --slug my-topic   # process draft → EN + BM
          python new_insight.py --all                       # process all pending drafts
          python new_insight.py --process --slug my-topic --dry-run
        """),
    )
    parser.add_argument("slug", nargs="?", help="Post slug (URL-safe, e.g. my-topic)")
    parser.add_argument("--process", action="store_true", help="Process draft through Claude")
    parser.add_argument("--all", action="store_true", help="Process all pending drafts")
    parser.add_argument("--dry-run", action="store_true", help="Preview output without saving")
    args = parser.parse_args()

    if args.all:
        process_all()
        return

    if args.process:
        if not args.slug:
            args.slug = input("Enter the slug to process: ").strip()
        process_draft(slugify(args.slug), dry_run=args.dry_run)
        return

    # Default: create a new draft
    slug = args.slug
    if not slug:
        raw = input("📌  New post topic or slug: ").strip()
        if not raw:
            print("❌  Slug cannot be empty.")
            sys.exit(1)
        slug = slugify(raw)
        print(f"   → Slug: {slug}")

    create_draft(slugify(slug))


if __name__ == "__main__":
    main()
