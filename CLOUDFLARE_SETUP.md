# Cloudflare Worker setup — Term Corrections backend

**Время:** 7–10 минут, одноразово.
**Стоимость:** 0₼ (free tier: 100 000 запросов в день — нам нужно ~50).

---

## Шаг 1: GitHub Personal Access Token (PAT)

1. Откройте https://github.com/settings/tokens → **"Generate new token"** → **"Fine-grained personal access token"**
2. Заполните:
   - **Token name:** `klinik-corrections-worker`
   - **Expiration:** `No expiration` (или 1 year)
   - **Repository access:** **Only select repositories** → выберите `kentavr34/ragimoff.org`
   - **Permissions → Repository permissions:**
     - **Contents** → **Read and write** ✓
     - (всё остальное — Read only или None)
3. Внизу → **"Generate token"**
4. **Скопируйте токен** (начинается с `github_pat_...`) — он покажется ОДИН раз
5. Сохраните где-то временно (Notes/блокнот)

---

## Шаг 2: Cloudflare аккаунт + Worker

### Создать аккаунт (если ещё нет)
1. https://dash.cloudflare.com/sign-up → e-mail + пароль → подтвердить email

### Создать Worker
1. В dashboard слева: **Workers & Pages** → **Create**
2. Кнопка **"Create Worker"** → название: `klinik-corrections` → **Deploy**
3. После deploy откроется страница воркера. Кликните **"Edit code"** (или ⚙ → Edit code)
4. В редакторе:
   - Удалите весь дефолтный код
   - Откройте файл `_workers/corrections-worker.js` из этого репо
   - Скопируйте всё содержимое
   - Вставьте в редактор Cloudflare
   - Сверху справа: **"Save and Deploy"** → подтвердить

### Добавить секрет (GitHub токен)
1. Вернитесь на главную страницу воркера (стрелка ← вверху)
2. Слева → **Settings** → **Variables**
3. Прокрутите вниз до **"Add variable"** в секции **Environment Variables**
4. Нажмите **"Add variable"**:
   - **Variable name:** `GH_TOKEN`
   - **Value:** ваш `github_pat_...` (из Шага 1)
   - **Encrypt** → ✓ (это превратит её в Secret — невидимую)
5. **Save and deploy**

### Узнать URL воркера
1. На странице воркера сверху написан URL:
   ```
   https://klinik-corrections.<вашаккаунт>.workers.dev
   ```
2. **Скопируйте и пришлите мне** — я подставлю в `duzelis.js`.

---

## Шаг 3: Проверка

После Шага 2.4 и получения URL — откройте URL в браузере. Должно показать:
```json
{"ok":false,"error":"POST only"}
```

Это **успех** — endpoint жив. POST-запросы будут работать.

Если показывается **Cloudflare login** или ошибка `Cloudflare Worker is not deployed` — что-то пошло не так на шаге 2.3.

---

## Шаг 4: Я обновляю сайт

Когда пришлёте URL, я:
1. Заменю `__CLOUDFLARE_WORKER_URL__` в `duzelis.js` на ваш URL
2. Закоммичу, запушу в `main`
3. GitHub Pages деплоит — ~1 минута
4. Можете тестировать на live-сайте

---

## Шаг 5: Workflow с этого момента

```
Студент жмёт ✎ Düzəlt на сайте
  → POST → Cloudflare Worker → коммит в _corrections/PENDING.json
  ↓
Вы открываете https://github.com/kentavr34/ragimoff.org/blob/main/_corrections/PENDING.json
  ↓
Жмёте ✏ (Edit), меняете "status": "pending" → "status": "approved" у нужных
  ↓
Commit (1 кнопка)
  ↓
В следующей сессии я запускаю:
  python _term_sync.py
  → читает PENDING.json
  → применяет approved правки во всех 157 файлах
  → помечает "status": "applied"
  → коммитит
  → пересборка nav/TOC/DOCX
  → пуш в main
```

---

## Структура `_corrections/PENDING.json`

```json
[
  {
    "ts": "2026-05-15T20:33:14.123Z",
    "status": "pending",           ← измените на "approved" чтобы применить
    "original": "ANOREKSİYA NERVOZA",
    "proposed": "SİNİR ANOREKSİYASI",
    "note": "AzPA göstəricisi 2024",
    "url": "https://ragimoff.org/klinik-psixiatriya/09-6B8-qida-qebulu.html",
    "rowKind": "term",
    "ua": "Mozilla/5.0..."
  }
]
```

Возможные статусы:
- `pending` — новая, не рассмотрена
- `approved` — одобрено, ждёт применения
- `applied` — применено (автоматически, агентом)
- `rejected` — отклонено (необязательно, можно просто оставить pending или удалить запись)

---

## Безопасность

- Токен `GH_TOKEN` хранится **только** в Cloudflare как зашифрованный secret. В коде JS его нет.
- Worker может только **читать и писать** файлы в репо `kentavr34/ragimoff.org` (через fine-grained PAT).
- Worker открыт для всех (`Access-Control-Allow-Origin: *`) — это OK, потому что только commit в PENDING.json возможен. Никаких других действий не позволяется.
- Spam-protection: если кто-то начнёт спамить — можно добавить rate-limiting в Worker (Cloudflare free tier даёт `request.cf` с IP).

---

## Откат на старый GAS (если что-то сломается)

В `duzelis.js`:
```javascript
const ENDPOINT = "https://script.google.com/macros/s/AKfycb.../exec";  // вернуть GAS URL
```
Закомичено. Готов вернуть назад в любой момент.
