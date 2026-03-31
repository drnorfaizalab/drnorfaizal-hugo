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
cd ai-router
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
your-project/
├── ai-router/
│   ├── ai-router.js      ← main router
│   ├── package.json
│   ├── .env.example
│   └── .env              ← your keys (gitignored)
├── .vscode/
│   └── tasks.json        ← copy from .vscode-tasks.json
└── src/                  ← your website files
```

---

## Add to .gitignore

```
ai-router/.env
node_modules/
```
