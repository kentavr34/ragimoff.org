# -*- coding: utf-8 -*-
"""Кенан 11.11.2026 («да»): оплата тренингов/консультаций отмечается оплаченной, Telegram получает
подтверждение или отказ, язык страницы ePoint — язык клиента, энурез 50/500, понятная заявка."""
import io, shutil, time, py_compile, sys
ST = time.strftime("%Y%m%d_%H%M%S")


def rep(s, a, b, n=1):
    assert s.count(a) == n, "ожидалось %d, найдено %d: %s" % (n, s.count(a), a[:70])
    return s.replace(a, b)


E_ = "/opt/ragimoff-api/epoint_routes.py"
A_ = "/opt/ragimoff-api/app.py"
e = io.open(E_, encoding="utf-8").read()
a = io.open(A_, encoding="utf-8").read()
if "_training_result" in e:
    print("уже применено")
    sys.exit(0)

# 1. язык страницы ePoint
e = rep(e, 'def _mk_payment(amount, order_id, part_no, nparts, installment=None):',
        'def _mk_payment(amount, order_id, part_no, nparts, installment=None, lang="az"):')
e = rep(e, '''               "description": _part_desc(order_id, part_no, nparts),
               "currency": "AZN", "language": "az",''',
        '''               "description": _part_desc(order_id, part_no, nparts),
               "currency": "AZN", "language": (lang if lang in ("az", "ru", "en") else "az"),''')
e = rep(e, '''def training_checkout(name, phone, program, order_id=None, notify=True,
                      mode="prepay", folder=""):''',
        '''def training_checkout(name, phone, program, order_id=None, notify=True,
                      mode="prepay", folder="", lang="az"):''')
e = rep(e, '''        res = _mk_payment(parts[0], order_id, 1, len(parts),
                          installment=(mode == "installment"))''',
        '''        res = _mk_payment(parts[0], order_id, 1, len(parts),
                          installment=(mode == "installment"), lang=lang)''')
e = rep(e, '''    r = training_checkout(name, phone, program, mode=mode, folder=folder)''',
        '''    lang = str(d.get("lang") or "az").strip().lower()[:2]
    r = training_checkout(name, phone, program, mode=mode, folder=folder, lang=lang)''')

# 2. заказ помнит папку заявки (иначе подтверждению некуда лечь)
e = rep(e, '''    # номер заказа и способ — к заявке (training_regs), чтобы Кенан видел связь
    if folder:
        try:''', '''    # номер заказа и способ — к заявке (training_regs), чтобы Кенан видел связь
    if folder:
        _remember_folder(order_id, folder)
        try:''')

# 3. энурез (Кенан 11.11.2026): первичная консультация 50, курс лечения 500
e = rep(e, '''    if len(parts) == 3 and parts[0] == "consult":     # консультация, 1 час (тот же тариф, Кенан 08.11)
''', '''    if len(parts) == 3 and parts[0] == "consult" and parts[2] in ENUREZ_PRICES:
        return ENUREZ_PRICES[parts[2]]                # энурез: своя цена (Кенан 11.11.2026)
    if len(parts) == 3 and parts[0] == "consult":     # консультация, 1 час (тот же тариф, Кенан 08.11)
''')
e = rep(e, '''INDIVIDUAL_MIN_HOURS = 20
''', '''INDIVIDUAL_MIN_HOURS = 20
# Лечение ночного энуреза (Кенан 11.11.2026): первичная консультация 50 AZN, курс лечения 500 AZN.
# Код из формы: "consult|kenan|enurez-first" / "consult|kenan|enurez-course".
ENUREZ_PRICES = {"enurez-first": 50, "enurez-course": 500}
''')

# 4. подтверждение: имя клиента в сообщении
e = rep(e, 'def _save_payment_proof(order_id, amount, status, trn, payload):',
        'def _save_payment_proof(order_id, amount, status, trn, payload, who=""):')
e = rep(e, '''        _tg_notify("\\n".join([
            "\\U0001F7E2 ОПЛАТА ПОДТВЕРЖДЕНА — ragimoff.org",
            "Заказ: %s" % order_id,''', '''        _tg_notify("\\n".join(filter(None, [
            "\\U0001F7E2 ОПЛАТА ПОДТВЕРЖДЕНА — ragimoff.org",
            who,
            "Заказ: %s" % order_id,''')
e = rep(e, '''            "Документы и подтверждение: %s" % folder,
        ]))''', '''            "Документы и подтверждение: %s" % folder,
        ])))''')

