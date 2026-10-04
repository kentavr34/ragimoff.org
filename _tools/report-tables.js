#!/usr/bin/env node
/* report-tables.js — сводит «до»/«после» из _tools/layout-audit.js в две TSV:
 *
 *   stats-strip-audit.tsv  — страница | полоса | наложение до | наложение после
 *                            | зазор до | зазор после | вывод
 *   label-inset-audit.tsv  — страница | блок | ярлык | инсет до | инсет после
 *                            | отклонение
 *
 * Запуск:
 *   node _tools/report-tables.js <каталог-до> <каталог-после> <каталог-вывода>
 *   (каталоги — с файлами *.json от `layout-audit.js --json`)
 */
'use strict';
const fs = require('fs');
const path = require('path');

const [dirBefore, dirAfter, outDir] = process.argv.slice(2);
if (!dirBefore || !dirAfter || !outDir) {
  console.error('нужны три аргумента: <до> <после> <вывода>');
  process.exit(1);
}

function load(dir) {
  const map = new Map();
  for (const f of fs.readdirSync(dir)) {
    if (!f.endsWith('.json')) continue;
    let rows;
    try { rows = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')); } catch (e) { continue; }
    for (const r of rows) {
      if (r.error) { map.set(r.file, { error: r.error, width: r.width }); continue; }
      map.set(r.file, r);
    }
  }
  return map;
}

/* В пределах одной страницы бывает по несколько ярлыков с одинаковым текстом
   (например два «Tərəf»), поэтому ключ ярлыка — текст + блок + порядковый
   номер в списке. */
function labelKeys(row) {
  const seen = new Map();
  return row.badges.map(function (b) {
    const base = b.block + '|' + b.text;
    const n = (seen.get(base) || 0) + 1;
    seen.set(base, n);
    return { key: base + '#' + n, b: b };
  });
}

const before = load(dirBefore);
const after = load(dirAfter);
fs.mkdirSync(outDir, { recursive: true });

/* ── 1. Полоса цифр vs герой ─────────────────────────────────────── */
const s1 = ['page', 'strip', 'overlap_before', 'overlap_after', 'gap_before', 'gap_after', 'verdict'];
const rowsStrip = [];
for (const [page, b] of before) {
  const a = after.get(page);
  if (!b || b.error) continue;
  if (b.stripT === null && (!a || a.stripT === null)) continue;   // полосы нет ни до, ни после
  const strip = b.strip || (a && a.strip) || '-';
  const ob = b.overlap, oa = a && !a.error ? a.overlap : null;
  const gb = b.gap, ga = a && !a.error ? a.gap : null;
  let verdict;
  if (oa === null) verdict = 'нет замера после';
  else if (oa > 0.5) verdict = 'НАЛОЖЕНИЕ ОСТАЛОСЬ';
  else if (ob !== null && ob > 0.5) verdict = 'исправлено (наложение ' + ob + ' → 0)';
  else verdict = 'не требовалось (наложения не было)';
  rowsStrip.push([page, strip, ob === null ? '-' : ob, oa === null ? '-' : oa,
                  gb === null ? '-' : gb, ga === null ? '-' : ga, verdict]);
}
rowsStrip.sort(function (x, y) { return x[0] < y[0] ? -1 : 1; });
fs.writeFileSync(path.join(outDir, 'stats-strip-audit.tsv'),
  [s1].concat(rowsStrip).map(function (r) { return r.join('\t'); }).join('\n') + '\n', 'utf8');

/* Страницы вообще без полосы — владелец решит, нужна ли она там. */
const noStrip = [];
for (const [page, b] of before) {
  if (b && !b.error && b.stripT === null) noStrip.push(page);
}
noStrip.sort();
fs.writeFileSync(path.join(outDir, 'stats-strip-absent.tsv'),
  ['page'].concat(noStrip).join('\n') + '\n', 'utf8');

/* ── 2. Отступы ярлыков ──────────────────────────────────────────── */
const s2 = ['page', 'block', 'label', 'insetL_before', 'insetT_before',
            'insetL_after', 'insetT_after', 'verdict'];
const rowsLbl = [];
for (const [page, b] of before) {
  if (!b || b.error) continue;
  const a = after.get(page);
  const aMap = new Map();
  if (a && !a.error) for (const x of labelKeys(a)) aMap.set(x.key, x.b);
  for (const x of labelKeys(b)) {
    const y = aMap.get(x.key);
    const stuckB = (x.b.insetL !== null && x.b.insetL < 16) || (x.b.insetT !== null && x.b.insetT < 16);
    let verdict;
    if (!y) verdict = 'нет замера после';
    else if (y.insetL === null) verdict = 'блок не найден после';
    else if (y.insetL >= 16 && y.insetT >= 16) verdict = stuckB ? 'исправлено' : 'соответствует';
    else verdict = 'ОТКЛОНЕНИЕ';
    rowsLbl.push([page, x.b.block || '-', x.b.text,
                  x.b.insetL, x.b.insetT, y ? y.insetL : '-', y ? y.insetT : '-', verdict]);
  }
}
rowsLbl.sort(function (x, y) { return (x[0] + x[1] + x[2]) < (y[0] + y[1] + y[2]) ? -1 : 1; });
fs.writeFileSync(path.join(outDir, 'label-inset-audit.tsv'),
  [s2].concat(rowsLbl).map(function (r) { return r.join('\t'); }).join('\n') + '\n', 'utf8');

/* ── сводка ──────────────────────────────────────────────────────── */
const fixed = rowsStrip.filter(function (r) { return r[6].indexOf('исправлено') === 0; });
const left = rowsStrip.filter(function (r) { return r[6] === 'НАЛОЖЕНИЕ ОСТАЛОСЬ'; });
const stuck = rowsLbl.filter(function (r) { return r[7] === 'исправлено'; });
const dev = rowsLbl.filter(function (r) { return r[7] === 'ОТКЛОНЕНИЕ'; });
console.log('полоса: строк ' + rowsStrip.length + ' | исправлено ' + fixed.length + ' | осталось ' + left.length);
for (const r of fixed) console.log('   FIXED ' + r[0] + '  наложение ' + r[2] + ' → ' + r[3]);
for (const r of left) console.log('   LEFT  ' + r[0] + '  наложение ' + r[3]);
console.log('страниц без полосы: ' + noStrip.length);
console.log('ярлыки: строк ' + rowsLbl.length + ' | приведено ' + stuck.length + ' | отклонений ' + dev.length);
for (const r of dev) console.log('   DEV ' + r.join(' | '));
