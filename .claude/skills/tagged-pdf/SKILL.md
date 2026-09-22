---
name: tagged-pdf
description: Produce an accessible, tagged PDF from an HTML page (poster, one-pager, report, design-canvas artboard) using headless Chrome's tagged print plus a pikepdf post-process that flattens NonStruct wrappers, repairs the structure tree, and sets language and title metadata. Use this whenever the user wants a PDF export of HTML that screen readers can navigate, mentions tags, PDF/UA, alt text, NVDA/JAWS, "accessible PDF", or complains that a canvas or browser "Export PDF" mangled the layout or lost fonts. Also use it to audit an existing PDF's tag tree.
---

# Tagged PDF from HTML

A tagged PDF is the page's accessibility tree written down: a structure tree of Document, H1-H6,
P, L/LI, Figure (with /Alt) laid over the drawn text runs. Headless Chrome builds that tree from
the HTML's accessibility tree when printing with `--export-tagged-pdf`, so the tags are only as
good as the markup. This skill is the markup checklist, the print command, and a post-process
that cleans up what Chrome leaves behind. NVDA reads the result as a structured document.

Why not the app's own export: canvas and design-tool exporters re-render elsewhere, usually
without the web fonts and with different fragmentation, so text overlaps and nothing is tagged.
Printing from the same Chrome that renders the page correctly avoids both problems.

## 1. Make the HTML say what things are

Chrome maps roles to tags: heading -> H1..H6, list -> L/LI, paragraph -> P, image with alt ->
Figure + /Alt, image with `alt=""` -> artifact (dropped from the tree). Everything else, every
div and span, becomes NonStruct. So before printing, make sure:

- The document has one `h1`, a sensible `h2`/`h3` ladder, and `lang` on `<html>`.
- Repeated items are real lists (`ul`/`ol` + `li`), body copy is `p`. Reset default margins in
  CSS (`h1,h2,h3{margin:0;font-size:inherit;font-weight:inherit} ul{list-style:none;margin:0;padding:0} p{margin:0}`)
  so nothing moves visually.
- Icons and marks that carry meaning are `<img alt="...">`, not inline SVG or CSS. Chrome does
  not export alt for inline SVG, and visually-hidden "sr-only" text (clip/1px tricks) is culled
  from the print entirely, so it never reaches the PDF. A generated SVG file per icon with a real
  alt is the reliable route; keep inline SVG for on-screen builds if you like, but switch to
  `<img>` for the print build.
- Decorative images get `alt=""`.
- Avoid CSS multi-column (`column-count`) around structured content: fragmentation scrambles the
  tag tree inside list items. Use explicit flex/grid columns instead; they print identically.
- Fixed sheet size: add `@page { size: <W>in <H>in; margin: 0 }` and a print rule that pins
  `html, body` to the same size with `print-color-adjust: exact` so tints and backgrounds print.
  Write the size in inches or points; if the page pipeline scales px values, px in `@page` will
  be scaled too.

## 2. Print and post-process

Serve the HTML over HTTP (file:// blocks fonts and relative assets in headless mode), then run
the bundled script. It launches Chrome, prints with tagging, flattens NonStruct wrappers, repairs
parent links and the ParentTree, sets `/Lang`, `DisplayDocTitle` and XMP title/description, and
prints a tag tally plus integrity checks:

```
python <skill-dir>/scripts/print_tagged_pdf.py http://127.0.0.1:8765/page.html out.pdf \
  --title "Document title" --lang en-US --description "One sentence for the metadata"
```

Options: `--chrome <path>` if Chrome is not in the default Windows/macOS/Linux location,
`--no-flatten` to keep NonStruct, `--report-only existing.pdf` to audit a PDF without printing.

Start a server from the page's folder first (`python -m http.server 8765 --bind 127.0.0.1 &`)
and stop it afterwards. If the output file is open in a viewer the save fails with a permission
error; write to a new name.

## 3. Verify, do not assume

The script's report is the minimum. Read it:

- **tags**: expect the counts you designed for (one H1, an H2 per section, an L per list, a
  Figure per meaningful image with `alts` equal to the Figure count). NonStruct should be 0 after
  flattening.
- **ParentTree unresolved / mismatched** and **broken /P links** must be 0; otherwise a screen
  reader's reading order can jump.
- **text chars** > 0 and the page size matches the sheet.
- Render a proof (`pymupdf` page.get_pixmap) and look at it; overlaps mean fonts did not load
  (raise `--virtual-time-budget`) or the print rule is missing.

Then say what the file is: "tagged" with headings, lists, paragraphs and alt text. Chrome emits
no Lbl/LBody inside list items and no table structure beyond what the markup gives, so do not
claim PDF/UA conformance. Suggest PAC 2024 (free, Windows) or Acrobat's checker for a formal
report; remediation tools (Acrobat, axesPDF, CommonLook) start from a much better place when
the semantics are already right.

## Gotchas learned the hard way

- Chrome prints only what is on screen: hidden text (clip, 1px, offscreen) is gone, `display:none`
  is gone, but `alt` on `<img>` survives. Put text alternatives in alt.
- `<p>` directly inside `<li>` is merged into the LI by Chrome; that is fine.
- Percent widths on images and flex layouts print exactly as on screen; `vh`/`vw` do not.
- Fonts: give Chrome time (`--virtual-time-budget=15000`) and confirm with `document.fonts.ready`
  in a preview if in doubt. Google Fonts load fine over HTTP; not over file://.
- pikepdf's `open(path, allow_overwriting_input=True)` is needed to save in place.
