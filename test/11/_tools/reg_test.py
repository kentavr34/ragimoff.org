"""Проверка формы записи на живой странице: одна тестовая заявка на консультацию (имя TEST), до оплаты не доходит.
Заполняет форму как человек (выбор по умолчанию), нажимает «Записаться», записывает ответы сервера и адрес, куда ведёт оплата.
Запуск: python reg_test.py [адрес страницы]   — ТОЛЬКО по слову владельца: создаёт настоящую запись на сервере."""
import asyncio, json, sys, subprocess, time, urllib.request, tempfile
import websockets

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = sys.argv[1] if len(sys.argv) > 1 else 'https://ragimoff.org/test/11/'


async def main():
    prof = tempfile.mkdtemp()
    p = subprocess.Popen([CHROME, '--headless=new', '--remote-debugging-port=9397', '--user-data-dir=' + prof, '--window-size=1280,900', 'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ws_url = None
    for _ in range(60):
        try:
            tabs = json.load(urllib.request.urlopen('http://127.0.0.1:9397/json'))
            ws_url = [t for t in tabs if t['type'] == 'page'][0]['webSocketDebuggerUrl']; break
        except Exception:
            time.sleep(.2)
    log, pending = [], {}
    async with websockets.connect(ws_url, max_size=80_000_000) as ws:
        n = [0]
        events = []

        async def cmd(m, **pr):
            n[0] += 1; i = n[0]
            await ws.send(json.dumps({'id': i, 'method': m, 'params': pr}))
            while True:
                r = json.loads(await ws.recv())
                if r.get('id') == i:
                    return r.get('result', {})
                events.append(r)

        async def pump(sec):
            end = time.time() + sec
            while time.time() < end:
                try:
                    r = json.loads(await asyncio.wait_for(ws.recv(), timeout=.5))
                    events.append(r)
                except asyncio.TimeoutError:
                    pass

        async def ev(expr):
            return (await cmd('Runtime.evaluate', expression=expr, returnByValue=True, awaitPromise=True)).get('result', {}).get('value')

        await cmd('Page.enable'); await cmd('Runtime.enable'); await cmd('Network.enable')
        await cmd('Fetch.enable', patterns=[{'urlPattern': '*epoint.az*', 'requestStage': 'Request'}])     # на платёжную страницу не переходим: останавливаем запрос
        await cmd('Page.navigate', url=URL)
        await pump(6)
        state = await ev("""(async () => {
          document.querySelector('[data-lang-btn=ru]').click(); await new Promise(r => setTimeout(r, 500));
          const b = document.querySelector('#regBox'); if (!b) return 'нет формы';
          const set = (n, v) => { const i = b.querySelector('input[name=' + n + ']'); i.value = v; i.dispatchEvent(new Event('input', { bubbles: true })); };
          set('fname', 'TEST'); set('lname', 'TEST'); set('phone', '+994 70 000 00 00');
          const st = { kind: (b.querySelector('.reg__kind.is-on') || {}).textContent, chips: [...b.querySelectorAll('.chip.is-on')].map(c => c.textContent), price: (b.querySelector('.reg__p') || {}).textContent, btn: b.querySelector('.reg__go').textContent };
          b.querySelector('form').requestSubmit(); return st; })()""")
        print('ФОРМА ПЕРЕД ОТПРАВКОЙ:', json.dumps(state, ensure_ascii=False))
        await pump(14)
        for e in events:
            m, pr = e.get('method'), e.get('params', {})
            if m == 'Network.requestWillBeSent' and ('api.ragimoff.org' in pr['request']['url'] or 'epoint' in pr['request']['url']):
                pending[pr['requestId']] = pr['request']['url']
                print('ЗАПРОС:', pr['request']['method'], pr['request']['url'][:110], '|', (pr['request'].get('postData') or '')[:260])
            if m == 'Fetch.requestPaused':
                print('ОСТАНОВЛЕН ПЕРЕХОД НА ОПЛАТУ:', pr['request']['url'][:160])
            if m == 'Network.responseReceived' and pr['requestId'] in pending:
                log.append((pr['requestId'], pr['response']['status']))
        for rid, status in log:
            try:
                body = await cmd('Network.getResponseBody', requestId=rid)
                txt = body.get('body', '')[:500]
            except Exception as ex:
                txt = '(тело недоступно: %s)' % ex
            print('ОТВЕТ', status, pending[rid][:70], '→', txt)
        msg = await ev("(() => { try { const m = document.querySelector('#regBox .reg__msg'); return { url: location.href.slice(0, 120), msg: m && !m.hidden ? m.textContent : '', pay: (document.querySelector('#regBox .reg__pay') || {}).innerText || '' }; } catch (e) { return String(e); } })()")
        print('СТРАНИЦА ПОСЛЕ ОТПРАВКИ:', json.dumps(msg, ensure_ascii=False))
    p.terminate()

asyncio.run(main())
