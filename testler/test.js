/* Тест для студентов: одна страница = один тест.
   Кенан 03.11.2026: по ссылке, без пароля; ввёл имя и фамилию → «Testə başla» →
   все вопросы на одной странице → «Nəticəni göndər» → результат на сервере и в админке.

   Вопросы приходят с сервера (api.ragimoff.org/api/test/<slug>) БЕЗ ключа ответов:
   сайт публичный, ключ в HTML/JS увидел бы любой студент. Проверка — на сервере.
   Слаг теста — в <body data-test="…">. Новый тест = копия страницы с другим слагом.

   Черновик (имя + ответы) хранится в localStorage: случайная перезагрузка
   страницы не стирает ответы. После отправки черновик удаляется. */
(function () {
  'use strict';

  var API = 'https://api.ragimoff.org';
  try {   // локальная проверка: ?api=http://127.0.0.1:9631 (только на localhost)
    var o = new URLSearchParams(location.search).get('api');
    if (o && /^(localhost|127\.0\.0\.1)$/.test(location.hostname)) API = o;
  } catch (e) {}

  var SLUG = document.body.getAttribute('data-test') || '';
  var KEY = 'ragimoff_test_' + SLUG;
  var LETTERS = 'ABCDEFGH';

  var T = {
    start: 'Testə başla', send: 'Nəticəni göndər', sending: 'Göndərilir…',
    needName: 'Zəhmət olmasa adınızı və soyadınızı yazın.',
    loadErr: 'Test yüklənmədi. İnternet bağlantısını yoxlayıb səhifəni yeniləyin.',
    sendErr: 'Nəticə göndərilmədi. İnternet bağlantısını yoxlayıb yenidən «Nəticəni göndər» düyməsini basın — cavablarınız saxlanılıb.',
    unanswered: 'Cavablandırılmayan suallar: ',
    answered: 'Cavablandırılıb', of: '/', q: 'Sual',
    student: 'Tələbə: ',
    doneT: 'Təşəkkür edirik!',
    doneM: 'Nəticəniz göndərildi və qeydə alındı.',
    score: 'Düzgün cavablar: '
  };

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var app = $('#test-app');
  var test = null;            // {title, questions:[{n,q,options:[{k,t}]}]}
  var draft = load() || {};   // {fname, lname, started, answers:{n:key}, done}

  function load() { try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { return null; } }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(draft)); } catch (e) {} }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  if (draft.done) { showDone(draft.done); return; }

  var loading = fetch(API + '/api/test/' + encodeURIComponent(SLUG))
    .then(function (r) { return r.json(); })
    .then(function (d) {
      if (!d || !d.ok) throw new Error((d && d.error) || 'load');
      test = d;
      return d;
    });

  if (draft.fname && draft.lname && draft.started) {
    loading.then(showQuestions, loadFailed);
  } else {
    showIntro();
  }

  function showIntro() {
    app.innerHTML =
      '<form class="t-card" id="t-intro" novalidate>' +
      '<label class="t-field"><span>Ad</span><input name="fname" autocomplete="given-name" required></label>' +
      '<label class="t-field"><span>Soyad</span><input name="lname" autocomplete="family-name" required></label>' +
      '<button class="t-btn" type="submit">' + T.start + '</button>' +
      '<p class="t-msg" role="alert"></p></form>';
    var f = $('#t-intro');
    f.fname.value = draft.fname || '';
    f.lname.value = draft.lname || '';
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var fn = f.fname.value.trim(), ln = f.lname.value.trim();
      f.fname.parentNode.classList.toggle('is-bad', !fn);
      f.lname.parentNode.classList.toggle('is-bad', !ln);
      if (!fn || !ln) { $('.t-msg', f).textContent = T.needName; return; }
      draft.fname = fn; draft.lname = ln;
      draft.started = draft.started || Date.now();
      draft.answers = draft.answers || {};
      save();
      var btn = $('button', f);
      btn.disabled = true;
      loading.then(showQuestions, function () { btn.disabled = false; loadFailed(); });
    });
  }

  function loadFailed() {
    var m = $('.t-msg') || app.appendChild(Object.assign(document.createElement('p'), { className: 't-msg' }));
    m.textContent = T.loadErr;
  }

  function showQuestions() {
    var total = test.questions.length;
    var html =
      '<p class="t-who">' + T.student + '<b>' + esc(draft.fname) + ' ' + esc(draft.lname) + '</b></p>' +
      '<div class="t-progress"><span>' + T.answered + ' <b id="t-cnt">0</b>' + T.of + total + '</span>' +
      '<div class="t-bar"><i id="t-bar"></i></div></div><form id="t-form" novalidate>';
    test.questions.forEach(function (q) {
      html += '<fieldset class="t-q" id="q' + q.n + '"><legend><small>' + T.q + ' ' + q.n + ' / ' + total +
        '</small><span>' + esc(q.q) + '</span></legend>';
      q.options.forEach(function (o, i) {
        var chk = draft.answers[q.n] === o.k ? ' checked' : '';
        html += '<label class="t-opt"><input type="radio" name="q' + q.n + '" value="' + esc(o.k) + '"' + chk + '>' +
          '<span class="l">' + LETTERS[i] + '</span><span class="x">' + esc(o.t) + '</span></label>';
      });
      html += '</fieldset>';
    });
    html += '<div class="t-send"><button class="t-btn" type="submit">' + T.send + '</button>' +
      '<p class="t-msg" role="alert"></p></div></form>';
    app.innerHTML = html;

    var form = $('#t-form');
    form.addEventListener('change', function (e) {
      var m = /^q(\d+)$/.exec(e.target.name || '');
      if (!m) return;
      draft.answers[m[1]] = e.target.value;
      save();
      $('#q' + m[1]).classList.remove('is-bad');
      count();
    });
    form.addEventListener('submit', submit);
    count();
    window.scrollTo(0, 0);
  }

  function count() {
    var total = test.questions.length;
    var n = test.questions.filter(function (q) { return draft.answers[q.n]; }).length;
    $('#t-cnt').textContent = n;
    $('#t-bar').style.width = (100 * n / total) + '%';
  }

  function submit(e) {
    e.preventDefault();
    var msg = $('.t-send .t-msg'), btn = $('.t-send .t-btn');
    var missing = test.questions.filter(function (q) { return !draft.answers[q.n]; });
    test.questions.forEach(function (q) { $('#q' + q.n).classList.toggle('is-bad', !draft.answers[q.n]); });
    if (missing.length) {
      msg.textContent = T.unanswered + missing.map(function (q) { return q.n; }).join(', ');
      $('#q' + missing[0].n).scrollIntoView({ behavior: 'smooth', block: 'center' });
      return;
    }
    btn.disabled = true; btn.textContent = T.sending; msg.textContent = '';
    fetch(API + '/api/test/' + encodeURIComponent(SLUG) + '/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },   // без preflight
      body: JSON.stringify({ fname: draft.fname, lname: draft.lname, answers: draft.answers,
                             started: draft.started, source: location.href })
    }).then(function (r) { return r.json(); }).then(function (d) {
      if (!d || !d.ok) throw new Error((d && d.error) || 'send');
      draft = { done: { name: draft.fname + ' ' + draft.lname, score: d.score, total: d.total, percent: d.percent } };
      save();
      showDone(draft.done);
    }).catch(function () {
      btn.disabled = false; btn.textContent = T.send; msg.textContent = T.sendErr;
    });
  }

  function showDone(d) {
    app.innerHTML = '<div class="t-card t-done"><div class="ico">&#10004;</div>' +
      '<h2>' + T.doneT + '</h2><p><b>' + esc(d.name) + '</b></p><p>' + T.doneM + '</p>' +
      (typeof d.score === 'number'
        ? '<p class="score">' + T.score + d.score + ' / ' + d.total + ' (' + d.percent + '%)</p>' : '') +
      '</div>';
    window.scrollTo(0, 0);
  }
})();
