#!/usr/bin/env python
"""
ai_compose.py — Gemini for composing content ideas (Python port of ai-compose.js)
All output is automatically saved to Raw Ideas Inbox in Notion.

Usage:
    python tools/ai_compose.py "write a TikTok hook about spine surgery" [--file path/to/file]
    python tools/ai_compose.py          (interactive mode)

Requirements:
    pip install google-genai python-dotenv notion-client
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
    sys.exit("Missing dependencies: pip install google-genai python-dotenv notion-client")

try:
    from notion_client import Client as NotionClient
    HAS_NOTION = True
except ImportError:
    HAS_NOTION = False

# ── Config ────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")

BRAND_CONTEXT_PATH = PROJECT_ROOT / "tools" / "brand-context.md"
GEMINI_MODEL = "gemini-2.5-pro"


def get_system_instruction() -> str:
    """Reads the brand context file to guide the GenAI system prompt."""
    brand_context = ""
    if BRAND_CONTEXT_PATH.exists():
        brand_context = BRAND_CONTEXT_PATH.read_text(encoding="utf-8")
    else:
        print(f"Warning: Brand context file not found at {BRAND_CONTEXT_PATH}. Proceeding without it.")

    return f"""{brand_context}

You are the content and language specialist for Dr Nor Faizal Ahmad Bahuri.
Your role: generate, translate, and refine all written content.
Voice: Human first, credentials second.
Bilingual: Bahasa Malaysia for reach, English for authority.
Platforms: TikTok, Instagram, YouTube, Facebook, LinkedIn.
"""


def ask(prompt: str, context_file: str = None) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        sys.exit("GEMINI_API_KEY not found in environment or .env file.")

    client = genai.Client(api_key=api_key)
    system_instruction = get_system_instruction()

    user_content = prompt
    if context_file:
        context_path = Path(context_file)
        if context_path.exists():
            file_content = context_path.read_text(encoding="utf-8")
            user_content = f"Context file: {context_path.name}\n```\n{file_content}\n```\n\n{prompt}"
        else:
            print(f"Warning: Context file '{context_file}' not found.")

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        config=gentypes.GenerateContentConfig(system_instruction=system_instruction),
        contents=user_content,
    )

    return response.text.strip()


def save_to_inbox(prompt: str, response: str):
    """Saves the output to the Notion Raw Ideas Database."""
    if not HAS_NOTION:
        print("notion-client not installed. Skipping Notion save. (pip install notion-client)")
        return

    notion_api_key = os.environ.get("NOTION_API_KEY")
    db_id = os.environ.get("NOTION_RAW_IDEAS_DB_ID")

    if not notion_api_key or not db_id:
        print("Notion credentials missing in .env. Skipping Notion save.")
        return

    notion = NotionClient(auth=notion_api_key)
    idea_title = prompt[:97] + "..." if len(prompt) > 100 else prompt
    
    # Chunk text to fit Notion's maximum 2000 character limit per text block
    chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
    children = []
    for chunk in chunks[:100]:  # Max 100 blocks per request
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": chunk}}]
            }
        })

    try:
        notion.pages.create(
            parent={"database_id": db_id},
            properties={
                "Idea": {"title": [{"type": "text", "text": {"content": idea_title}}]},
                "Status": {"select": {"name": "Raw"}},
                "Format": {"select": {"name": "Not Sure Yet"}},
                "Source": {"select": {"name": "Random"}}
            },
            children=children
        )
    except Exception as e:
        print(f"Failed to save to Notion: {e}")


def main():
    parser = argparse.ArgumentParser(description="ai_compose.py — Gemini for composing content ideas")
    parser.add_argument("prompt", nargs="?", help="The prompt for generating content")
    parser.add_argument("--file", help="Optional path to a context file")
    args = parser.parse_args()

    if args.prompt:
        print("\n🟢 Gemini (compose)\n" + "─" * 50)
        try:
            response = ask(args.prompt, args.file)
            print(response)
            print("─" * 50)
            save_to_inbox(args.prompt, response)
            print("📝 Saved to Raw Ideas Inbox\n")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        # Start interactive mode when no prompt is provided
        os.system(f"python -c 'import sys; from tools.ai_compose import interactive; interactive()' "
                  f"|| echo 'Interactive mode requires standard terminal input.'")
        print("Please provide a prompt to use this script via CLI, e.g., \n  python tools/ai_compose.py \"Your idea here\"")

if __name__ == "__main__":
    main()