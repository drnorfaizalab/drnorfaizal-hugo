# Hugo Insight Template — drnorfaizal.com

Matches `archetypes/insights.md` and existing posts (e.g. `content/insights/craniotomy-explained/`).

## Bundle layout
```
content/insights/<slug>/
├── index.en.md    # English
├── index.ms.md    # Bahasa Malaysia
└── *.jpg/png      # optional page resources
```
- Permalink: `/insights/:slug/` (EN) and `/ms/insights/:slug/` (BM).
- `<slug>`: lowercase, hyphenated, English keyword-led (`glioblastoma-treatment-options`). BM-first topics may use a BM slug (`jatuh-pendarahan-otak`) — same folder for both languages.
- Set the same `slug` and `translationKey` in both files.
- Shared images: `static/images/insights/<slug>.jpg`; fallback `/images/insights/insights-default.jpg`.

## English — `index.en.md`
```yaml
---
title: "How Is Brain Surgery Actually Performed? Inside a Craniotomy"
date: 2026-11-21T09:00:00+08:00
draft: true
type: "blog"
slug: "craniotomy-explained"
translationKey: "craniotomy-explained"
author: "Dr Nor Faizal Ahmad Bahuri"
categories: ["Neurooncology", "Patient Education"]
tags: ["craniotomy", "brain-surgery", "neurosurgery", "patient-education"]
description: "One sentence, 140–160 characters, for search and social previews."
image: "/images/insights/insights-default.jpg"
keywords: ["craniotomy explained Malaysia", "brain tumour surgery Malaysia", "neurosurgeon Kuala Lumpur"]
seo:
  focusKeyword: "how brain surgery is performed"
show_appointment_button: true
youtube_id: ""            # omit if no video
cta:
  type: appointment       # appointment | whatsapp | download | none
  label: "Book a Consultation"
  url: "/contact"
faq_schema:               # 3–5 Q&As, renders FAQPage JSON-LD
  - question: "What is a craniotomy?"
    answer: "Plain-language answer, 2–3 sentences."
---
```

## Bahasa Malaysia — `index.ms.md`
```yaml
---
title: "Bagaimana Pembedahan Otak Sebenarnya Dilakukan? Di Sebalik Kraniotomi"
seoTitle: "Kraniotomi: Bagaimana Pembedahan Otak Dilakukan"   # optional, shorter
date: 2026-11-21T09:00:00+08:00
draft: true
type: "blog"
slug: "craniotomy-explained"
translationKey: "craniotomy-explained"
author: "Dr Nor Faizal Ahmad Bahuri"
categories: ["Neuro-onkologi", "Pendidikan Pesakit"]
tags: ["kraniotomi", "pembedahan-otak", "bedah-saraf", "pendidikan-pesakit"]
description: "Satu ayat, 140–160 aksara, untuk pratonton carian dan media sosial."
image: "/images/insights/insights-default.jpg"
keywords: ["kraniotomi Malaysia", "pembedahan tumor otak Malaysia", "pakar bedah saraf Kuala Lumpur"]
seo:
  focusKeyword: "bagaimana pembedahan otak dilakukan"
show_appointment_button: true
youtube_id: ""
cta:
  type: appointment
  label: "Buat Janji Temu"
  url: "/contact"
faq_schema:
  - question: "Apakah itu kraniotomi?"
    answer: "Jawapan ringkas dalam bahasa mudah, 2–3 ayat."
---
```

## Category pairs (use these, keep consistent)
| EN | BM |
|---|---|
| Neurooncology | Neuro-onkologi |
| Brain Tumours | Tumor Otak |
| Paediatric Neurosurgery | Bedah Saraf Kanak-kanak |
| Headache & Migraine | Sakit Kepala & Migrain |
| Facial Pain | Sakit Muka |
| Pain Management | Pengurusan Kesakitan |
| Spine | Tulang Belakang |
| Head Injury | Kecederaan Kepala |
| Brain Haemorrhage | Pendarahan Otak |
| Patient Education | Pendidikan Pesakit |
| Behind the Scenes | Di Sebalik Tabir |
| Personal / Reflections | Peribadi / Refleksi |

Tags: 4–6, lowercase-hyphenated, include one location tag (`malaysia`) where relevant.

## Body
- 400–700 words, story-led, `##` subheadings, no bullet dumps.
- Shortcodes available:
  - `{{< youtube "VIDEO_ID" >}}`
  - `{{< tiktok "VIDEO_ID" >}}`
  - `{{< instagram "POST_ID" >}}`
  - `{{< cta type="appointment" label="Book a Consultation" url="/contact" >}}` (`relLangURL` adds `/ms/` automatically)
- Internal links: relative (`/expertise/neurooncology/`) — Hugo localises per language.
- End with red flags / when to seek review, then the CTA.

## Create
```bash
hugo new content insights/<slug>/index.en.md
hugo new content insights/<slug>/index.ms.md
```
or `python tools/new_insight.py` (Gemini pipeline).
