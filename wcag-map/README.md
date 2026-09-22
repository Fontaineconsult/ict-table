# WCAG 2.2 Success Criteria Map (36 x 24 in poster)

Generated poster: all 86 WCAG 2.2 success criteria by principle and guideline, each with a
plain-language line and the Section 508 functional performance criteria it serves.

## Files

- `gen.py` — the generator. All content (criteria, one-liners, FPC mapping, legend, key, About
  text) and layout live here. `S` at the top is the print scale (base units x S = 3456 x 2304 px).
- `project/Main.dc.html`, `project/canvas.json` — the canvas build (Claude Design canvas at
  https://claude.ai/artifact/ATU1rib1x8EhQg9c2Ld3oZ). Inline SVG icons, images by `/_blob/` id.
- `preview.html` — the print build (`PREVIEW=1`): local image paths, `<img alt>` icons so the
  PDF carries alt text.
- `assets.json` — principle drawings by uploaded asset id. `images/alpha/*.png` are the
  white-on-transparent versions actually used; `images/*.png` are the Recraft originals.
- `icons/*.svg` — FPC and 508 glyphs, regenerated on every build.
- `export/wcag-map-36x24-tagged.pdf` — the deliverable PDF (tagged, 36 x 24 in, live text).
- `outline.md` — design outline and history.

## Rebuild

```
python gen.py                 # canvas build -> project/
PREVIEW=1 python gen.py       # print build -> project/ (copy to preview.html)
```

## Publish to the canvas

Publish `project/canvas.json` + `project/Main.dc.html` with root = this folder. Before
publishing, read the artifact and diff `project/Main.dc.html` against the server copy: the canvas
editor saves the user's on-canvas edits, which must be folded into `gen.py`, and an open editor tab
can save a stale copy over a fresh publish. Verify by reading the file back.

## Export the PDF (do not use the canvas exporter; it re-renders without the fonts)

```
PREVIEW=1 python gen.py && cp project/Main.dc.html preview.html
python -m http.server 8765 --bind 127.0.0.1 &
"C:/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu \
  --export-tagged-pdf --no-pdf-header-footer --virtual-time-budget=15000 \
  --print-to-pdf="export\wcag-map-36x24-tagged.pdf" http://127.0.0.1:8765/preview.html
```

Then run `python pdf_postprocess.py export/wcag-map-36x24-tagged.pdf` (add an output path if the
file is open in a viewer). It removes the NonStruct
wrappers Chrome emits for every div/span (hoisting their content into the real parent and repairing
the ParentTree), and sets `/Lang en-US`, `DisplayDocTitle`, and the XMP title/description.
Chrome's tags cover headings (H1-H3), lists (L/LI), paragraphs, and Figures with alt text; list
items have no Lbl/LBody, so full PDF/UA conformance still needs a pass in Acrobat, axesPDF or
CommonLook. Check with PAC 2024.
