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
  3. Fill in the template (thoughts, photos, metadata)
  4. Run again with --prepare flag to:
     a. Optimize photos in the folder (resize + compress) in-place
     b. Print ready-to-paste prompts for Gemini

Flags:
  --prepare   Optimize photos + print prompts to paste into Gemini
  --photos    Optimize photos in the slug folder only
  --slug      Specify slug directly (or pass as positional arg)
  --all       List all drafts that still need index.en.md
"""

import sys
import re
import argparse
import textwrap
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("❌  pyyaml not found. Run: pip install pyyaml")
    sys.exit(1)

# ── Config ────────────────────────────────────────────────────────────────────
HUGO_ROOT    = Path(__file__).parent.parent
INSIGHTS_DIR = HUGO_ROOT / "content" / "insights"

DIVIDER = "=" * 72

# Brand voice context prepended to every prompt
CONTEXT = """\
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
the highest standard of specialist care."""


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text


# ── STEP 1: Create draft template ─────────────────────────────────────────────
DRAFT_TEMPLATE = """\
# ============================================================
#  DR FAIZAL — INSIGHT DRAFT
#  Fill in every field. Leave a field blank if unsure.
#  Run:  python new_insight.py --prepare --slug {slug}
#  to optimize photos and get prompts to paste into Gemini.
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
        print("     Edit it, then run --prepare to get the Gemini prompts.")
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
    print(f"     3. Run:  python new_insight.py --prepare --slug {slug}")
    return draft_path


# ── STEP 2: Optimize photos in slug folder ────────────────────────────────────

IMAGE_EXTS   = {".jpg", ".jpeg", ".png", ".webp"}
MAX_WIDTH    = 1200  # px — wider images are downscaled
JPEG_QUALITY = 82    # 0–95; 82 is visually lossless for web
_RESAMPLE    = 1     # Pillow resampling filter: 1 = high-quality downscale


def process_photos(post_dir: Path) -> list:
    """Find images in post_dir, compress + resize in-place. Returns processed paths."""
    try:
        from PIL import Image
    except ImportError:
        print("❌  Pillow not found. Run: pip install Pillow")
        return []

    images = [p for p in post_dir.iterdir() if p.suffix.lower() in IMAGE_EXTS]
    if not images:
        print("   No images found in folder — skipping photo step.")
        return []

    processed = []
    for img_path in sorted(images):
        before_kb = img_path.stat().st_size // 1024
        with Image.open(img_path) as img:
            ext = img_path.suffix.lower()

            if img.width > MAX_WIDTH:
                new_h = int(img.height * MAX_WIDTH / img.width)
                img = img.resize((MAX_WIDTH, new_h), _RESAMPLE)

            if ext in {".jpg", ".jpeg"}:
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img.save(img_path, "JPEG", quality=JPEG_QUALITY,
                         optimize=True, progressive=True)
            elif ext == ".png":
                img.save(img_path, "PNG", optimize=True)
            elif ext == ".webp":
                img.save(img_path, "WEBP", quality=JPEG_QUALITY, method=6)

        after_kb = img_path.stat().st_size // 1024
        saved_pct = round((1 - after_kb / before_kb) * 100) if before_kb else 0
        print(f"   📸  {img_path.name}: {before_kb} KB → {after_kb} KB  ({saved_pct}% smaller)")
        processed.append(img_path)

    print(f"   ✅  {len(processed)} photo(s) processed.")
    return processed


# ── STEP 3: Print prompts for Gemini ─────────────────────────────────────

EN_PROMPT = """\
{context}

---

Your job: write a polished, publication-ready Hugo Markdown file (index.en.md).

Instructions:
1. Use the Hugo front matter format shown below — fill every field.
2. Body: warm, authoritative, story-led. Avoid bullet-point dumps.
3. Word count: 400–700 words for a standard insight post.
4. End with a clear CTA matching cta_type in the draft.
5. Photo placements as Hugo shortcodes: {{{{< figure src="filename" alt="..." caption="..." >}}}}
6. Output ONLY the complete Markdown file — no preamble, no commentary.

Hugo front matter format:
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
{draft_yaml}"""

BM_PROMPT = """\
{context}

---

Your job: write the Bahasa Melayu version of this post as index.bm.md.

Rules:
- Modern, conversational BM — educated Malaysian friend tone, NOT formal/government
- Translate concepts faithfully; adapt idioms naturally (don't translate literally)
- Medical terms: use BM equivalent where natural, keep English in parentheses where needed
- Same story arc and CTA as the English version
- Same Hugo front matter structure, title/description in BM
- Output ONLY the complete Markdown file — no preamble, no commentary.

DRAFT YAML:
{draft_yaml}

ENGLISH POST (index.en.md):
{english_post}"""


