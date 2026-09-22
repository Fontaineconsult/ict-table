---
name: build-table
description: Regenerate table.html from sources.json and content.json by running the Node-based generator (build.js). Use this after any edit to sources.json or content.json, or whenever the user asks to rebuild, regenerate, or refresh the accessibility laws HTML table.
---

# build-table

Regenerates `table.html` — the accessibility laws comparison table — as a derived artifact from two JSON source files:

- `sources.json` — citation bank (columns + [1]–[N] citations with URL and metadata).
- `content.json` — content matrix (row groups → rows → cells → clauses).

`table.html` should never be hand-edited; edit the JSON and run this skill.

## What to do when invoked

1. From the repo root, run:
   ```
   node build.js
   ```

2. Capture stdout/stderr. On success, the generator prints a summary like:
   ```
   Wrote /path/to/table.html
     10 columns, 17 citations
     3 row groups, 11 rows, 55 cells, 88 clauses
   ```
   Relay those stats back to the user in one or two sentences.

3. On validation failure, `build.js` exits non-zero and prints a list of errors (unknown column id, unknown citation id, missing text, etc.). Surface each error verbatim to the user and do **not** attempt to silently fix `content.json` — ask the user how they want it resolved.

4. If `node` is missing (`command not found` or exit 127), tell the user Node.js ≥ 18 is required to regenerate the table, and point them at `build.js` as the generator. Do not hand-roll the HTML in place of the script.

## When to offer this skill proactively

- User edited `sources.json` or `content.json` and the on-disk `table.html` is now stale.
- User asks to "rebuild / regenerate / refresh the table," "update the HTML," or similar.
- User asks to verify their JSON edits are valid (the skill surfaces the validator's errors).

## When NOT to use this skill

- User is only asking about the JSON structure or citation metadata (no HTML change needed).
- User is hand-editing `table.html` on purpose for a one-off experiment (flag that edits to `table.html` will be overwritten on the next run of this skill).

## Notes on the generator

- `build.js` validates before writing: every `column_order` entry and every cell's `column_id` must exist in `sources.json.columns`; every `citations: [id]` must exist in `sources.json.citations`.
- Rowspans are computed from `rows.length` per row group — do not hand-maintain them in `content.json`.
- HTML is emitted with `&`, `<`, `>` escaped in content; the CSS block is preserved verbatim. Output file is `table.html` in the repo root.
