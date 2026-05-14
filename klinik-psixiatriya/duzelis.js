/* Düzəliş et — feedback widget
   Endpoint: Google Apps Script Web App URL (POST JSON)
   Configure ENDPOINT below after deploying the GAS script (see duzelis-gas.txt).
*/
(function(){
  "use strict";
  const ENDPOINT = "https://script.google.com/macros/s/AKfycbzS9vijozxUyEB3pWJcQY09y4MzmSmk_wvE-3w9ThYTLnqG79yWwhQggfRNW3roLv2m2A/exec";
  const MAX_SAMPLE_LEN = 280;
  const MIN_SAMPLE_LEN = 30;

  function $(sel, root){ return (root||document).querySelector(sel); }
  function el(tag, attrs, html){
    const e = document.createElement(tag);
    if(attrs) for(const k in attrs) e.setAttribute(k, attrs[k]);
    if(html!=null) e.innerHTML = html;
    return e;
  }

  function pickRandomSample(){
    const nodes = document.querySelectorAll("main h2, main h3, main h4, main p, main li");
    const cands = [];
    nodes.forEach(n=>{
      const t = (n.textContent||"").trim().replace(/\s+/g," ");
      if(t.length>=MIN_SAMPLE_LEN && t.length<=MAX_SAMPLE_LEN) cands.push(t);
    });
    if(!cands.length) return "";
    return cands[Math.floor(Math.random()*cands.length)];
  }

  function buildModal(){
    const backdrop = el("div",{class:"dzl-backdrop", role:"dialog", "aria-modal":"true"});
    const modal = el("div",{class:"dzl-modal"});
    backdrop.appendChild(modal);
    backdrop.addEventListener("click", e=>{
      if(e.target===backdrop) close();
    });
    document.body.appendChild(backdrop);

    function close(){ backdrop.classList.remove("open"); }
    function open(){
      renderChoices();
      backdrop.classList.add("open");
    }

    function renderChoices(){
      modal.innerHTML = "";
      modal.appendChild(el("h3",{}, "Düzəliş et"));
      modal.appendChild(el("p",{class:"dzl-lead"},
        "Bu kitab inkişaf edən sənəddir. Hər iki yolla kömək edə bilərsiniz:"));
      const wrap = el("div",{class:"dzl-choices"});
      const b1 = el("button",{class:"dzl-choice", type:"button"},
        "<b>Səhv tapdım</b><span>Konkret səhv mətni göstərib düzgün variantı təklif edirəm</span>");
      const b2 = el("button",{class:"dzl-choice", type:"button"},
        "<b>Kömək etməyə hazıram</b><span>Təsadüfi cümlə üzərində redaktə təklifi verirəm</span>");
      b1.onclick = renderError;
      b2.onclick = renderHelp;
      wrap.appendChild(b1); wrap.appendChild(b2);
      modal.appendChild(wrap);
      const actions = el("div",{class:"dzl-actions"});
      const cancel = el("button",{class:"dzl-btn ghost", type:"button"}, "Bağla");
      cancel.onclick = close;
      actions.appendChild(cancel);
      modal.appendChild(actions);
    }

    function renderError(){
      modal.innerHTML = "";
      modal.appendChild(el("h3",{}, "Səhv tapdım"));
      modal.appendChild(el("p",{class:"dzl-lead"},
        "1) Səhv mətni daxil edin. 2) Necə olmalı olduğunu yazın."));
      const f1 = el("div",{class:"dzl-field"});
      f1.appendChild(el("label",{for:"dzl-orig"}, "Səhv mətn"));
      f1.appendChild(el("textarea",{id:"dzl-orig", placeholder:"Səhifədəki səhv hissəni buraya köçürün"}));
      const f2 = el("div",{class:"dzl-field"});
      f2.appendChild(el("label",{for:"dzl-prop"}, "Necə olmalıdır"));
      f2.appendChild(el("textarea",{id:"dzl-prop", placeholder:"Düzgün variantı yazın"}));
      modal.appendChild(f1); modal.appendChild(f2);
      modal.appendChild(actionsBar("error"));
    }

    function renderHelp(){
      modal.innerHTML = "";
      modal.appendChild(el("h3",{}, "Kömək etməyə hazıram"));
      modal.appendChild(el("p",{class:"dzl-lead"},
        "Bu cümlə təsadüfi seçilib. Daha yaxşı necə yaza bilərdik?"));
      const sample = pickRandomSample() || "Bu səhifədə uyğun cümlə tapılmadı.";
      const f1 = el("div",{class:"dzl-field"});
      f1.appendChild(el("label",{}, "Mətn (səhifədən)"));
      const ro = el("div",{class:"dzl-readonly", id:"dzl-orig-ro"}, "");
      ro.textContent = sample;
      f1.appendChild(ro);
      const f2 = el("div",{class:"dzl-field"});
      f2.appendChild(el("label",{for:"dzl-prop"}, "Sizin variant"));
      f2.appendChild(el("textarea",{id:"dzl-prop", placeholder:"Yenidən yazın və ya redaktə təklif edin"}));
      modal.appendChild(f1); modal.appendChild(f2);
      modal.appendChild(actionsBar("help"));
    }

    function actionsBar(kind){
      const wrap = el("div",{class:"dzl-actions"});
      const back = el("button",{class:"dzl-btn ghost", type:"button"}, "← Geri");
      back.onclick = renderChoices;
      const send = el("button",{class:"dzl-btn primary", type:"button"}, "Göndər");
      send.onclick = ()=>submit(kind, send);
      wrap.appendChild(back); wrap.appendChild(send);
      return wrap;
    }

    async function submit(kind, btn){
      const proposed = ($("#dzl-prop", modal)||{}).value || "";
      const original = kind==="error"
        ? (($("#dzl-orig", modal)||{}).value || "")
        : (($("#dzl-orig-ro", modal)||{}).textContent || "");
      if(!proposed.trim() || !original.trim()){
        return showToast("Hər iki sahə doldurulmalıdır.", "err");
      }
      btn.disabled = true; btn.textContent = "Göndərilir...";
      const payload = {
        kind: kind,
        url: location.href,
        title: document.title,
        original: original.trim().slice(0, 4000),
        proposed: proposed.trim().slice(0, 4000),
        ua: navigator.userAgent,
        ts: new Date().toISOString()
      };
      try{
        if(ENDPOINT.indexOf("__")===0){
          throw new Error("Endpoint konfiqurasiya olunmayıb");
        }
        const res = await fetch(ENDPOINT, {
          method:"POST",
          headers:{"Content-Type":"text/plain;charset=utf-8"}, // avoid CORS preflight to GAS
          body: JSON.stringify(payload)
        });
        if(!res.ok) throw new Error("HTTP "+res.status);
        showToast("Təşəkkürlər! Təklifiniz qəbul edildi.", "ok");
        setTimeout(renderChoices, 1400);
      }catch(err){
        console.error(err);
        showToast("Göndərmə alınmadı: "+err.message, "err");
        btn.disabled = false; btn.textContent = "Göndər";
      }
    }

    function showToast(msg, cls){
      const old = modal.querySelector(".dzl-toast"); if(old) old.remove();
      const t = el("div",{class:"dzl-toast "+(cls||"ok")}, "");
      t.textContent = msg;
      modal.appendChild(t);
    }

    return { open };
  }

  // ─── Per-term editor (for abbreviatur.html "Düzəlt" buttons) ────────
  function buildTermEditor(){
    const backdrop = el("div",{class:"dzl-backdrop", role:"dialog", "aria-modal":"true"});
    const modal = el("div",{class:"dzl-modal"});
    backdrop.appendChild(modal);
    backdrop.addEventListener("click", e=>{ if(e.target===backdrop) close(); });
    document.body.appendChild(backdrop);

    let currentTerm = "";
    let currentKind = "term";
    function close(){ backdrop.classList.remove("open"); }
    function open(term, kind){
      currentTerm = term || "";
      currentKind = kind || "term";
      render();
      backdrop.classList.add("open");
    }
    function render(){
      modal.innerHTML = "";
      modal.appendChild(el("h3",{}, "Termin düzəlişi"));
      modal.appendChild(el("p",{class:"dzl-lead"},
        "Cari forma birinci sahədə yerləşdirilib. İkinci sahəyə akademik azərbaycan dilində <b>düzgün formanı</b> daxil edin. Lazım gəlsə, mənbə və ya izah yazın."));
      const f1 = el("div",{class:"dzl-field"});
      f1.appendChild(el("label",{for:"dzl-term-orig"}, "Cari forma (saytda)"));
      const inp1 = el("input",{id:"dzl-term-orig", type:"text", readonly:"readonly"});
      inp1.value = currentTerm;
      f1.appendChild(inp1);
      const f2 = el("div",{class:"dzl-field"});
      f2.appendChild(el("label",{for:"dzl-term-prop"}, "Düzgün forma"));
      const inp2 = el("input",{id:"dzl-term-prop", type:"text",
        placeholder:"Düzgün azərbaycan forması..."});
      f2.appendChild(inp2);
      const f3 = el("div",{class:"dzl-field"});
      f3.appendChild(el("label",{for:"dzl-term-note"}, "Mənbə / izah (könüllü)"));
      f3.appendChild(el("textarea",{id:"dzl-term-note", rows:"2",
        placeholder:"AzPA göstəricisi, akademik mənbə, kontekst..."}));
      modal.appendChild(f1); modal.appendChild(f2); modal.appendChild(f3);
      const wrap = el("div",{class:"dzl-actions"});
      const cancel = el("button",{class:"dzl-btn ghost", type:"button"}, "Bağla");
      cancel.onclick = close;
      const send = el("button",{class:"dzl-btn primary", type:"button"}, "Təklifi göndər");
      send.onclick = ()=>submitTerm(send);
      wrap.appendChild(cancel); wrap.appendChild(send);
      modal.appendChild(wrap);
      setTimeout(()=>inp2.focus(), 50);
    }
    async function submitTerm(btn){
      const orig = ($("#dzl-term-orig", modal)||{}).value || currentTerm;
      const prop = (($("#dzl-term-prop", modal)||{}).value || "").trim();
      const note = (($("#dzl-term-note", modal)||{}).value || "").trim();
      if(!prop){
        return showToast("Düzgün formanı boş buraxmayın.", "err");
      }
      btn.disabled = true; btn.textContent = "Göndərilir...";
      const payload = {
        kind: "term-edit",
        rowKind: currentKind,
        url: location.href,
        title: document.title,
        original: orig.trim().slice(0, 500),
        proposed: prop.slice(0, 500),
        note: note.slice(0, 2000),
        ua: navigator.userAgent,
        ts: new Date().toISOString()
      };
      try{
        const res = await fetch(ENDPOINT, {
          method:"POST",
          headers:{"Content-Type":"text/plain;charset=utf-8"},
          body: JSON.stringify(payload)
        });
        if(!res.ok) throw new Error("HTTP "+res.status);
        showToast("Təşəkkürlər! Təklif qeydiyyata alındı.", "ok");
        setTimeout(close, 1500);
      }catch(err){
        console.error(err);
        showToast("Göndərmə alınmadı: "+err.message, "err");
        btn.disabled = false; btn.textContent = "Təklifi göndər";
      }
    }
    function showToast(msg, cls){
      const old = modal.querySelector(".dzl-toast"); if(old) old.remove();
      const t = el("div",{class:"dzl-toast "+(cls||"ok")});
      t.textContent = msg;
      modal.appendChild(t);
    }
    return { open };
  }

  // ─── Defensive: panic-close all overlays on ESC + sanity reset ──
  function panicClose(){
    // 1. Sidebar
    const sb = document.getElementById("sb");
    const ov = document.getElementById("ov");
    if(sb) sb.classList.remove("on");
    if(ov) ov.classList.remove("on");
    // 2. Kitab-modal
    const km = document.getElementById("kitab-modal");
    if(km) km.classList.remove("open");
    // 3. Search dropdown
    const sd = document.getElementById("search-drop");
    if(sd) sd.classList.remove("on");
    // 4. dzl backdrops
    document.querySelectorAll(".dzl-backdrop.open")
      .forEach(b => b.classList.remove("open"));
    // 5. Always restore body scroll
    document.body.style.overflow = "";
  }
  // ESC = panic close
  document.addEventListener("keydown", function(e){
    if(e.key === "Escape") panicClose();
  });
  // If after a navigation any overlay element somehow got stuck, clean on load
  window.addEventListener("pageshow", function(e){
    if(e.persisted) panicClose();   // bfcache restore
  });

  function init(){
    if(document.querySelector(".dzl-fab")) return;
    const fab = el("button",{class:"dzl-fab", type:"button", "aria-label":"Düzəliş et"}, "Düzəliş et");
    document.body.appendChild(fab);
    const m = buildModal();
    fab.addEventListener("click", m.open);

    // Wire per-term "Düzəlt" buttons on abbreviatur.html
    const termEditor = buildTermEditor();
    document.addEventListener("click", function(e){
      const btn = e.target.closest && e.target.closest(".dzl-row-btn");
      if(!btn) return;
      e.preventDefault();
      const term = btn.getAttribute("data-az") || btn.getAttribute("data-term") || "";
      const kind = btn.getAttribute("data-row-kind") || "term";
      termEditor.open(term, kind);
    });
  }

  if(document.readyState==="loading"){
    document.addEventListener("DOMContentLoaded", init);
  } else { init(); }
})();
