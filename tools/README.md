# Tools — drnorfaizal.com

Content automation for the site. All generative tasks use Gemini (`gemini-2.5-pro`).

## Setup

```bash
pip install google-genai python-dotenv pyyaml   # Python tools
cd tools && npm install                         # Node tools
```

Copy `.env.example` to `.env` in the project root (`drnorfaizal-hugo/`) and fill in the keys.

## Tools

| Tool | What it does | Guide |
|---|---|---|
| `new_insight.py` | Draft → bilingual insight post (EN + BM) | `docs/new-insight.md` |
| `translate_content.py` | Translate one Hugo Markdown file EN ↔ BM | — |
| `translate_testimonials.py` | Fill missing BM in `data/testimonials.yaml` | `docs/translate-testimonials.md` |
| `indexnow_submit.py` | Notify Bing/Yandex of new or updated URLs | — |
| `atomise.js` | One post or topic → 5 social pieces → Notion Raw Ideas Inbox | `docs/atomise.md` |
| `ai-compose.js` | Ad-hoc Gemini writing → Notion Raw Ideas Inbox | below |
| `ai-curate.js` | Daily/weekly content brief → Notion AI Curator Briefings | below |
| `brand-context.md` | Shared brand voice, read by `translate_content.py` | — |

## Quick commands

```bash
python tools/new_insight.py <slug>                          # create draft, then run again to generate
python tools/translate_content.py content/insights/<slug>/index.en.md
python tools/translate_testimonials.py
python tools/indexnow_submit.py /insights/<slug>/ /ms/insights/<bm-slug>/
node tools/atomise.js content/insights/<slug>/index.en.md
node tools/ai-compose.js "write a TikTok hook about spine surgery"
node tools/ai-curate.js daily          # or: weekly, --dry-run
```

npm shortcuts (from `tools/`): `npm run compose`, `npm run curate:daily`, `npm run curate:weekly`, `npm run curate:daily:dry`, `npm run curate:weekly:dry`.

## Deploy

No deploy script. Push to `main` and Cloudflare Pages builds and publishes in about a minute. If a change doesn't show, purge the cache in Cloudflare (Caching → Configuration → Purge Everything).
