// ═══════════════════════════════════════════════
//  RAGIMOFF — Backend (Google Apps Script)
//  Принимает формы с сайта → Google Sheets + Telegram
// ═══════════════════════════════════════════════

// ─────────────────────────────────────────────────────────────
//  ДОСТУПЫ
//
//  Токен бота лежит здесь открытым текстом — решение владельца
//  2026-08-17. Репозиторий публичный, и это принято сознательно:
//  @clodea_bot ничего не делает, кроме отправки Кенану уведомления о
//  регистрации с сайта. С клиентами он не работает, данных не хранит,
//  доступа никуда не даёт. Перевод репозитория в приватный требует
//  платного плана и того не стоит; в перспективе сайт переедет на
//  собственный сервер.
//
//  ЧТО БУДЕТ ДАЛЬШЕ. Telegram сам сканирует публичные репозитории и
//  отзывает найденные токены — именно поэтому предыдущий перестал
//  работать, это была утечка, а не взлом. Значит и этот, скорее всего,
//  однажды отзовут. Признак: заявки падают в таблицу, но в Telegram не
//  приходят, а на листе «Errors» появляется строка с кодом 401.
//  Что делать: взять новый токен у @BotFather и вписать его в
//  Apps Script → Настройки проекта → Свойства скрипта, ключ TG_TOKEN.
//  Свойства имеют приоритет над кодом, менять файл не нужно.
// ─────────────────────────────────────────────────────────────
const PROPS      = PropertiesService.getScriptProperties();
const TG_TOKEN   = PROPS.getProperty('TG_TOKEN')   || '8627472656:AAGcRVoZL_yb6WU5IIombnt5ZPwAsCK__aQ';
const TG_CHAT_ID = PROPS.getProperty('TG_CHAT_ID') || '254450353';
const SHEET_ID   = PROPS.getProperty('SHEET_ID')   || '1ucYNu6mjcDzUE1g4rVIQi__56qUhaMjcG9r0JorV2rI';

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const type = data.type || 'registration';

    if (type === 'review') {
      saveReview(data);
    } else {
      saveRegistration(data);
    }

    return json({ ok: true });
  } catch (err) {
    return json({ ok: false, error: String(err) });
  }
}

function doGet() {
  return json({ ok: true, service: 'ragimoff-backend' });
}

// ── РЕГИСТРАЦИЯ ──
function saveRegistration(d) {
  const sheet = getSheet('Registrations', [
    'Дата', 'Имя', 'Фамилия', 'Телефон', 'Email', 'Программа', 'Комментарий', 'Источник'
  ]);
  const row = [
    new Date(),
    d.fname || '', d.lname || '', d.phone || '', d.email || '',
    d.service || '', d.note || '', d.source || ''
  ];
  sheet.appendRow(row);

  const msg =
    '🎓 <b>Новая регистрация</b>\n\n' +
    '👤 ' + esc(d.fname) + ' ' + esc(d.lname || '') + '\n' +
    '📞 ' + esc(d.phone) + '\n' +
    '✉️ ' + esc(d.email || '—') + '\n' +
    '📚 ' + esc(d.service || '—') + '\n' +
    '💬 ' + esc(d.note || '—') + '\n' +
    '🔗 ' + esc(d.source || '—');
  sendTelegram(msg);
}

// ── ОТЗЫВ (модерация) ──
function saveReview(d) {
  const sheet = getSheet('Reviews', [
    'Дата', 'Имя', 'Программа', 'Звёзды', 'Текст', 'Email', 'Статус'
  ]);
  sheet.appendRow([
    new Date(),
    d.name || '', d.program || '', d.rating || '',
    d.text || '', d.email || '', 'ожидает модерации'
  ]);

  const msg =
    '⭐ <b>Новый отзыв — требует модерации</b>\n\n' +
    '👤 ' + esc(d.name) + '\n' +
    '📚 ' + esc(d.program || '—') + '\n' +
    '⭐ ' + esc(d.rating || '—') + '/5\n' +
    '✉️ ' + esc(d.email || '—') + '\n\n' +
    '💬 ' + esc(d.text || '');
  sendTelegram(msg);
}

// ── HELPERS ──
function getSheet(name, headers) {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  let sh = ss.getSheetByName(name);
  if (!sh) {
    sh = ss.insertSheet(name);
    sh.appendRow(headers);
    sh.getRange(1, 1, 1, headers.length).setFontWeight('bold');
  }
  return sh;
}

// Ошибка отправки ЗАПИСЫВАЕТСЯ, а не глотается.
// Раньше стоял голый muteHttpExceptions: true без разбора ответа —
// Telegram мог отвечать 401 «Unauthorized» на отозванный токен, а
// скрипт молчал. Заявки при этом падали в таблицу, и со стороны
// выглядело, будто «всё работает, но бот не пишет».
function sendTelegram(text) {
  if (!TG_TOKEN) {
    logProblem('TG_TOKEN не задан в свойствах скрипта');
    return false;
  }
  try {
    const res = UrlFetchApp.fetch('https://api.telegram.org/bot' + TG_TOKEN + '/sendMessage', {
      method: 'post',
      payload: { chat_id: TG_CHAT_ID, text: text, parse_mode: 'HTML' },
      muteHttpExceptions: true
    });
    const code = res.getResponseCode();
    if (code !== 200) {
      logProblem('Telegram ответил ' + code + ': ' + res.getContentText().slice(0, 300));
      return false;
    }
    return true;
  } catch (err) {
    logProblem('Сбой запроса к Telegram: ' + String(err));
    return false;
  }
}

// Проблемы доставки видно в самой таблице — отдельный лист «Errors».
function logProblem(message) {
  try {
    const sh = getSheet('Errors', ['Дата', 'Проблема']);
    sh.appendRow([new Date(), message]);
  } catch (e) {
    console.error('logProblem: ' + e);
  }
  console.error(message);
}

// Проверка доставки без заполнения формы: запустить руками из редактора.
function testTelegram() {
  const ok = sendTelegram('🔧 Проверка связи с сайтом ragimoff.org');
  console.log(ok ? 'Telegram принял сообщение' : 'НЕ доставлено — смотри лист «Errors»');
}

function esc(s) {
  return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
