#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replace the search block in all bolme-*.html with full-text search version.
"""
import sys, io, os, glob, unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

OLD_SEARCH = r"""// Search index (page headings)
const idx=[];
document.querySelectorAll('[id]').forEach(el=>{
  const t=el.textContent.trim();
  if(t&&['H1','H2','H3'].includes(el.tagName))
    idx.push({id:el.id,title:t.slice(0,90),page:CURRENT});
});
// Add all pages for cross-page search
ALL_PAGES.forEach(p=>idx.push({id:'',title:p.title,page:p.slug,code:p.code||''}));

const si=document.getElementById('search-input');
const sd=document.getElementById('search-drop');
if(si&&sd){
  let tmr;
  si.addEventListener('input',()=>{
    clearTimeout(tmr);
    tmr=setTimeout(()=>{
      const q=si.value.trim().toLowerCase();
      if(q.length<2){sd.classList.remove('on');return;}
      const res=idx.filter(x=>(x.title+' '+(x.code||'')).toLowerCase().includes(q)).slice(0,12);
      if(!res.length){sd.innerHTML='<div class="sr"><div class="sr-title">Nəticə tapılmadı</div></div>';sd.classList.add('on');return;}
      sd.innerHTML=res.map(r=>{
        const hl=s=>s.replace(new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'),'gi'),m=>'<mark>'+m+'</mark>');
        return `<div class="sr" onclick="goTo('${r.page}','${r.id}')">${r.code?`<div class="sr-code">${hl(r.code)}</div>`:''}
          <div class="sr-title">${hl(r.title)}</div>
          <div class="sr-sub">${r.page}.html</div></div>`;
      }).join('');
      sd.classList.add('on');
    },220);
  });
  document.addEventListener('click',e=>{if(!e.target.closest('.hdr-search'))sd.classList.remove('on');});
  si.addEventListener('keydown',e=>{if(e.key==='Escape'){si.value='';sd.classList.remove('on');}});
}"""

NEW_SEARCH = r"""// Search — full-text index (lazy loaded from search-index.json)
let _srIdx=null,_srLoading=false;
function _srLoad(cb){
  if(_srIdx){cb(_srIdx);return;}
  if(_srLoading){setTimeout(()=>_srLoad(cb),80);return;}
  _srLoading=true;
  fetch('/klinik-psixiatriya/search-index.json')
    .then(r=>r.json())
    .then(d=>{_srIdx=d;_srLoading=false;cb(d);})
    .catch(()=>{_srIdx=[];_srLoading=false;cb([]);});
}

const si=document.getElementById('search-input');
const sd=document.getElementById('search-drop');
if(si&&sd){
  si.addEventListener('focus',()=>_srLoad(()=>{}),{once:true});
  let tmr;
  si.addEventListener('input',()=>{
    clearTimeout(tmr);
    tmr=setTimeout(()=>{
      const q=si.value.trim().toLowerCase();
      if(q.length<2){sd.classList.remove('on');return;}
      _srLoad(idx=>{
        const esc=q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
        const re=new RegExp(esc,'gi');
        const hl=s=>s?String(s).replace(re,m=>'<mark>'+m+'</mark>'):s;
        const res=idx.filter(x=>(x.title+' '+(x.codes||'')+' '+(x.text||'')).toLowerCase().includes(q)).slice(0,20);
        if(!res.length){sd.innerHTML='<div class="sr"><div class="sr-title">Nəticə tapılmadı</div></div>';sd.classList.add('on');return;}
        sd.innerHTML=res.map(r=>{
          let snip='';
          const txt=r.text||'';
          const lo=txt.toLowerCase();
          const i2=lo.indexOf(q);
          if(i2>=0){const s=Math.max(0,i2-50);snip=txt.slice(s,s+140).trim();}
          else{
            const co=(r.codes||'').toLowerCase();
            const i3=co.indexOf(q);
            if(i3>=0){const s=Math.max(0,i3-30);snip=(r.codes||'').slice(s,s+120).trim();}
          }
          return `<div class="sr" onclick="goTo('${r.page}','${r.id}')">
            <div class="sr-title">${hl(r.title)}</div>
            ${snip?`<div class="sr-snip">${hl(snip)}</div>`:''}
            <div class="sr-sub">${r.sub||r.page+'.html'}</div></div>`;
        }).join('');
        sd.classList.add('on');
      });
    },200);
  });
  document.addEventListener('click',e=>{if(!e.target.closest('.hdr-search'))sd.classList.remove('on');});
  si.addEventListener('keydown',e=>{if(e.key==='Escape'){si.value='';sd.classList.remove('on');}});
}"""

total = 0
for fpath in sorted(glob.glob(os.path.join(BASE, 'bolme-*.html'))):
    fname = os.path.basename(fpath)
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    html_n = unicodedata.normalize('NFC', html)
    old_n = unicodedata.normalize('NFC', OLD_SEARCH)
    if old_n in html_n:
        html_n = html_n.replace(old_n, unicodedata.normalize('NFC', NEW_SEARCH), 1)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html_n)
        print(f'  OK {fname}')
        total += 1
    else:
        print(f'  MISS {fname}')

print(f'\nDone. {total} files updated.')
