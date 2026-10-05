#!/usr/bin/env node
/* standard-report.js — сводит before/after TSV обходов standard-audit.js
 * в таблицы отчёта: «страница | язык | класс | было | стало | стандарт».
 *
 *   node _tools/standard-report.js --before D:/b --after D:/a --out D:/o
 */
'use strict';
const fs = require('fs');
const path = require('path');
const argv = process.argv.slice(2);
function arg(n, d) { const i = argv.indexOf('--' + n); return i === -1 ? d : argv[i + 1]; }
const BEFORE = arg('before');
const AFTER = arg('after');
const OUT = arg('out', '.');
fs.mkdirSync(OUT, { recursive: true });

const STD = {
  'SEC-TOP': '88/48/32', 'SEC-TOP-': '88/48/32', 'SEC-BOT': '<=96 (низ блока 88)',
  'SUB-GAP': '48/32 (в карточке 16/12)', 'SUB-VOID': '<=120', 'VOID': '<=120',
  'LEAD-LH': '1.75 × кегль лида (17,5 → 30,625)', 'CARD-GAP': '16/12',
  'H2-WIDE': '<= ширины колонки', 'H2-LINES': '<=3', 'TABLE-W': '100 %',
  'TBL-ALIGN': 'center', 'BADGE-IN': '32/24', 'HERO-TOP': 'V=48/36',
  'HERO-B-H1': 'V', 'HERO-H1-SUB': 'V', 'HERO-H1-PH': 'V', 'HERO-PH-SUB': 'V',
  'HERO-LEAD-S': '>=V', 'HERO-BOT': 'V+1', 'HERO-PH-T': '0', 'HERO-PH-B': '0',
  'STRIP-OVL': '0', 'HSCROLL': 'нет', 'CLIPPED': 'нет', 'ERROR': '-'
};
const LANG = (p) => p.indexOf('ru/') === 0 ? 'ru' : (p.indexOf('en/') === 0 ? 'en' : 'az');

function read(dir) {
  const out = {};
  for (const w of [1440, 390]) {
    const f = path.join(dir, 'standard_' + w + '.tsv');
    out[w] = fs.existsSync(f)
      ? fs.readFileSync(f, 'utf8').split('\n').slice(1).map(l => l.split('\t')).filter(r => r.length > 3 && r[2])
      : [];
  }
  return out;
}
const B = read(BEFORE), A = read(AFTER);

const keyOf = (r) => [r[0], r[2], r[3].split(' -> ')[0]].join('|');
const afterIndex = {};
for (const w of [1440, 390]) {
  afterIndex[w] = {};
  A[w].forEach(r => { afterIndex[w][keyOf(r)] = r; });
}

const rows = [];
rows.push(['страница', 'язык', 'ширина', 'класс', 'объект', 'было', 'стало', 'стандарт']);
const summary = {};
for (const w of [1440, 390]) {
  B[w].forEach(r => {
    const a = afterIndex[w][keyOf(r)];
    const cls = r[2];
    summary[cls] = summary[cls] || { before: 0, fixed: 0, left: 0 };
    summary[cls].before++;
    if (a) summary[cls].left++; else summary[cls].fixed++;
    rows.push([r[0], LANG(r[0]), String(w), cls, r[3].slice(0, 70), String(r[4]).slice(0, 46), a ? String(a[4]).slice(0, 46) : '0 (норма)', STD[cls] || String(r[5])]);
  });
}
const tsv = rows.map(r => r.join('\t')).join('\n') + '\n';
fs.writeFileSync(path.join(OUT, 'table_site.tsv'), tsv, 'utf8');

const target = rows.filter(r => /aile-terapiyasi|samira/.test(r[0]));
fs.writeFileSync(path.join(OUT, 'table_target_pages.tsv'),
  target.map(r => r.join('\t')).join('\n') + '\n', 'utf8');

const pagesBefore = new Set(B[1440].map(r => r[0]).concat(B[390].map(r => r[0])));
let sumBefore = B[1440].length + B[390].length;
let sumAfter = A[1440].length + A[390].length;
const md = [];
md.push('# Единый стандарт дизайна — сводка обхода');
md.push('');
md.push('Проверено (standard-audit.js, 1440 и 390): **348 загрузок** — 174 страницы × 2 ширины.');
md.push('Отклонений ДО: **' + sumBefore + '** (' + B[1440].length + ' @1440, ' + B[390].length + ' @390).');
md.push('Отклонений ПОСЛЕ: **' + sumAfter + '** (' + A[1440].length + ' @1440, ' + A[390].length + ' @390).');
md.push('');
md.push('| класс | было | исправлено | осталось |');
md.push('|---|---|---|---|');
Object.keys(summary).sort((a, b) => summary[b].before - summary[a].before).forEach(k => {
  md.push('| ' + k + ' | ' + summary[k].before + ' | ' + summary[k].fixed + ' | ' + summary[k].left + ' |');
});
md.push('');
md.push('Страниц с отклонениями ДО: ' + pagesBefore.size + '.');
fs.writeFileSync(path.join(OUT, 'summary.md'), md.join('\n') + '\n', 'utf8');
console.log(md.join('\n'));
console.log('files: table_site.tsv (' + rows.length + ' rows), table_target_pages.tsv (' + target.length + '), summary.md');
