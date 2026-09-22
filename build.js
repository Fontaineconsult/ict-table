#!/usr/bin/env node
// Generate table.html from sources.json + content.json.
// Usage: node build.js

const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const sources = JSON.parse(fs.readFileSync(path.join(ROOT, 'sources.json'), 'utf8'));
const content = JSON.parse(fs.readFileSync(path.join(ROOT, 'content.json'), 'utf8'));

const citationById = new Map(sources.citations.map(c => [c.id, c]));
const columnById = new Map(sources.columns.map(c => [c.id, c]));

// ---------- validation ----------
const errors = [];
for (const colId of content.column_order) {
  if (!columnById.has(colId)) errors.push(`column_order references unknown column: ${colId}`);
}
for (const rg of content.row_groups) {
  for (const row of rg.rows) {
    for (const [colId, clauses] of Object.entries(row.cells)) {
      if (!columnById.has(colId)) errors.push(`unknown column '${colId}' in ${rg.id}/${row.id}`);
      for (let i = 0; i < clauses.length; i++) {
        const cl = clauses[i];
        if (typeof cl.text !== 'string') errors.push(`missing text in ${rg.id}/${row.id}/${colId}[${i}]`);
        for (const cid of cl.citations || []) {
          if (!citationById.has(cid)) errors.push(`unknown citation [${cid}] in ${rg.id}/${row.id}/${colId}[${i}]`);
        }
      }
    }
  }
}
if (errors.length) {
  console.error('Validation failed:');
  errors.forEach(e => console.error('  - ' + e));
  process.exit(1);
}

// ---------- rendering helpers ----------
function escapeHtml(s) {
  return s.replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;');
}

function renderCitation(id) {
  const c = citationById.get(id);
  return `<a href="${c.url}" target="_blank"><sup>[${id}]</sup></a>`;
}

function renderClause(clause) {
  const label = clause.label
    ? `<strong>${escapeHtml(clause.label)}:</strong> `
    : '';
  const text = escapeHtml(clause.text);
  const cites = (clause.citations || []).map(renderCitation).join('');
  return label + text + cites;
}

function renderCell(clauses, indent) {
  if (!clauses || clauses.length === 0) return '';
  const lines = clauses.map(renderClause);
  return lines.map((l, i) => indent + l + (i < lines.length - 1 ? '<br>' : '')).join('\n');
}

// ---------- column helpers ----------
const federalCols = content.column_order.map(id => {
  const c = columnById.get(id);
  if (c.layer !== 'federal') throw new Error(`column_order entry ${id} is not layer=federal`);
  return c;
});
const stateCols = federalCols.map(fc => {
  const sc = columnById.get(fc.pairs_with);
  if (!sc) throw new Error(`federal column ${fc.id} pairs_with unknown column ${fc.pairs_with}`);
  return sc;
});

// ---------- thead ----------
const theadLines = [];
theadLines.push('    <tr class="layer-federal">');
theadLines.push('        <th rowspan="2"></th>');
theadLines.push('        <th rowspan="2">Category</th>');
for (const col of federalCols) {
  const sub = col.sublabel ? `<br>(${escapeHtml(col.sublabel)})` : '';
  theadLines.push(`        <th><a href="${col.url}" target="_blank">${escapeHtml(col.label)}</a>${sub}</th>`);
}
theadLines.push('    </tr>');
theadLines.push('    <tr class="layer-state">');
for (const col of stateCols) {
  theadLines.push(`        <th><a href="${col.url}" target="_blank">${escapeHtml(col.label)}</a></th>`);
}
theadLines.push('    </tr>');

// ---------- tbody ----------
const tbodyLines = [];
for (const rg of content.row_groups) {
  tbodyLines.push(`    <!-- ${rg.label} -->`);
  rg.rows.forEach((row, rowIdx) => {
    tbodyLines.push('    <tr>');
    if (rowIdx === 0) {
      tbodyLines.push(`        <th class="overview" scope="rowgroup" rowspan="${rg.rows.length}">${escapeHtml(rg.label)}</th>`);
    }
    tbodyLines.push(`        <th scope="row">${escapeHtml(row.label)}</th>`);
    for (const col of federalCols) {
      const clauses = row.cells[col.id] || [];
      if (clauses.length === 0) {
        tbodyLines.push('        <td></td>');
      } else if (clauses.length === 1 && !clauses[0].label) {
        // Single-clause cell with no label: inline it on one line like the Recent Updates row.
        tbodyLines.push(`        <td>${renderClause(clauses[0])}</td>`);
      } else {
        tbodyLines.push('        <td>');
        tbodyLines.push(renderCell(clauses, '            '));
        tbodyLines.push('        </td>');
      }
    }
    tbodyLines.push('    </tr>');
  });
}

