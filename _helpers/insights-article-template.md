# Insights Article Template

Reference for writing new articles under `content/insights/`.

---

## Filter Category Routing

The Insights page filters (Brain · Head · Pain · Story) are assigned **automatically** based on keywords found in `categories` and `tags`. Use the table below to target the right filter.

| Filter | Keywords to include in `categories` or `tags` |
|--------|------------------------------------------------|
| **Brain** | `Neurooncology`, `Brain Tumours`, `Brain Cancer`, `GBM`, `Glioblastoma`, `Meningioma` |
| **Head** | `Migraine`, `Headache`, `Cluster Headache`, `Trigeminal`, `Facial Pain` |
| **Pain** | `Pain Management`, `Spinal`, `Neuropathic Pain`, `Back Pain`, `Chronic Pain` |
| **Story** | `Personal`, `Philosophy`, `Oxford`, `Mindset`, `Behind the Scenes` |

> If no keyword matches, the article defaults to **Brain**.

---

## Front Matter Fields

### Required
```yaml
title: ""          # Article headline
description: ""    # One sentence — shown on card and used for SEO meta
date: YYYY-MM-DD
draft: false
```

### Recommended
```yaml
categories: []     # See filter table above — drives the filter tab
tags: []           # More specific keywords — also used for SEO and routing
image: ""          # Card thumbnail path e.g. /images/blog/filename.jpg
                   # Drop the image file into static/images/blog/
```

### Optional
```yaml
social_platform: "" # "tiktok" | "youtube" | "instagram"
                    # Shows platform badge on the card
pdf_available: true # Shows a PDF badge on the card
```

---

## Templates

### Clinical Article
```yaml
---
title: ""
description: ""
date: YYYY-MM-DD
draft: false
categories: ["Neurooncology", "Brain Tumours"]
tags: ["", "neurosurgery"]
image: "/images/blog/filename.jpg"
---
```

### Headache / Migraine Article
```yaml
---
title: ""
description: ""
date: YYYY-MM-DD
draft: false
categories: ["Headache & Migraine", "Neurology"]
tags: ["migraine", "headache", ""]
image: "/images/blog/filename.jpg"
---
```

### Pain Management Article
```yaml
---
title: ""
description: ""
date: YYYY-MM-DD
draft: false
categories: ["Pain Management"]
tags: ["spinal", "neuropathic pain", ""]
image: "/images/blog/filename.jpg"
---
```

### Social Media Post
```yaml
---
title: ""
description: ""
date: YYYY-MM-DD
draft: false
social_platform: "tiktok"   # tiktok | youtube | instagram
categories: [""]
tags: [""]
---
```

### Personal Story
```yaml
---
title: ""
description: ""
date: YYYY-MM-DD
draft: false
categories: ["Personal"]
tags: ["mindset", "Oxford", "neurosurgery"]
---
```

---

## File Naming Convention

```
content/insights/your-article-slug/
├── index.en.md     # English version
└── index.bm.md     # Bahasa Malaysia version (optional)
```

- Use lowercase, hyphen-separated slugs
- Keep it short and descriptive: `glioblastoma-treatment-options`, `migraine-red-flags`
- Slug becomes the URL: `drnorfaizal.com/insights/your-article-slug/`

---

## Image Checklist

- [ ] File saved to `static/images/blog/filename.jpg`
- [ ] Recommended size: 1200 × 630 px (OG image ratio)
- [ ] Referenced in front matter as `image: "/images/blog/filename.jpg"`