def prepare_draft(slug: str) -> None:
    post_dir = INSIGHTS_DIR / slug
    draft_path = post_dir / "draft.yaml"

    if not draft_path.exists():
        print(f"❌  No draft.yaml found at {draft_path}")
        print(f"     Run without --prepare first to create one.")
        sys.exit(1)

    # ── Photos ───────────────────────────────────────────────────────────────
    print(f"🖼️   Optimizing photos in {post_dir}…")
    process_photos(post_dir)

    # ── Clean the YAML (strip comments, stamp timestamp) ─────────────────────
    raw_yaml = draft_path.read_text(encoding="utf-8")
    clean_yaml = "\n".join(
        line for line in raw_yaml.splitlines()
        if not line.strip().startswith("#")
    )
    now_ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    clean_yaml = re.sub(r'date:\s*"?[\d\-T:+]+"?', f'date: "{now_ts}"', clean_yaml)

    # ── Print PROMPT 1 (English) ──────────────────────────────────────────────
    print(f"\n{DIVIDER}")
    print("PROMPT 1 OF 2 — Paste this into Gemini to generate index.en.md")
    print(DIVIDER)
    print(EN_PROMPT.format(context=CONTEXT, draft_yaml=clean_yaml))
    print(DIVIDER)

    # ── Print PROMPT 2 (BM version) ──────────────────────────────────────────
    print(f"\n{DIVIDER}")
    print("PROMPT 2 OF 2 — After saving index.en.md, paste this into Gemini to generate index.bm.md")
    print("               Replace <PASTE EN POST HERE> with the output from Prompt 1.")
    print(DIVIDER)
    print(BM_PROMPT.format(
        context=CONTEXT,
        draft_yaml=clean_yaml,
        english_post="<PASTE index.en.md CONTENT HERE>",
    ))
    print(DIVIDER)

    print(f"\n📋  Done. Copy each prompt above into Gemini in order.")
    print(f"     Save the outputs as:")
    print(f"       {post_dir}/index.en.md")
    print(f"       {post_dir}/index.bm.md")
    print(f"\n💡  Preview:  hugo server -D")
    print(f"    Deploy:   git add . && git commit -m 'insight: {slug}' && git push")


# ── STEP 4: List all pending drafts ───────────────────────────────────────────

def list_pending() -> None:
    if not INSIGHTS_DIR.exists():
        print(f"❌  Insights directory not found: {INSIGHTS_DIR}")
        sys.exit(1)

    pending = []
    for draft_path in sorted(INSIGHTS_DIR.glob("*/draft.yaml")):
        slug = draft_path.parent.name
        if not (draft_path.parent / "index.en.md").exists():
            pending.append(slug)

    if not pending:
        print("✅  No pending drafts — all have index.en.md.")
        return

    print(f"📋  {len(pending)} draft(s) waiting for --prepare:\n")
    for slug in pending:
        print(f"     python new_insight.py --prepare --slug {slug}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Dr Faizal Hugo Content Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
        Examples:
          python new_insight.py                              # interactive slug prompt
          python new_insight.py my-migraine-insight         # create draft
          python new_insight.py --photos --slug my-topic    # compress photos only
          python new_insight.py --prepare --slug my-topic   # compress photos + print prompts
          python new_insight.py --all                       # list all pending drafts
        """),
    )
    parser.add_argument("slug",      nargs="?", help="Post slug (URL-safe, e.g. my-topic)")
    parser.add_argument("--prepare", action="store_true", help="Optimize photos + print Gemini prompts")
    parser.add_argument("--photos",  action="store_true", help="Optimize photos in slug folder only")
    parser.add_argument("--all",     action="store_true", help="List all pending drafts")
    args = parser.parse_args()

    if args.all:
        list_pending()
        return

    if args.photos:
        if not args.slug:
            args.slug = input("Enter the slug: ").strip()
        post_dir = INSIGHTS_DIR / slugify(args.slug)
        if not post_dir.exists():
            print(f"❌  Folder not found: {post_dir}")
            sys.exit(1)
        process_photos(post_dir)
        return

    if args.prepare:
        if not args.slug:
            args.slug = input("Enter the slug to prepare: ").strip()
        prepare_draft(slugify(args.slug))
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
