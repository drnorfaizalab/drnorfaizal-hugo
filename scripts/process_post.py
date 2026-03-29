#!/usr/bin/env python3
"""
process_post.py — Edit and translate a Hugo content file using the Claude API.

Reads the Dr. Faizal brand brief from GEMINI.md and applies it via Claude to:
  1. Edit the source file for medical authority, tone, and precision.
  2. Translate it into the paired language and save as the mirror file.

Usage (run from project root):
    python scripts/process_post.py content/insights/your-article/index.en.md
    python scripts/process_post.py content/insights/your-article/index.bm.md

Requirements:
    pip install anthropic
    ANTHROPIC_API_KEY set in environment or .env file
"""

import os
import sys
import re
from pathlib import Path

try:
    import anthropic
except ImportError:
    sys.exit("Missing dependency: pip install anthropic")

# ── Paths ────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent
GEMINI_MD    = PROJECT_ROOT / "GEMINI.md"

# ── Load brand brief ─────────────────────────────────────────────────────────

if not GEMINI_MD.exists():
    sys.exit(f"Brand brief not found: {GEMINI_MD}")

BRAND_BRIEF = GEMINI_MD.read_text(encoding="utf-8")

# ── Claude system prompt ──────────────────────────────────────────────────────

SYSTEM_PROMPT = f"""You are an expert medical content editor and bilingual translator working for Dr. Nor Faizal, an Oxford-trained Neurosurgeon.

Your every decision is governed by this brand brief:

---
{BRAND_BRIEF}
---

When given a Hugo markdown file, you will perform TWO tasks and return TWO clearly-labelled sections:

**TASK 1 — EDITED SOURCE**
Return the full edited source file. Apply the language style guide for the detected language. Keep all YAML frontmatter intact — do NOT change keys, categories, tags, or date. You may refine the `title` and `description` values for precision and authority. Keep the same filename language (en or bm).

**ENGLISH STYLE RULES (apply when editing or translating into English):**
- Voice: the specialist who has nothing to prove. Calm, precise, human.
- Perspective: first person. Written as if talking to one's own inner self — honest, unguarded, direct. Not a speech to an audience.
- Short sentences. One idea at a time. No run-ons.
- Tone: quietly inspiring — not motivational-poster energy, not clinical detachment. The space between.
- Cut filler. No "it is important to note", "in order to", "as we can see". Say the thing directly.
- Use specific words over vague ones (e.g. "the tumour shrank" not "there was a positive response").
- Medical terms are fine — follow each with a plain one-line payoff for the patient (e.g. "*Microdiscectomy* — a keyhole procedure that removes the fragment pressing on your nerve.").
- No hospital-speak. Active voice. Write like a person, not a press release.

**TASK 2 — TRANSLATED FILE**
Return the full translated mirror file. If the source is English (.en.md), translate to Bahasa Melayu. If Bahasa (.bm.md), translate to English. Apply the correct voice (Authority vs Reach) from the style guide. Keep all YAML frontmatter keys identical to the source — only translate the values of `title` and `description`.

**BAHASA MELAYU STYLE RULES (override defaults when writing or translating into BM):**
- Use modern, conversational Bahasa — the kind a professional speaks, not a textbook.
- Perspective: orang pertama. Ditulis seperti bercakap dengan diri sendiri — jujur, tanpa topeng, langsung. Bukan ucapan kepada khalayak.
- Short sentences. Direct. No padding.
- Tone: calm confidence with quiet inspiration. Never preachy.
- Cut any word that doesn't earn its place. No filler phrases (e.g. avoid "adalah merupakan", "dalam konteks ini", "seperti yang kita sedia maklum").
- Prefer common everyday words over formal ones (e.g. "guna" not "menggunakan", "buat" not "melaksanakan") unless precision demands otherwise.
- Keep medical terms in English with a brief plain-Bahasa explanation only if needed.
- Do NOT do literal word-for-word translation from English — rewrite for natural Bahasa flow.

Format your response EXACTLY like this (no other commentary outside these blocks):

=== EDITED SOURCE ===
<full edited markdown here>
=== END EDITED SOURCE ===

=== TRANSLATED FILE ===
<full translated markdown here>
=== END TRANSLATED FILE ===
"""

# ── Helpers ───────────────────────────────────────────────────────────────────

def detect_language(filepath: Path) -> str:
    """Return 'en' or 'bm' based on filename suffix."""
    name = filepath.name
    if ".en." in name:
        return "en"
    if ".bm." in name:
        return "bm"
    sys.exit(f"Cannot detect language from filename: {name}\nFile must contain '.en.' or '.bm.'")


def mirror_path(filepath: Path, source_lang: str) -> Path:
    """Return the path of the paired-language mirror file."""
    target_lang = "bm" if source_lang == "en" else "en"
    new_name = filepath.name.replace(f".{source_lang}.", f".{target_lang}.")
    return filepath.parent / new_name


def extract_block(response: str, tag: str) -> str:
    """Extract content between === TAG === and === END TAG === markers."""
    pattern = rf"=== {re.escape(tag)} ===\n(.*?)\n=== END {re.escape(tag)} ==="
    match = re.search(pattern, response, re.DOTALL)
    if not match:
        sys.exit(f"Claude response missing expected block: '{tag}'\n\nRaw response:\n{response}")
    return match.group(1).strip()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/process_post.py <path/to/index.en.md>")
        sys.exit(1)

    source_path = Path(sys.argv[1])
    if not source_path.exists():
        sys.exit(f"File not found: {source_path}")

    source_lang  = detect_language(source_path)
    target_path  = mirror_path(source_path, source_lang)
    source_text  = source_path.read_text(encoding="utf-8")

    lang_label = "English" if source_lang == "en" else "Bahasa Melayu"
    print(f"Processing {source_path.name} ({lang_label}) ...")

    # ── Call Claude ───────────────────────────────────────────────────────────
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        # Try loading from .env in project root
        env_file = PROJECT_ROOT / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("ANTHROPIC_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break

    if not api_key:
        sys.exit("ANTHROPIC_API_KEY not found in environment or .env file.")

    client = anthropic.Anthropic(api_key=api_key)

    user_message = (
        f"Source language: {lang_label}\n"
        f"Source file: {source_path.name}\n\n"
        f"{source_text}"
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    raw = response.content[0].text

    # ── Parse response ────────────────────────────────────────────────────────
    edited      = extract_block(raw, "EDITED SOURCE")
    translated  = extract_block(raw, "TRANSLATED FILE")

    # ── Write files ───────────────────────────────────────────────────────────
    source_path.write_text(edited, encoding="utf-8")
    print(f"  Edited source saved   → {source_path}")

    target_path.write_text(translated, encoding="utf-8")
    print(f"  Translation saved     → {target_path}")

    print("\nDone. Review both files before setting draft: false.")


if __name__ == "__main__":
    main()
