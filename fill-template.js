#!/usr/bin/env node
/**
 * fill-template.js
 * Reads client-data.json, replaces all [TOKEN] placeholders in every .html
 * file in this directory, and writes output to ./dist/.
 *
 * Usage:
 *   node fill-template.js
 *   node fill-template.js --check   (only report unfilled tokens, no output)
 */

const fs   = require('fs');
const path = require('path');

const CHECK_ONLY = process.argv.includes('--check');
const TOKEN_RE   = /\[([A-Z][A-Z 0-9_]*)\]/g;

// ── Load client data ──────────────────────────────────────────────────────
if (!fs.existsSync('client-data.json')) {
  console.error('ERROR: client-data.json not found. Create it before running.');
  process.exit(1);
}
const data = JSON.parse(fs.readFileSync('client-data.json', 'utf8'));

// ── Collect HTML files ────────────────────────────────────────────────────
const htmlFiles = fs.readdirSync('.').filter(f => f.endsWith('.html')).sort();

if (!CHECK_ONLY) {
  if (!fs.existsSync('dist')) fs.mkdirSync('dist');
  const imgSrc = path.join('.', 'images');
  const imgDst = path.join('dist', 'images');
  if (fs.existsSync(imgSrc) && !fs.existsSync(imgDst)) {
    fs.mkdirSync(imgDst);
    for (const img of fs.readdirSync(imgSrc)) {
      fs.copyFileSync(path.join(imgSrc, img), path.join(imgDst, img));
    }
  }
}

// ── Process each file ─────────────────────────────────────────────────────
const unfilled = new Set();

for (const file of htmlFiles) {
  let content = fs.readFileSync(file, 'utf8');

  // Replace known tokens from client-data.json
  for (const [key, value] of Object.entries(data)) {
    if (value === '' || value == null) continue;
    const placeholder = `[${key}]`;
    content = content.split(placeholder).join(value);
  }

  // Collect any remaining unfilled tokens
  let m;
  TOKEN_RE.lastIndex = 0;
  while ((m = TOKEN_RE.exec(content)) !== null) {
    unfilled.add(m[1]);
  }

  if (!CHECK_ONLY) {
    fs.writeFileSync(path.join('dist', file), content, 'utf8');
    console.log(`  ✓  ${file}`);
  }
}

// ── Report ────────────────────────────────────────────────────────────────
if (unfilled.size > 0) {
  console.log('\n⚠️  Unfilled tokens (' + unfilled.size + '):');
  for (const t of [...unfilled].sort()) {
    console.log(`     [${t}]`);
  }
  if (CHECK_ONLY) process.exit(1);
} else {
  console.log('\n✅  All tokens filled. Output in ./dist/');
}
