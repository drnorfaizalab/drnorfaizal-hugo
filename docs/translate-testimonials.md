# Script: translate_testimonials.py

**File:** `scripts/translate_testimonials.py`
**Purpose:** Auto-translate missing Bahasa Malaysia (`bm`) fields in `data/testimonials.yaml` using the Claude API.

---

## How to Run

```bash
python scripts/translate_testimonials.py
```

Run from the project root (`drnorfaizal-hugo/`).

---

## What It Does

1. Opens `data/testimonials.yaml`
2. Scans every entry for a missing `bm` field
3. Translates the `en` field from English → Bahasa Malaysia via Claude
4. Writes the translated `bm` field back into the YAML file
5. Skips entries that already have a `bm` value — safe to re-run

---

## Requirements

```bash
pip install anthropic python-dotenv pyyaml
```

Add your API key to `.env` at the project root:

```env
ANTHROPIC_API_KEY=sk-ant-...
```

---

## Adding a New Testimonial

Edit `data/testimonials.yaml` and add a new entry with only the `en` field:

```yaml
- name: Patient Name
  en: Their review text in English.
  stars: 5
```

Then run the script to auto-generate the `bm` field:

```bash
python scripts/translate_testimonials.py
# Translating: Patient Name...
# Done. 1 translation(s) added to data/testimonials.yaml
```

The carousel on the homepage will pick up the new entry automatically.

---

## testimonials.yaml Structure

```yaml
- name: ""          # Display name on the card
  en: ""            # English version of the review
  bm: ""            # Bahasa Malaysia version (auto-filled by this script)
  stars: 5          # Star rating — used to render ★ icons (1–5)
```

---

## Notes

- Claude translates in modern, conversational Bahasa — not formal government language.
- Medical terms without a natural Bahasa equivalent are kept in English.
- The script never overwrites an existing `bm` field, so manual translations are safe.
- Always skim the translated `bm` text after running — review for tone and accuracy.
