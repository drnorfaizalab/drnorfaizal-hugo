# AI Router — drnorfaizal.com

Routes tasks between two AI specialists:

| Agent | Role | Triggers |
|-------|------|----------|
| 🔵 Claude | Code, backend, website, debugging | fix, build, html, css, js, deploy... |
| 🟢 Gemini | Content, captions, BM/EN, social | write, caption, translate, tiktok... |

---

## Setup

```bash
# 1. Install dependencies
cd tools
npm install

# 2. Set your API keys
cp .env.example .env
# Edit .env with your actual keys

# 3. Load env vars (add to your shell profile)
export ANTHROPIC_API_KEY=your_key
export GEMINI_API_KEY=your_key
```

---

## Usage

### Interactive mode
```bash
node ai-router.js
```

### Direct CLI
```bash
# Auto-detect agent
node ai-router.js "fix the navigation bug in index.html"
node ai-router.js "write a TikTok caption about spine surgery in BM"

# Force agent
node ai-router.js --claude "refactor the contact form"
node ai-router.js --gemini "translate this post to Bahasa Malaysia"

# With file context
node ai-router.js --claude "review this code" --file src/index.js
node ai-router.js --gemini "rewrite this in Dr Faizal's voice" --file drafts/post.md
```

### VS Code Tasks (Ctrl+Shift+P → Run Task)
- 🤖 AI Router (interactive)
- 🔵 Claude — Code task
- 🟢 Gemini — Content task
- 🟢 Gemini — Content with file (uses currently open file)

---

## Project Structure

```
drnorfaizal-hugo/
├── tools/
│   ├── ai-code.js
│   ├── ai-compose.js
│   ├── ai-curate.js
│   ├── new_insight.py
│   ├── new_insight.sh
│   ├── translate_testimonials.py
│   ├── deploy.sh
│   ├── quick-start.sh
│   ├── package.json
│   └── .env              ← your keys (gitignored)
└── content/              ← Hugo site content
```

---

## Add to .gitignore

```
tools/.env
node_modules/
```