// ---------- CSS (verbatim from original) ----------
const CSS = `        table.accessibility-comparison {
            width: 100%;
            border-collapse: collapse;
            font-family: Arial, sans-serif;
            margin: 1em 0;
        }
        table.accessibility-comparison th,
        table.accessibility-comparison td {
            border: 1px solid #ccc;
            padding: 0.75em;
            vertical-align: top;
            text-align: left;
        }
        table.accessibility-comparison thead tr.layer-federal th {
            background-color: #004b8d;
            color: #fff;
        }

        table.accessibility-comparison thead tr.layer-federal a {
            color: #fff;
        }
        table.accessibility-comparison thead tr.layer-state th {
            background-color: #f2a900;
            color: #231161;
            font-size: 0.9em;
        }
        table.accessibility-comparison th[scope="row"],
        table.accessibility-comparison th[scope="rowgroup"] {
            background-color: #e9ecef;
            font-weight: bold;
        }
        table.accessibility-comparison th[scope="rowgroup"] {
            width: 12%;
        }
        table.accessibility-comparison th[scope="row"] {
            width: 18%;
        }
        table.accessibility-comparison tbody tr:nth-child(odd) {
            background-color: #fafafa;
        }
        table.accessibility-comparison tbody tr:hover {
            background-color: #f1f5f9;
        }
        table.accessibility-comparison ul {
            margin: 0;
            padding-left: 1.2em;
        }
        table.accessibility-comparison strong {
            font-weight: bold;
        }
        table.accessibility-comparison a {
            color: #004b8d;
            text-decoration: underline;
        }
        table.accessibility-comparison-main-header a {
            color: #ffffff;
            text-decoration: underline;
        }
        table.accessibility-comparison a:hover {
            text-decoration: none;
        }`;

// ---------- assemble ----------
const pageTitle = content.page_title || 'Accessibility Laws: Expert Quick‑Reference';
const caption = content.caption || '';
const now = new Date();
const buildIso = now.toISOString();
const buildDate = buildIso.slice(0, 10);

const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="generator" content="build.js">
    <meta name="build-date" content="${buildIso}">
    <title>${escapeHtml(pageTitle)}</title>
    <style>
${CSS}
        p.build-stamp {
            font-family: Arial, sans-serif;
            font-size: 0.8em;
            color: #666;
            text-align: right;
            margin: 0.5em 0 1em 0;
        }
    </style>
</head>
<body>
<!-- Generated by build.js on ${buildIso} -->
<table class="accessibility-comparison">
    <caption>${escapeHtml(caption)}</caption>
    <thead>
${theadLines.join('\n')}
    </thead>
    <tbody>
${tbodyLines.join('\n')}
    </tbody>
</table>
<p class="build-stamp">Built <time datetime="${buildIso}">${buildDate}</time> from <code>sources.json</code> + <code>content.json</code>.</p>
</body>
</html>
`;

const outPath = path.join(ROOT, 'table.html');
fs.writeFileSync(outPath, html, 'utf8');

// ---------- summary ----------
const cellCount = content.row_groups.reduce((s, rg) =>
  s + rg.rows.reduce((r, row) => r + Object.keys(row.cells).length, 0), 0);
const clauseCount = content.row_groups.reduce((s, rg) =>
  s + rg.rows.reduce((r, row) =>
    r + Object.values(row.cells).reduce((c, arr) => c + arr.length, 0), 0), 0);

console.log(`Wrote ${outPath}`);
console.log(`  ${sources.columns.length} columns, ${sources.citations.length} citations`);
console.log(`  ${content.row_groups.length} row groups, ${content.row_groups.reduce((s,rg)=>s+rg.rows.length,0)} rows, ${cellCount} cells, ${clauseCount} clauses`);
