# Script: atomise.js

**File:** `tools/atomise.js`
**Purpose:** Break a long-form insight post (or topic brief) into 5 platform-ready atomic content pieces — saved individually to Raw Ideas Inbox in Notion.

---

## How to Run

```bash
# From a published insight post
node tools/atomise.js content/insights/my-slug/index.en.md

# From a topic brief (no file needed)
node tools/atomise.js "glioblastoma treatment journey"
```

Run from the project root (`drnorfaizal-hugo/`).

---

## What It Produces

One Notion entry per platform, tagged `Source: Atomiser`:

| Platform  | Language | Format              |
|-----------|----------|---------------------|
| TikTok    | BM       | Hook + 90-sec Script |
| Instagram | BM       | Caption + hashtags  |
| LinkedIn  | EN       | Professional post   |
| Facebook  | BM       | Patient-facing post |
| WhatsApp  | BM       | Broadcast message   |

Each piece is saved to **Raw Ideas Inbox** with Status `Raw` — move to the Content Calendar when ready to schedule.

---

## Workflow

### Typical: atomise after publishing a new insight

```bash
# 1. Generate the insight post
python tools/new_insight.py neurooncology-second-opinion

# 2. Publish
git add . && git commit -m "insight: neurooncology-second-opinion" && git push

# 3. Atomise for social
node tools/atomise.js content/insights/neurooncology-second-opinion/index.en.md
```

### Quick: atomise a topic without a post

```bash
node tools/atomise.js "when to see a neurosurgeon for chronic headache"
```

Gemini generates platform content from the topic alone — useful for planning week's social posts ahead of writing the full insight.

---

## Setup

No additional dependencies — uses the same packages as `ai-compose.js`.

```bash
npm install   # if not already done
```

Requires in `.env`:
```
GEMINI_API_KEY=...
NOTION_API_KEY=...
NOTION_RAW_IDEAS_DB_ID=...
```

---

## Notes

- If Gemini wraps its JSON in a code fence, the script strips it automatically.
- WhatsApp entries fall back to `Format: Not Sure Yet` in Notion (not a native Notion format option).
- Re-running on the same file creates new Notion entries — no deduplication.
- Content is output to the terminal as well, so you can copy directly without opening Notion.