# 5. ответ ePoint по тренингам и консультациям
e = rep(e, '''    # Epoint ждёт именно такой ответ, чтобы считать уведомление принятым
''', '''    try:
        _training_result(order_id, amount, status, trn, payload)
    except Exception as _e:
        print("ОШИБКА отметки оплаты тренинга:", _e, flush=True)

    # Epoint ждёт именно такой ответ, чтобы считать уведомление принятым
''')
e = rep(e, '''def register(app):
    """Подключить маршруты к приложению."""''', '''def _training_result(order_id, amount, status, trn, payload):
    """Тренинг/консультация (TR-, TRI-, KS-): отметить заявку оплаченной, положить
    подтверждение к документам, сообщить Кенану. Повтор того же уведомления — молчим.
    Кенан 11.11.2026: «сервер должен получать подтверждение оплаты»."""
    base = re.sub(r"-P\\d+$", "", str(order_id))
    if not base.startswith(("TR-", "TRI-", "KS-")):
        return
    ok = str(status).upper() in ("SUCCESS", "PAID", "APPROVED", "OK")
    con = _db()
    n = con.execute("SELECT COUNT(*) FROM epoint_payments WHERE order_id=? AND status=?",
                    (order_id, status)).fetchone()[0]
    con.close()
    if n > 1:
        return
    folder = _folder_of(base)
    who = ""
    if folder:
        con = sqlite3.connect(DB_PATH, timeout=20)
        try:
            row = con.execute("SELECT fname, lname, phone, service, pay_form FROM training_regs"
                              " WHERE folder=?", (folder,)).fetchone()
            if row:
                who = "%s %s, %s — %s" % (row[0] or "", row[1] or "", row[2] or "", row[3] or "")
                mark = " — ÖDƏNİLİB" if ok else " — ödəniş keçmədi"
                if ok or "ÖDƏNİLİB" not in (row[4] or ""):
                    pf = re.sub(r" — (ÖDƏNİLİB|ödəniş keçmədi).*$", "", row[4] or "ePoint")
                    con.execute("UPDATE training_regs SET pay_form=? WHERE folder=?",
                                ((pf + mark + " %s AZN" % amount)[:200], folder))
            con.commit()
        finally:
            con.close()
    if ok:
        if not _save_payment_proof(order_id, amount, status, trn, payload, who=who):
            _tg_notify("\\n".join(filter(None, [
                "\\U0001F7E2 ОПЛАТА ПОДТВЕРЖДЕНА — ragimoff.org", who,
                "Заказ: %s" % order_id, "Сумма: %s AZN" % amount,
                "Код операции: %s" % (trn or "—")])))
    else:
        _tg_notify("\\n".join(filter(None, [
            "\\U0001F534 ОПЛАТА НЕ ПРОШЛА — ragimoff.org", who,
            "Заказ: %s" % order_id, "Сумма: %s AZN" % amount,
            "Статус ePoint: %s" % (status or "—")])))


def register(app):
    """Подключить маршруты к приложению."""''')

# 6. понятная заявка в Telegram
a = rep(a, '''        "\\U0001F393 Заявка на ТРЕНИНГ — ragimoff.org",
        f"Имя: {row['fname']} {row['lname']}".strip(),''',
        '''        ("\\U0001FA7A Заявка на КОНСУЛЬТАЦИЮ — ragimoff.org" if row["service"].startswith("consult|")
         else "\\U0001F393 Заявка на ТРЕНИНГ — ragimoff.org"),
        "(ещё не оплачено — об оплате придёт отдельное сообщение)",
        f"Имя: {row['fname']} {row['lname']}".strip(),''')
a = rep(a, '''        f"Программа: {row['service']}" if row["service"] else "",
        f"Оплата: {pay_form}" if pay_form else "",''',
        '''        f"Программа: {row['service']}" if row["service"] else "",
        f"Детали: {row['note']}" if row["note"] else "",
        f"Оплата: {pay_form}" if pay_form else "",''')

for p in (E_, A_):
    shutil.copy2(p, p + ".bak_pay1112_" + ST)
io.open(E_ + ".new", "w", encoding="utf-8").write(e)
io.open(A_ + ".new", "w", encoding="utf-8").write(a)
py_compile.compile(E_ + ".new", doraise=True)
py_compile.compile(A_ + ".new", doraise=True)
shutil.move(E_ + ".new", E_)
shutil.move(A_ + ".new", A_)
print("применено, бэкап .bak_pay1112_" + ST)
