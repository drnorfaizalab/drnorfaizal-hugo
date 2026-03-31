# AI Tools — drnorfaizal.com

Three focused CLI tools — each with a single AI and a single purpose.

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
NOTION_RAW_IDEAS_DB_ID=<database-id>
```

---

## ai-code.js

Claude for code troubleshooting — debug, refactor, review.

**Model:** Claude Sonnet 4

```bash
# Direct mode
node ai-code.js "fix the nav menu bug"
node ai-code.js "refactor this function" --file path/to/file.js

# Interactive mode
node ai-code.js
```

---

## ai-compose.js

Gemini for composing content ideas. All output is automatically saved to the **Raw Ideas Inbox** in Notion.

**Model:** Gemini 2.5 Pro

```bash
# Direct mode
node ai-compose.js "write a TikTok hook about spine surgery"
node ai-compose.js "translate this caption to Bahasa Malaysia" --file caption.md

# Interactive mode
node ai-compose.js
```

---

## ai-curate.js

Gemini generates structured daily or weekly content briefs and posts them to Notion (AI Curator Briefings).

**Model:** Gemini 2.5 Pro

```bash
# Generate and post to Notion
node ai-curate.js daily
node ai-curate.js weekly

# Preview without posting
node ai-curate.js daily --dry-run
node ai-curate.js weekly --dry-run
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

---

## npm scripts

```bash
npm run code                  # Interactive Claude code session
npm run compose               # Interactive Gemini compose session
npm run curate:daily          # Post daily brief to Notion
npm run curate:weekly         # Post weekly plan to Notion
npm run curate:daily:dry      # Dry run — print only
npm run curate:weekly:dry     # Dry run — print only
```
