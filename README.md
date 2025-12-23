# CAIS 2026 Website

The official website for **CAIS 2026 — ACM Conference on Agentic and AI Systems**.

Built with [Eleventy (11ty)](https://www.11ty.dev/) for maintainability and ease of content updates.

## Quick Start

```bash
# Install dependencies
npm install

# Run development server with live reload
npm run dev

# Build for production
npm run build
```

The development server runs at `http://localhost:8080` by default.

## Project Structure

```
CAIS-Website/
├── src/                      # Source files (11ty processes these)
│   ├── _data/                # Global data files (JSON)
│   │   ├── site.json         # Site config (dates, URLs, contact info)
│   │   ├── navigation.json   # Navigation menus
│   │   ├── committee.json    # Committee member data
│   │   └── pillars.json      # "What is CAIS" pillar content
│   ├── _includes/            # Reusable components
│   │   ├── layouts/          # Page layouts
│   │   │   └── base.njk      # Base HTML template
│   │   ├── nav.njk           # Navigation partial
│   │   ├── footer.njk        # Footer partial
│   │   ├── committee-card.njk
│   │   ├── committee-thumbnail.njk
│   │   └── pillar-card.njk
│   ├── assets/               # Static assets (copied as-is)
│   │   ├── css/styles.css    # Main stylesheet
│   │   ├── js/               # JavaScript files
│   │   └── images/           # Images
│   ├── pages/                # Content pages
│   │   ├── committee.njk
│   │   ├── workshops.njk
│   │   ├── codeofconduct.njk
│   │   └── ...
│   └── index.njk             # Homepage
├── _site/                    # Build output (gitignored)
├── .eleventy.js              # 11ty configuration
├── package.json
└── README.md
```

## Common Tasks

### Updating Conference Dates

Edit `src/_data/site.json`:

```json
{
  "dates": {
    "start": "2026-05-26",
    "end": "2026-05-29",
    "display": "May 26–29, 2026"
  },
  "deadlines": {
    "paperSubmission": {
      "date": "2026-02-27",
      "display": "February 27, 2026"
    }
  }
}
```

### Adding a Committee Member

Edit `src/_data/committee.json`. Add to either `steering` or `organizing` array:

```json
{
  "name": "Jane Doe",
  "affiliation": "University",
  "photo": "doe_jane.png",
  "role": "Program Chair",  // optional, for organizing committee
  "bio": "Bio text here..."
}
```

Then add their photo to `src/assets/images/`.

### Adding a New Page

1. Create `src/pages/your-page.njk`
2. Add frontmatter:

```yaml
---
layout: base.njk
title: Page Title
description: Page description for SEO
permalink: /pages/your-page/
---

<!-- Your page content here -->
```

3. Optionally add to navigation in `src/_data/navigation.json`

### Updating Navigation

Edit `src/_data/navigation.json`:

```json
{
  "main": [
    { "label": "What is CAIS", "href": "/#why" },
    { "label": "New Page", "href": "/pages/new-page/" }
  ]
}
```

## Design System

### Colors (defined in styles.css)

| Variable | Color | Usage |
|----------|-------|-------|
| `--terracotta-deep` | #B8593E | Primary accent (20-25%) |
| `--olive-moss` | #6B7F5A | Secondary accent |
| `--seasalt` | #FAFAF8 | Background white |
| `--eerie-black` | #252523 | Text color |
| `--platinum` | #e8e7e7 | Light backgrounds |

### CSS Classes

- `.hero` - Hero section with gradient background
- `.section-title` - Section headings
- `.card-quiet` - Standard card component
- `.highlight-box` - Highlighted content box
- `.cta-band` - Call-to-action banner
- `.btn-primary`, `.btn-outline-primary` - Button styles

## Deployment

The `npm run build` command outputs static files to `_site/`. Deploy this folder to any static hosting:

- **GitHub Pages**: Push `_site/` contents to `gh-pages` branch
- **Vercel/Netlify**: Connect repo and set build command to `npm run build`
- **Manual**: Upload `_site/` contents to your web server

## Legacy Files

The original static HTML files are still in the root directory (`index.html`, `pages/`). These can be removed once the 11ty migration is complete and tested.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on making changes to the site.
