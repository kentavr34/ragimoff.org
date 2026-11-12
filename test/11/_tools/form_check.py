# -*- coding: utf-8 -*-
"""Проверка формы записи на всех видах страниц БЕЗ создания заявок: сетевой вызов в браузере подменён,
на сервер ничего не уходит. Проверяется, что форма на каждой странице собирает верную заявку:
код услуги для сервера оплаты, тему страницы в примечании, имя, телефон, язык; что без обязательных
полей (и без документа на программах обучения) отправки нет.
Запуск из test/11 (сервер: python -m http.server 8812 из корня сайта): python _tools/form_check.py
Код возврата 1 при расхождениях."""
import asyncio, json, sys, subprocess, time, urllib.request, os, tempfile, io, re
import websockets
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = os.environ.get("BASE", "http://localhost:8812/test/11/")
PORT = 9398
# страница → (ожидаемый код услуги — регулярное выражение, слово, которое должно быть в примечании на русском)
CASES = [
    ("index.html", r"^consult\|(kenan|samira|both)\|(online|offline)$", u"Панические"),
    ("consult.html?c=panik-ataklar", r"^consult\|kenan\|(online|offline)$", u"Панические"),
    ("consult.html?c=depressiya", r"^consult\|", u"Депрессия"),
    ("consult.html?c=sosial-fobiya", r"^consult\|", u"Социальная фобия"),
    ("consult.html?c=enurez", r"^consult\|kenan\|enurez-(first|course)$", u"энурез"),
    ("consult.html?c=aile-terapiyasi", r"^consult\|samira\|", u"Семейная"),
    ("consult.html?c=aile-usaq-terapiyasi", r"^consult\|samira\|", u"Семейная"),
    ("consult.html?c=tesvis-pozuntulari", r"^consult\|", u"Тревожные"),
    ("consult.html?c=okp", r"^consult\|", u"ОКР"),
    ("specialist.html?s=samira", r"^consult\|samira\|", u"Семейная"),
    ("specialist.html?s=kenan", r"^consult\|kenan\|", u""),
    ("article.html?a=enurez-2", r"^consult\|kenan\|enurez-", u"энурез"),
    ("program.html?p=general", u"^Общая психология$", u"Общая психология"),
    ("program.html?p=clinical", u"^Клиническая психология$", u"Клиническая"),
    ("program.html?p=practicum", u"^Практикум по психотерапии$", u"Практикум"),
    ("program.html?p=psychodiagnostics", r"^short-psixodiaqnostika$", u"Психодиагностика"),
    ("program.html?p=cbt", r"^short-kdt$", u"КПТ"),
    ("program.html?p=psychoanalysis", r"^short-psixoanaliz$", u"Психоанализ"),
    ("program.html?p=family", r"^short-aile$", u"Семейная"),
]
JS = r"""
(async () => {
  const out = { sent: [] };
  window.fetch = async (u, o) => { out.sent.push({ url: String(u), body: o && o.body ? JSON.parse(o.body) : null }); return { ok: true, json: async () => ({ ok: true }) }; };
  const form = document.querySelector('#regBox form'); if (!form) return { fail: 'нет формы' };
  const go = async () => { form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true })); await new Promise(r => setTimeout(r, 500)); };
  await go(); out.emptySent = out.sent.length;                       /* пустая форма уходить не должна */
  const set = (n, v) => { const e = document.querySelector('#regBox [name="' + n + '"]'); if (e) { e.value = v; e.dispatchEvent(new Event('input', { bubbles: true })); } return !!e; };
  set('fname', 'Проверка'); set('lname', 'Формы'); set('phone', '+994 50 000 00 00'); set('company', 'Проверка');
  const idf = document.querySelector('#regBox [name="idcard"]'); out.needsDoc = !!idf;
  if (idf) { await go(); out.noDocSent = out.sent.length; const dt = new DataTransfer(); dt.items.add(new File(['x'], 'id.jpg', { type: 'image/jpeg' })); idf.files = dt.files; }
  await go();
  out.msg = (document.querySelector('#regBox .reg__msg') || {}).textContent || '';
  return out;
})()
"""


async def main():
    prof = tempfile.mkdtemp()
    p = subprocess.Popen([CHROME, "--headless=new", "--remote-debugging-port=%d" % PORT, "--user-data-dir=" + prof, "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ws_url = None
    for _ in range(60):
        try:
            tabs = json.load(urllib.request.urlopen("http://127.0.0.1:%d/json" % PORT))
            ws_url = [t for t in tabs if t["type"] == "page"][0]["webSocketDebuggerUrl"]
            break
        except Exception:
            time.sleep(.2)
    bad = 0
    try:
        async with websockets.connect(ws_url, max_size=80_000_000) as ws:
            n = [0]

            async def cmd(m, **pr):
                n[0] += 1
                i = n[0]
                await ws.send(json.dumps({"id": i, "method": m, "params": pr}))
                while True:
                    r = json.loads(await ws.recv())
                    if r.get("id") == i:
                        return r.get("result", {})

            await cmd("Page.enable"); await cmd("Runtime.enable")
            await cmd("Emulation.setDeviceMetricsOverride", width=1366, height=800, deviceScaleFactor=1, mobile=False)
            await cmd("Page.navigate", url=BASE + "contact.html")
            await asyncio.sleep(1.2)
            await cmd("Runtime.evaluate", expression="localStorage.setItem('r11_lang','ru')")
            for pg, svc, word in CASES:
                await cmd("Page.navigate", url=BASE + pg)
                await asyncio.sleep(2.0)
                r = await cmd("Runtime.evaluate", expression=JS, returnByValue=True, awaitPromise=True)
                o = r.get("result", {}).get("value") or {"fail": "нет ответа страницы"}
                v = []
                if o.get("fail"):
                    v.append(o["fail"])
                else:
                    if o.get("emptySent"): v.append("пустая форма отправилась")
                    if o.get("needsDoc") and o.get("noDocSent"): v.append("программа обучения ушла без документа")
                    reqs = [s for s in o["sent"] if "/api/training-reg" in s["url"]]
                    if len(reqs) != 1:
                        v.append("заявок %d вместо одной (%s)" % (len(reqs), o.get("msg", "")[:60]))
                    else:
                        b = reqs[0]["body"]
                        if not re.search(svc, b.get("service", "")): v.append("код услуги «%s» не тот" % b.get("service"))
                        if word and word.lower() not in (b.get("note", "") or "").lower(): v.append("в примечании нет темы страницы: «%s»" % b.get("note"))
                        if b.get("lang") != "ru" or not b.get("fname") or not b.get("phone") or b.get("type") != "registration": v.append("неполная заявка")
                        if o.get("needsDoc") and not b.get("attachments"): v.append("документ не приложен")
                        info = "%s · %s" % (b.get("service"), (b.get("note") or "")[:70])
                    extra = [s["url"] for s in o["sent"] if "/api/training-reg" not in s["url"]]
                    if extra: v.append("лишние вызовы: " + ", ".join(extra)[:120])
                bad += 1 if v else 0
                print(("✗ " if v else "ok ") + pg.ljust(42) + (" ‖ ".join(v) if v else info))
    finally:
        p.terminate()
    print("ПРОВЕРЕНО форм: %d, РАСХОЖДЕНИЙ: %d (на сервер ничего не отправлялось)" % (len(CASES), bad))
    sys.exit(1 if bad else 0)

asyncio.run(main())
