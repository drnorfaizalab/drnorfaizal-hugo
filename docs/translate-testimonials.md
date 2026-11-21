# Script: translate_testimonials.py

**File:** `tools/translate_testimonials.py`
**Purpose:** Fill missing Bahasa Malaysia (`ms`) fields in `data/testimonials.yaml` using Gemini.

---

## How to Run

```bash
python tools/translate_testimonials.py
```

Run from the project root (`drnorfaizal-hugo/`).

---

## What It Does

1. Opens `data/testimonials.yaml`
2. Finds every entry with an `en` field but no `ms` field
3. Translates `en` → modern conversational Bahasa Malaysia via Gemini (`gemini-2.5-pro`)
4. Writes `ms` back into the YAML
5. Skips entries that already have `ms` — safe to re-run

---

## Requirements

```bash
pip install google-genai python-dotenv pyyaml
```

`.env` (project root): `GEMINI_API_KEY=...`

---

## Adding a New Testimonial

Add an entry with only `en`:

```yaml
- name: Patient Name
  en: Their review text in English.
  stars: 5
```

Then run the script. The homepage carousel picks up the new entry automatically.

## testimonials.yaml Structure

```yaml
- name: ""    # display name on the card
  en: ""      # English review
  ms: ""      # Bahasa Malaysia (auto-filled)
  stars: 5    # 1–5
```

---

## Notes

- The script rewrites the whole YAML file (`yaml.dump`), so formatting and line wrapping may change — check the diff.
- It never overwrites an existing `ms` field.
- Always skim the BM output for tone and accuracy before committing.
- Get consent before publishing any testimonial; don't add identifying clinical details.
