// ═══════════════════════════════════════════════
//  RAGIMOFF — Backend (Google Apps Script)
//  Принимает формы с сайта → Google Sheets + Telegram
// ═══════════════════════════════════════════════

const TG_TOKEN   = '8627472656:AAEv9hImWmxwq5HuxuemRWTZywRJEqa63cU';
const TG_CHAT_ID = '254450353';
const SHEET_ID   = '1ucYNu6mjcDzUE1g4rVIQi__56qUhaMjcG9r0JorV2rI';

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

function sendTelegram(text) {
  UrlFetchApp.fetch('https://api.telegram.org/bot' + TG_TOKEN + '/sendMessage', {
    method: 'post',
    payload: { chat_id: TG_CHAT_ID, text: text, parse_mode: 'HTML' },
    muteHttpExceptions: true
  });
}

function esc(s) {
  return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
