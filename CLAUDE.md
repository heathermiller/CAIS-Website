# CAIS Website - Guide for Claude

This is the website for CAIS 2026 (ACM Conference on AI and Agentic Systems). It uses [Eleventy (11ty)](https://www.11ty.dev/) as a static site generator.

## Before Making Any Changes

**Always start the local dev server first:**
```bash
npm run dev
```
This runs at http://localhost:8080 (or 8081 if 8080 is busy) and auto-reloads when you make changes. Keep it running while you work so you can verify changes look correct.

## Project Structure

```
src/
├── _data/           # JSON data files (the "CMS")
│   ├── site.json    # Core site info: dates, location, venue, emails, deadlines
│   ├── committee.json   # Steering and organizing committee members
│   ├── navigation.json  # Navigation menus
│   └── pillars.json     # "What is CAIS?" section content
├── _includes/
│   ├── layouts/     # Page templates (base.njk is the main one)
│   └── *.njk        # Reusable components (nav, footer, cards)
├── pages/           # Individual pages (cfp, committee, workshops, etc.)
├── assets/
│   ├── css/         # Stylesheets
│   └── images/      # Images and logos
└── index.njk        # Homepage
```

## Common Tasks

### Update Conference Dates, Deadlines, or Location
Edit `src/_data/site.json`. Key fields:
- `dates` - Conference dates
- `deadlines` - Paper submission deadlines
- `location` - City/state
- `venue` - Hotel details and booking URL

### Update Contact Emails
Edit `src/_data/site.json` under `contact`:
- `email` - General contact
- `sponsorship` - Sponsorship inquiries
- `conduct` - Code of conduct reports

### Add/Edit Committee Members
Edit `src/_data/committee.json`. Each member has:
```json
{
  "name": "Full Name",
  "affiliation": "University or Company",
  "photo": "filename.png",  // Must exist in src/assets/images/
  "bio": "Bio text here...",
  "role": "Optional role like 'General Co-Chair'"  // Only for organizing committee
}
```
Photos should be placed in `src/assets/images/`.

### Add a New Page
1. Create a new `.njk` file in `src/pages/`, e.g., `src/pages/newpage.njk`
2. Use this template:
```njk
---
layout: base.njk
title: Page Title
description: Meta description for SEO
permalink: /pages/newpage/
---

<header class="hero">
    <div class="container">
        <h1 class="display-5 fw-bold mb-3">Page Heading</h1>
        <p class="lead mb-0">Subheading text</p>
    </div>
</header>

<section class="py-5">
    <div class="container">
        <!-- Your content here -->
    </div>
</section>
```
3. Add it to navigation in `src/_data/navigation.json` if needed

### Add a Call-to-Action (CTA) Button
Use this pattern:
```html
<a href="URL_HERE" class="btn btn-primary" style="background:var(--cais-accent); border:none; color:#fff;">
    <i class="bi bi-icon-name me-2"></i>Button Text
</a>
```
For multiple buttons together, use `align-items-center` to keep them vertically aligned:
```html
<div class="d-flex flex-wrap gap-3 align-items-center">
    <a href="#" class="btn btn-primary" style="background:var(--cais-accent); border:none; color:#fff;">
        <i class="bi bi-envelope me-2"></i>Primary Button
    </a>
    <a href="#" class="btn btn-outline-primary">
        <i class="bi bi-arrow-right me-2"></i>Secondary Button
    </a>
</div>
```
Find icon names at https://icons.getbootstrap.com/

### Edit Navigation Menus
Edit `src/_data/navigation.json`:
- `main` - Top navigation bar
- `footerAuthors` - Footer "For Authors" links
- `footerPolicies` - Footer "Policies" links

### Update the "What is CAIS?" Pillars
Edit `src/_data/pillars.json`. Each pillar has:
```json
{
  "title": "Pillar Title",
  "description": "Description text...",
  "image": "Pillars_filename.svg"  // Must exist in src/assets/images/
}
```

### Reorder Committee Members
The order in `src/_data/committee.json` determines display order. Simply cut and paste the entire member object (from `{` to `},`) to move them. Be careful to maintain valid JSON (commas between items, no trailing comma on last item).

### Add Sponsors
To add a sponsors section, you'll need to:
1. Add sponsor data to `src/_data/` (create `sponsors.json`):
```json
[
  {
    "name": "Company Name",
    "logo": "sponsor-logo.png",
    "url": "https://company.com",
    "tier": "gold"
  }
]
```
2. Add logos to `src/assets/images/`
3. Add a sponsors section to `src/index.njk` or create `src/pages/sponsors.njk`

### Add Workshop Entries
Edit `src/pages/workshops.njk`. Add a new workshop section:
```html
<section id="workshop-name" class="anchor mb-5">
    <h2 class="section-title h4 mb-3">Workshop Title</h2>
    <p><strong>Organizers:</strong> Name 1, Name 2</p>
    <p>Workshop description goes here...</p>
</section>
```

### Add an Announcement Banner
Add this right after `<main id="main">` in `src/_includes/layouts/base.njk` for site-wide, or at the top of a specific page:
```html
<div class="alert alert-warning text-center mb-0 rounded-0">
    <i class="bi bi-megaphone me-2"></i>
    <strong>Announcement:</strong> Registration is now open!
    <a href="/pages/register/" class="alert-link ms-2">Register now</a>
</div>
```
Use `alert-warning` (yellow), `alert-info` (blue), or `alert-success` (green).

### Add a New Section to an Existing Page
Use the standard section pattern:
```html
<section class="py-5">
    <div class="container">
        <h2 class="section-title mb-3">Section Title</h2>
        <p class="lead mb-4">Optional lead paragraph.</p>
        <!-- Content here -->
    </div>
</section>
```
Use `class="py-5 bg-light"` to alternate background colors between sections.

## Common UI Patterns

### Cards (for features, topics, etc.)
```html
<div class="row g-4">
    <div class="col-md-6 col-lg-3">
        <div class="card card-quiet p-3 h-100">
            <img src="/assets/images/icon.svg" class="rounded mb-3" alt="Description" loading="lazy" />
            <h3 class="h5 fw-bold">Card Title</h3>
            <p class="mb-0">Card description text.</p>
        </div>
    </div>
    <!-- More cards... -->
</div>
```

### Highlight Box (for important callouts)
```html
<div class="highlight-box p-4">
    <h3 class="h5 fw-bold mb-2">Callout Title</h3>
    <p class="mb-0">Important information here.</p>
</div>
```

### CTA Band (full-width call to action)
```html
<div class="cta-band p-4 p-lg-5 d-flex flex-column flex-lg-row align-items-lg-center justify-content-between gap-3">
    <div>
        <h2 class="h3 fw-bold mb-1">Heading Text</h2>
        <p class="mb-0">Supporting text.</p>
    </div>
    <div>
        <a class="btn btn-light btn-lg text-dark px-4" href="URL">
            <i class="bi bi-icon-name me-2"></i>Button Text
        </a>
    </div>
</div>
```

### Two-Column Layout
```html
<div class="row g-4">
    <div class="col-lg-8">
        <!-- Main content -->
    </div>
    <div class="col-lg-4">
        <!-- Sidebar -->
    </div>
</div>
```

### Table (for schedules, deadlines)
```html
<table class="table table-sm">
    <tbody>
        <tr>
            <td>Item name</td>
            <td class="text-end"><strong>Date or value</strong></td>
        </tr>
        <tr class="table-active">
            <td><strong>Highlighted row</strong></td>
            <td class="text-end"><strong>Important date</strong></td>
        </tr>
    </tbody>
</table>
```

### Alert Box (for warnings, notes)
```html
<div class="alert alert-warning mb-4">
    <i class="bi bi-info-circle me-2"></i>
    <strong>Note:</strong> Alert message here.
</div>
```

## Important Notes

- **Always preview changes locally** before committing
- **Don't edit SVG logo files directly** - they need to be updated in design software
- **The conference name is "ACM Conference on AI and Agentic Systems"** (AI comes before Agentic)
- **Emails are centralized in site.json** - don't hardcode emails in templates
- **Images go in `src/assets/images/`** - reference them as `/assets/images/filename.png`

## Build & Deploy

- `npm run dev` - Start local dev server with live reload
- `npm run build` - Build static site to `_site/` folder

## Styling

The site uses Bootstrap 5 with custom CSS variables defined in `src/assets/css/styles.css`:
- `--cais-accent` - Primary accent color (terracotta/coral)
- `--seasalt` - Light background color

Use Bootstrap classes for layout (containers, rows, cols) and spacing (py-5, mb-3, etc.).
