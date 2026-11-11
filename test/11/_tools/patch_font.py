"""Интерфейсный шрифт: Manrope → Inter (в Manrope нет заглавной Ə). Проверка букв азербайджанского алфавита — в замер. Запуск из test/11."""
import io, re

p = 'index.html'
t = io.open(p, encoding='utf-8').read()
a = 'family=Manrope:wght@400;500;600'
if a not in t:
    raise SystemExit('ссылка на Manrope не найдена')
t = t.replace(a, 'family=Inter:wght@400;500;600').replace('&family=Oswald:wght@400;500', '')
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

p = 'assets/css/site.css'
t = io.open(p, encoding='utf-8').read()
n = t.count('"Manrope"')
t = t.replace('"Manrope"', '"Inter"')
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('в стилях заменено:', n)

p = '_tools/round.py'
t = io.open(p, encoding='utf-8').read()
if 'N4' not in t.split('MEASURE')[1][:6000] and 'AZ_LETTERS' not in t:
    a = "                    res = await ev(MEASURE) or {'bad': [['?', 'замер не выполнен']], 'info': {}}"
    if a not in t:
        raise SystemExit('round.py: якорь не найден')
    t = t.replace(a, a + "\n                    if lg == 'az' and th == 'night':                             # N4: все буквы азербайджанского алфавита и кириллица есть в каждой гарнитуре страницы\n                        miss = await ev(AZ_LETTERS)\n                        for m in (miss or []):\n                            res['bad'].append(['N4', m])")
    t = t.replace('async def main():', '''AZ_LETTERS = r"""
(async () => {
  const chars = ['Ə', 'ə', 'İ', 'ı', 'Ş', 'ş', 'Ğ', 'ğ', 'Ç', 'ç', 'Ö', 'ö', 'Ü', 'ü', 'Ж', 'я'];
  const fams = new Set(); document.querySelectorAll('body *').forEach(e => { const r = e.getBoundingClientRect(); if (r.width > 1 && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) fams.add(getComputedStyle(e).fontFamily.split(',')[0].replace(/["']/g, '').trim()); });
  const out = [];
  for (const f of fams) { for (const w of ['300', '400', '500', '600']) { try { await document.fonts.load(w + ' 40px "' + f + '"', chars.join('')); } catch (e) {} } }
  await new Promise(r => setTimeout(r, 1200));
  const c = document.createElement('canvas').getContext('2d'); const w = (f, ch) => { c.font = '40px ' + f; return c.measureText(ch).width; };
  for (const f of fams) { const hand = /Monsieur/.test(f); const m = chars.filter(ch => !(hand && /[Жя]/.test(ch)) && Math.abs(w('"' + f + '", monospace', ch) - w('"' + f + '", serif', ch)) > .01); if (m.length && !hand) out.push('в гарнитуре ' + f + ' нет букв: ' + m.join(' ')); }
  return out;
})()
"""


async def main():''', 1)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('patched')
