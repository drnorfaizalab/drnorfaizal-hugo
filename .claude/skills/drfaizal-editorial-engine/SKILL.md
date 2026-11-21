---
name: drfaizal-editorial-engine
description: Drafts, translates, and audits bilingual (English + Bahasa Malaysia) clinical education content for Dr Nor Faizal Ahmad Bahuri — Hugo insight posts for drnorfaizal.com, 60–90 s vertical video scripts for @drnorfaizalbahuri, social atomisation, and patient handouts. Use when turning voice memos, clinical notes, or rough ideas into publish-ready insights, TikTok/Reels/Shorts scripts, or patient education summaries.
---

# Dr Faizal Editorial Engine

Turns rough clinical notes, voice memos, or a topic into publish-ready bilingual content in Dr Faizal's voice, aligned with the neurooncology pivot.

## When to use
- Voice dump or notes → paired EN + BM Hugo insight post for `drnorfaizal.com`
- 60–90 s vertical video script (TikTok, IG Reels, YouTube Shorts) — BM by default
- Atomising an insight into TikTok / IG / LinkedIn / FB / WhatsApp pieces
- Patient handout or clinical audit summary
- EN ↔ BM adaptation without losing clinical precision or warmth

## Steps

### 1. Classify the deliverable
1. **Hugo insight post** — page bundle `content/insights/<slug>/index.en.md` + `index.ms.md`
2. **Vertical video script** — hook, spoken script, on-screen text, B-roll cues
3. **Social atomisation** — per-platform pieces from one source
4. **Handout / audit brief** — scannable, one page

### 2. Load the toolbox
- [tools/brand-voice.md](tools/brand-voice.md) — identity, voice, banned phrases, bilingual rules
- [tools/hugo-template.md](tools/hugo-template.md) — bundle layout, front matter, shortcodes, slugs
- [tools/video-hooks.md](tools/video-hooks.md) — hook formulas, script skeleton, pacing

### 3. Draft (80/20)
- **Open concrete:** a real patient dilemma, a myth, or a sharp clinical moment. No greetings, no textbook definitions.
- **80/20:** only the 20% of anatomy/procedure that drives 80% of understanding and action.
- **Adapt, don't translate:** BM for warmth and reach, EN for crisp Oxford-trained authority. Rewrite idioms and explanations per language.
- **Close calmly:** red flags and when to see a specialist. CTA only as requested (default: appointment).
- **Pivot alignment:** where the topic allows, link to the neurooncology pages (`/expertise/neurooncology/`, `/expertise/glioma-glioblastoma/`, `/expertise/meningioma/`, `/expertise/brain-tumour-malaysia/`, `/expertise/paediatric-brain-tumour/`).

### 4. Proof checklist (fix before output)
- [ ] No placeholders (`[Topic]`, `TBD`, empty `""` fields)
- [ ] Every technical term explained in plain language on first use
- [ ] Human-first voice; zero banned phrases (see brand-voice.md)
- [ ] Bilingual parity: both files complete, same `date`, `slug`, `translationKey`, `image`, `youtube_id`; localised `title`, `description`, `tags`, `categories`, `keywords`, `faq_schema`
- [ ] Clinically accurate; framed as public education, not individual diagnosis
- [ ] No identifiable patient details (name, IC, face, date + location combinations) without documented consent
- [ ] No outcome guarantees, no superlatives ("best", "No.1"), no before/after claims — MMC / Medicine Advertisements Board compliant

## Gotchas
- Never sound like a hospital brochure.
- BM is modern conversational Malaysian ("educated friend"), not formal government BM, and not Indonesian spelling.
- Scripts must be speakable in 60–90 s without rushing (~140–160 words BM, ~150–180 words EN).
- New posts default to `draft: true`; Dr Faizal flips to `false` after review.
