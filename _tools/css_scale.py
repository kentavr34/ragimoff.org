"""Отступы — только из шкалы. Режимы:
  python _tools/css_scale.py check   — сколько объявлений margin/padding/gap заданы числом в px (должно быть 0);
  python _tools/css_scale.py fix     — заменить такие числа ближайшей ступенью шкалы (сдвиг не больше 2 px), шкала — в :root.
Запуск из test/11."""
import io, re, sys

P = 'assets/css/site.css'
STEPS = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 40]
HEAD = {60: 62, 62: 62, 70: 70, 76: 76, 86: 86}                 # отступы под шапку — свои именованные ступени
PROP = re.compile(r'((?:margin|padding)(?:-top|-bottom|-left|-right|-block|-inline)?|gap|row-gap|column-gap)(\s*:\s*)([^;}]+)')
NUM = re.compile(r'(?<![\w.#-])(\d+(?:\.\d+)?)px')


def token(v):
    if v <= 1:
        return None
    if v in HEAD:
        return 'var(--hd%d)' % HEAD[v]
    s = min(STEPS, key=lambda x: (abs(x - v), x))
    return 'var(--p%d)' % s


def walk(css, fix):
    out, pos, n = [], 0, 0
    for m in re.finditer(r'/\*.*?\*/', css, re.S):               # комментарии не трогаем
        seg = css[pos:m.start()]
        seg, k = handle(seg, fix); n += k
        out.append(seg); out.append(m.group(0)); pos = m.end()
    seg, k = handle(css[pos:], fix); n += k
    out.append(seg)
    return ''.join(out), n


def handle(seg, fix):
    cnt = [0]

    def decl(m):
        def num(x):
            v = float(x.group(1)); t = token(v)
            if t is None:
                return x.group(0)
            cnt[0] += 1
            return t if fix else x.group(0)
        return m.group(1) + m.group(2) + NUM.sub(num, m.group(3))
    return PROP.sub(decl, seg), cnt[0]


css = io.open(P, encoding='utf-8').read()
mode = sys.argv[1] if len(sys.argv) > 1 else 'check'
if mode == 'check':
    _, n = walk(css, False)
    print('отступов числом в px:', n)
    sys.exit(1 if n else 0)
new, n = walk(css, True)
if '--p2:' not in new:
    root = ':root { ' + ' '.join('--p%d: %dpx;' % (s, s) for s in STEPS) + ' ' + ' '.join('--hd%d: %dpx;' % (v, v) for v in sorted(set(HEAD.values()))) + ' }   /* малая шкала отступов и отступы под шапку — меняются здесь */\n'
    i = new.index(':root')
    new = new[:i] + root + new[i:]
io.open(P, 'w', encoding='utf-8', newline='\n').write(new)
print('заменено:', n)
