import re,glob,os,sys
from html.parser import HTMLParser
SKIP={'br','hr','img','input','meta','link','source','col','area','wbr',
      'path','rect','circle','line','polygon','polyline','ellipse','stop','use'}
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.st=[]; s.err=[]
    def handle_starttag(s,t,a):
        if t in SKIP: return
        s.st.append(t)
    def handle_startendtag(s,t,a):
        if t in SKIP: return
        pass
    def handle_endtag(s,t):
        if t in SKIP: return
        if s.st and s.st[-1]==t: s.st.pop(); return
        s.err.append(('mismatch',t,s.st[-1] if s.st else None,s.getpos()))
def check(text):
    p=P(); p.feed(text); return len(p.err), len(p.st), p.err[:2]
bad=0; tot=0; ex=[]
for d in ['klinik-psixiatriya','klinik-psixiatriya/ru','klinik-psixiatriya/tr','klinik-psixiatriya/en']:
    for fp in sorted(glob.glob(os.path.join(d,'*.html'))):
        n,m,e = check(open(fp,encoding='utf-8',errors='replace').read()); tot+=1
        if n or m:
            bad+=1
            if len(ex)<5: ex.append((fp,n,m,e))
print(f'проверено {tot}, с нарушениями {bad}')
for e in ex: print('  ',e)
