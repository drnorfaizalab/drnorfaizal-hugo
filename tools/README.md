# AI Tools — drnorfaizal.com

Two CLI tools for code assistance and content automation.

## Setup

```bash
cd tools/
npm install
```

Add a `.env` file in the project root (`drnorfaizal-hugo/`):

```env
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=AIza...
NOTION_API_KEY=secret_...
NOTION_CURATOR_PAGE_ID=<page-id>
```

---

## ai-router.js

Routes prompts to Claude (code) or Gemini (content) based on keyword detection.

**Models:** Claude Sonnet 4 · Gemini 1.5 Pro

```bash
# Auto-detect
node ai-router.js "fix the nav menu bug"
node ai-router.js "write a TikTok hook about spine surgery"

# Force agent
node ai-router.js --claude "refactor this function" --file path/to/file.js
node ai-router.js --gemini "translate this caption to Bahasa Malaysia"

# Interactive mode
node ai-router.js
```

**Routing logic:**
- Code keywords (`fix`, `debug`, `deploy`, `html`, `api`, …) → Claude
- Content keywords (`write`, `caption`, `translate`, `tiktok`, …) → Gemini
- Ambiguous → prompts you to add `--claude` or `--gemini`

---

## curator.js

Generates daily or weekly social media content briefs using Gemini and posts them to Notion.

**Model:** Gemini 2.5 Pro

```bash
# Generate and post to Notion
node curator.js daily
node curator.js weekly

# Preview without posting
node curator.js daily --dry-run
node curator.js weekly --dry-run
```

**Daily brief includes:**
- TikTok/Reel hook (Bahasa Malaysia)
- Instagram caption (English, 150–200 words)
- LinkedIn post idea
- Story/quote for Instagram or Facebook Stories

**Weekly plan includes:**
- Day-by-day themes (Mon–Sun)
- TikTok/Reel concept per day
- Instagram post topic
- LinkedIn angle

Output is posted as a new child page under `NOTION_CURATOR_PAGE_ID`.

---

## npm scripts

```bash
npm run curate:daily          # Post daily brief to Notion
npm run curate:weekly         # Post weekly plan to Notion
npm run curate:daily:dry      # Dry run — print only
npm run curate:weekly:dry     # Dry run — print only
```
