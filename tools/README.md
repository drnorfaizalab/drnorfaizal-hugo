# Tools — drnorfaizal.com

Content automation for the site. All generative tasks use Gemini (`gemini-2.5-pro`). Run every command from the project root (`drnorfaizal-hugo/`).

## Setup

```bash
pip install google-genai python-dotenv pyyaml   # Python tools
cd tools && npm install && cd ..                # Node tools
```

Copy `.env.example` to `.env` in the project root and fill in:

| Key | Used by |
|---|---|
| `GEMINI_API_KEY` | all generative tools |
| `NOTION_API_KEY` | `atomise.js`, `ai-compose.js`, `ai-curate.js` |
| `NOTION_RAW_IDEAS_DB_ID` | `atomise.js`, `ai-compose.js` |
| `NOTION_CURATOR_PAGE_ID` | `ai-curate.js` (the AI Curator Briefings page) |
| `INDEXNOW_KEY` | `indexnow_submit.py` (must match the key file in `static/`) |

`.env` is gitignored. Never commit it — this repo is public.

## Tools

| Tool | What it does | Output | Guide |
|---|---|---|---|
| `new_insight.py` | Draft → bilingual insight post | `content/insights/<slug>/index.en.md` + `index.ms.md` | `docs/new-insight.md` |
| `translate_content.py` | Translate one Hugo Markdown file EN ↔ BM | `index.en.md` → `index.ms.md` and back (overwrites) | — |
| `translate_testimonials.py` | Fill missing `ms` fields | `data/testimonials.yaml` | `docs/translate-testimonials.md` |
| `indexnow_submit.py` | Notify Bing/Yandex of new or updated URLs | IndexNow API | — |
| `atomise.js` | Post or topic → 5 social pieces (TikTok, IG, LinkedIn, FB, WhatsApp) | Notion Raw Ideas Inbox, one entry each | `docs/atomise.md` |
| `ai-compose.js` | Ad-hoc Gemini writing | Terminal + Notion Raw Ideas Inbox | below |
| `ai-curate.js` | Daily or weekly content brief | New sub-page under Notion AI Curator Briefings | below |
| `brand-context.md` | Shared brand voice | Read by `translate_content.py` | — |

## Commands

### New insight post
```bash
python tools/new_insight.py <slug>       # 1st run: creates draft.yaml — fill it in
python tools/new_insight.py <slug>       # 2nd run: Gemini writes index.en.md + index.ms.md
```

### Translate
```bash
python tools/translate_content.py content/<path>/index.en.md
python tools/translate_testimonials.py
```

### After publishing
```bash
python tools/indexnow_submit.py /insights/<slug>/ /ms/insights/<bm-slug>/
node tools/atomise.js content/insights/<slug>/index.en.md
node tools/atomise.js "when to see a neurosurgeon for chronic headache"   # topic only, no post
```

### Ideas and briefs
```bash
node tools/ai-compose.js "write a TikTok hook about spine surgery"
node tools/ai-compose.js "rewrite this in BM" --file path/to/file.md
node tools/ai-compose.js                    # interactive
node tools/ai-curate.js daily               # or: weekly
node tools/ai-curate.js daily --dry-run     # print only, nothing saved
```

npm shortcuts (run inside `tools/`): `npm run compose`, `npm run curate:daily`, `npm run curate:weekly`, `npm run curate:daily:dry`, `npm run curate:weekly:dry`.

## Deploy

No deploy script. Push to `main` and Cloudflare Pages builds and publishes in about a minute. Build-check first with `hugo --gc --minify -d "$TEMP/check"`. If a change doesn't show, purge the cache in Cloudflare (Caching → Configuration → Purge Everything).

## Notes

- `translate_content.py` overwrites the target file if it exists — commit or back up the other language first.
- Atomiser and compose entries are not de-duplicated — re-running creates new Notion entries.
