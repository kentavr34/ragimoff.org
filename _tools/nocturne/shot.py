"""Скриншоты через Chrome без окна (CDP). python shot.py URL W H OUTPREFIX y1 y2 ... ; y может быть 'sel:CSS' (прокрутка к элементу)."""
import asyncio, json, sys, subprocess, base64, time, urllib.request, os, tempfile
import websockets

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'


async def main():
    url, W, H, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    ys = sys.argv[5:]
    prof = tempfile.mkdtemp()
    p = subprocess.Popen([CHROME, '--headless=new', '--remote-debugging-port=9399', '--user-data-dir=' + prof, '--hide-scrollbars',
                          '--window-size=%d,%d' % (W, H), 'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(50):
        try:
            tabs = json.load(urllib.request.urlopen('http://127.0.0.1:9399/json'))
            ws_url = [t for t in tabs if t['type'] == 'page'][0]['webSocketDebuggerUrl']; break
        except Exception:
            time.sleep(.2)
    async with websockets.connect(ws_url, max_size=50_000_000) as ws:
        n = [0]
        async def cmd(m, **pr):
            n[0] += 1; i = n[0]
            await ws.send(json.dumps({'id': i, 'method': m, 'params': pr}))
            while True:
                r = json.loads(await ws.recv())
                if r.get('id') == i:
                    return r.get('result', {})
        mobile = W < 700 and not os.environ.get("NOMOB")
        await cmd('Emulation.setDeviceMetricsOverride', width=W, height=H, deviceScaleFactor=1, mobile=mobile)
        await cmd('Page.enable'); await cmd('Runtime.enable')
        await cmd('Page.navigate', url=url)
        await asyncio.sleep(float(os.environ.get("WAIT", "3.5")))
        if os.environ.get('EVAL'):
            r = await cmd('Runtime.evaluate', expression=os.environ['EVAL'], returnByValue=True, awaitPromise=True, timeout=600000)
            print('EVAL', json.dumps(r.get('result', {}).get('value'), ensure_ascii=False)[:3000])
        for k, y in enumerate(ys):
            if y.startswith('sel:'):
                expr = "(()=>{const e=document.querySelector(%r); return e? e.getBoundingClientRect().top+scrollY-90 : 0})()" % y[4:]
                yy = (await cmd('Runtime.evaluate', expression=expr, returnByValue=True))['result']['value']
            else:
                yy = float(y)
            cur = (await cmd('Runtime.evaluate', expression='scrollY', returnByValue=True))['result']['value']
            steps = 14
            for s in range(1, steps + 1):          # плавно, чтобы сработали обработчики прокрутки
                await cmd('Runtime.evaluate', expression='scrollTo(0,%f)' % (cur + (yy - cur) * s / steps))
                await asyncio.sleep(.07)
            await asyncio.sleep(2.2)
            shot = await cmd('Page.captureScreenshot', format='jpeg', quality=70)
            fn = '%s_%d.jpg' % (out, k)
            open(fn, 'wb').write(base64.b64decode(shot['data']))
            print(fn, int(yy))
    p.terminate()

asyncio.run(main())
