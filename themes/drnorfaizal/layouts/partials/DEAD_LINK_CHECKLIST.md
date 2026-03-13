# Link Verification Checklist

Use this checklist to verify that all referenced pages exist and external links are correct.

## 🔴 High Priority (Likely Missing Content)
These links are hardcoded in `footer.html` but the content files likely do not exist yet.

- [ ] **FAQ Page**
  - **Link:** `/patients/faq/`
  - **Action:** Create `content/patients/faq/_index.md`

- [ ] **Symptom Checklist**
  - **Link:** `/patients/symptom-checklist/`
  - **Action:** Create `content/patients/symptom-checklist/_index.md`

## 🟠 Main Navigation (Verify Content Exists)
These are defined in `hugo.toml` menus. Ensure the corresponding `_index.md` files exist.

- [ ] **About Page** (`/about/`) -> `content/about/_index.md`
- [ ] **Specialties Section** (`/expertise/`) -> `content/kepakaran/_index.md`
- [ ] **Patients Section** (`/patients/`) -> `content/pesakit/_index.md`
- [ ] **For Doctors** (`/for-doctors/`) -> `content/for-doctors/_index.md`
- [ ] **Contact Page** (`/contact/`) -> `content/contact/_index.md`

## 🔵 External Links (Manual Check)
Click these to ensure they open the correct profiles.

- [ ] **Booking/Profile:** https://www.kpjhealth.com.my/dr-nor-faizal-ahmad-bahuri

### Social Media (Configured in `hugo.toml`)
Check if these handles are correct:
- [ ] **Instagram:** `drnorfaizalbahuri` -> https://instagram.com/drnorfaizalbahuri
- [ ] **TikTok:** `drnorfaizalbahuri` -> https://tiktok.com/@drnorfaizalbahuri
- [ ] **YouTube:** `drnorfaizalbahuri` -> https://youtube.com/@drnorfaizalbahuri
- [ ] **LinkedIn:** `drnorfaizalbahuri` -> https://linkedin.com/in/drnorfaizalbahuri
- [ ] **Facebook:** `drnorfaizalbahuri` -> https://facebook.com/drnorfaizalbahuri

## 🟢 Functional Links
- [ ] **WhatsApp (General):** `+60122895061` (Test button in bottom right)
- [ ] **WhatsApp (Referral):** (Test button on "For Doctors" page)
- [ ] **Phone:** `+603-4026 7777 ext 5099` (Test `tel:` link)
- [ ] **Email:** `drnfaizal@kpjtawakkal.com` (Test `mailto:` link)

