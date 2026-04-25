#!/usr/bin/env python
"""
translate_content.py — Translate Hugo Markdown content between English and Bahasa Malaysia.

Usage:
    python tools/translate_content.py path/to/index.en.md
    python tools/translate_content.py path/to/index.bm.md

Requirements:
    pip install google-genai python-dotenv
    GEMINI_API_KEY set in environment or .env file
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

try:
    from google import genai
    from google.genai import types as gentypes
except ImportError:
    sys.exit("Missing dependencies: pip install google-genai python-dotenv")

# ── Config ────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")

BRAND_CONTEXT_PATH = PROJECT_ROOT / "tools" / "brand-context.md"
GEMINI_MODEL = "gemini-2.5-pro"

def get_system_instruction(target_lang_name: str) -> str:
    brand_context = ""
    if BRAND_CONTEXT_PATH.exists():
        brand_context = BRAND_CONTEXT_PATH.read_text(encoding="utf-8")
    else:
        print(f"Warning: Brand context file not found at {BRAND_CONTEXT_PATH}. Proceeding without it.")

    return f"""{brand_context}

Your task is to translate the provided Hugo Markdown file into {target_lang_name}.

RULES:
1. Translate the body content accurately while maintaining the established brand voice.
2. Maintain the EXACT Hugo YAML frontmatter structure (the section between the `---` dashes at the top).
   - Translate the `title`, `description`, and SEO `keywords` fields.
   - DO NOT change programmatic fields like `date`, `url`, `type`, `weight`, `draft`, `image`, etc.
3. Keep all Markdown formatting, links, shortcodes, and image paths exactly as they are.
4. Output ONLY the final valid Markdown file (with frontmatter). 
5. Do not include any preamble, conversational text, or commentary.
"""

def translate_markdown(client, content: str, target_lang_name: str) -> str:
    system_instruction = get_system_instruction(target_lang_name)
    
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        config=gentypes.GenerateContentConfig(system_instruction=system_instruction),
        contents=content,
    )
    
    text = response.text.strip()
    
    # Strip markdown code fences if Gemini wraps the output
    if text.startswith("```markdown"):
        text = text[len("```markdown"):].strip()
    elif text.startswith("```"):
        text = text[3:].strip()
        
    if text.endswith("```"):
        text = text[:-3].strip()
        
    return text

def main():
    parser = argparse.ArgumentParser(description="Translate Hugo Markdown files (EN <-> BM)")
    parser.add_argument("file_path", help="Path to the .en.md or .bm.md file to translate")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        sys.exit("GEMINI_API_KEY not found in environment or .env file.")

    source_path = Path(args.file_path)
    if not source_path.exists():
        sys.exit(f"File not found: {source_path}")

    filename = source_path.name
    if filename.endswith(".en.md"):
        target_path = source_path.with_name(filename.replace(".en.md", ".bm.md"))
        target_lang_name = "Bahasa Malaysia (modern, conversational, educated Malaysian tone)"
    elif filename.endswith(".bm.md"):
        target_path = source_path.with_name(filename.replace(".bm.md", ".en.md"))
        target_lang_name = "English (authoritative, medical precision)"
    else:
        sys.exit("Error: File must end with '.en.md' or '.bm.md'.")

    print(f"Reading: {source_path}")
    print(f"Translating to {target_lang_name.split('(')[0].strip()}...")
    
    source_content = source_path.read_text(encoding="utf-8")
    
    client = genai.Client(api_key=api_key)
    translated_content = translate_markdown(client, source_content, target_lang_name)
    
    target_path.write_text(translated_content, encoding="utf-8")
    print(f"✅ Saved translation to: {target_path}")

if __name__ == "__main__":
    main()