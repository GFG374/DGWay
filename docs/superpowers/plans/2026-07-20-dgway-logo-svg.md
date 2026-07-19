# DGWay Logo SVG Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a compact, transparent, true-vector DGWay logo sized for 80×80 display and save it to the user's desktop.

**Architecture:** Reconstruct the supplied raster logo with a small set of SVG paths, ellipses, and rounded strokes. Use a single 80×80 viewBox, then validate the XML and rasterize a preview to confirm the mark remains legible at its target size.

**Tech Stack:** SVG 1.1-compatible XML, `xmllint`, macOS Quick Look

---

## File Structure

- Create `/Users/goufugui/Desktop/dgway logo.svg`: final transparent vector logo.
- Create `/tmp/dgway-logo-preview/`: temporary render output used only for visual verification, then remove it.

### Task 1: Create the SVG Logo

**Files:**
- Create: `/Users/goufugui/Desktop/dgway logo.svg`

- [ ] **Step 1: Write the SVG**

Create the final file with an 80×80 canvas, an accessible title and description, a black DG/face mark, blue cheeks, a blue star, and a blue orbit path. Use only vector primitives and no embedded bitmap:

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 80 80" role="img" aria-labelledby="title desc">
  <title id="title">DGWay Logo</title>
  <desc id="desc">Black DG monogram with a friendly robot face, blue cheeks, star and orbit.</desc>
  <defs>
    <linearGradient id="blue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#2496ff"/>
      <stop offset="1" stop-color="#3b82f6"/>
    </linearGradient>
  </defs>
  <path d="M8 18h18c11 0 20 6 24 15l-6 2c-3-7-10-11-18-11H14v27h7" fill="none" stroke="#101722" stroke-width="6" stroke-linejoin="round"/>
  <path d="M53 34a21 21 0 1 0 6 14H42" fill="none" stroke="#101722" stroke-width="6" stroke-linecap="square"/>
  <ellipse cx="34" cy="55" rx="1.5" ry="3" fill="#101722"/>
  <ellipse cx="45" cy="55" rx="1.5" ry="3" fill="#101722"/>
  <path d="m25 61-1.4 2m4.2-2-1.4 2m4.2-2-1.4 2m18-2-1.4 2m4.2-2-1.4 2m4.2-2-1.4 2" fill="none" stroke="url(#blue)" stroke-width="2.2" stroke-linecap="round"/>
  <path d="M58 9l1.3 4.2L63.5 15l-4.2 1.5L58 21l-1.4-4.5-4.1-1.5 4.1-1.8L58 9Z" fill="url(#blue)"/>
  <path d="M66 13c13-2 7 10-19 25 18-8 33-19 28-26-2-3-6-2-9 1Z" fill="url(#blue)"/>
</svg>
```

- [ ] **Step 2: Confirm the file contains no embedded bitmap**

Run:

```bash
rg -n 'data:image|<image' '/Users/goufugui/Desktop/dgway logo.svg'
```

Expected: no output and exit status 1.

### Task 2: Validate and Preview the Deliverable

**Files:**
- Test: `/Users/goufugui/Desktop/dgway logo.svg`
- Create temporarily: `/tmp/dgway-logo-preview/dgway logo.svg.png`

- [ ] **Step 1: Validate the SVG XML**

Run:

```bash
xmllint --noout '/Users/goufugui/Desktop/dgway logo.svg'
```

Expected: no output and exit status 0.

- [ ] **Step 2: Verify the target dimensions and transparent background**

Run:

```bash
rg -n '<svg[^>]+width="80"[^>]+height="80"[^>]+viewBox="0 0 80 80"' '/Users/goufugui/Desktop/dgway logo.svg'
rg -n '<rect|background|fill="white"|#fff' '/Users/goufugui/Desktop/dgway logo.svg'
```

Expected: the first command prints the root SVG line; the second prints no output because the document has no background shape.

- [ ] **Step 3: Render an 80×80 preview**

Run:

```bash
mkdir -p /tmp/dgway-logo-preview
qlmanage -t -s 80 -o /tmp/dgway-logo-preview '/Users/goufugui/Desktop/dgway logo.svg'
```

Expected: Quick Look reports thumbnail generation success and creates `/tmp/dgway-logo-preview/dgway logo.svg.png`.

- [ ] **Step 4: Visually inspect and clean up**

Open the rendered preview and confirm the DG outline, two eyes, both cheek groups, star, and orbit remain distinct at 80×80. Remove `/tmp/dgway-logo-preview/` after inspection so only the requested desktop SVG remains.
