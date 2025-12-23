# Contributing to CAIS Website

This document provides guidelines for contributing to the CAIS 2026 website.

## Getting Started

1. Clone the repository
2. Install dependencies: `npm install`
3. Start dev server: `npm run dev`
4. Make changes and verify at `http://localhost:8080`

## Content Updates

### Text Content

Most text content is either in:
- **Data files** (`src/_data/`) for structured/repeated content
- **Page files** (`src/pages/` or `src/index.njk`) for page-specific content

### Committee Members

Committee data lives in `src/_data/committee.json`. Each member has:

```json
{
  "name": "Full Name",
  "affiliation": "Organization",
  "photo": "filename.png",
  "role": "Optional Role Title",
  "bio": "Bio paragraph..."
}
```

**Photos**: Add to `src/assets/images/` using the naming convention `lastname_firstname.png`. Recommended size: 400x400px, square aspect ratio.

### Dates and Deadlines

All dates are centralized in `src/_data/site.json`. Update there and they'll propagate everywhere.

### Navigation

Edit `src/_data/navigation.json` to add/remove/reorder menu items.

## Adding New Pages

1. Create a new `.njk` file in `src/pages/`
2. Add frontmatter at the top:

```yaml
---
layout: base.njk
title: Your Page Title
description: SEO description
permalink: /pages/your-page-slug/
---
```

3. Write your content using HTML and Nunjucks
4. Add to navigation if needed

## Templates and Components

### Layouts

- `base.njk` - The main HTML wrapper with head, nav, footer, scripts

### Partials

Reusable components in `src/_includes/`:

- `nav.njk` - Site navigation
- `footer.njk` - Site footer
- `committee-card.njk` - Full committee member card
- `committee-thumbnail.njk` - Small circular photo for homepage
- `pillar-card.njk` - "What is CAIS" pillar cards

### Using Data in Templates

Access data files via their filename:

```nunjucks
{{ site.name }}                    {# From site.json #}
{{ site.dates.display }}           {# Nested access #}
{% for item in navigation.main %}  {# Loop over arrays #}
{% for member in committee.steering %}
```

## Styling

### CSS Organization

All styles are in `src/assets/css/styles.css`, organized by section:
- Design system variables
- Base styles
- Navigation
- Hero sections
- Buttons
- Cards
- etc.

### Adding Styles

1. Find the appropriate section in `styles.css`
2. Add your styles following existing patterns
3. Use CSS variables for colors: `var(--terracotta-deep)`

### Page-Specific Styles

For styles only needed on one page, use the `extraStyles` frontmatter:

```yaml
---
extraStyles: |
  .my-special-class {
    color: red;
  }
---
```

## Best Practices

### Accessibility

- Use semantic HTML (`<header>`, `<main>`, `<section>`, `<nav>`)
- Include alt text on all images
- Ensure sufficient color contrast
- Keep the skip-to-main link working

### Performance

- Use `loading="lazy"` on images below the fold
- Keep image file sizes reasonable
- Use SVG for logos and icons where possible

### Consistency

- Follow existing naming conventions
- Use the established CSS class patterns
- Keep component structure consistent

## Testing

Before submitting changes:

1. Run `npm run build` to ensure no build errors
2. Check the site in multiple browsers
3. Test on mobile viewport sizes
4. Verify all links work
5. Check for console errors

## Deployment

The site builds to `_site/`. This folder should be deployed to production.

After merging changes:
1. Run `npm run build`
2. Deploy the `_site/` folder to your hosting provider

## Questions?

Contact the organizing committee at contact@caisconf.org.
