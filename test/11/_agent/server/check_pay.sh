cd /opt/ragimoff-api
venv/bin/python /root/patch_pay_1112.py || exit 1
systemctl restart ragimoff-api; sleep 3; systemctl is-active ragimoff-api
cat > /tmp/chk.py <<'PY'
import sys
sys.path.insert(0, "/opt/ragimoff-api")
import epoint_routes as e
for p in ["consult|kenan|enurez-first", "consult|kenan|enurez-course", "consult|kenan|online", "consult|both|offline", "short-kdt", "Общая психология", "individual|kenan|online|20"]:
    print(p, e.training_prices(p))
PY
venv/bin/python /tmp/chk.py
curl -s -o /dev/null -w "result без подписи: %{http_code}\n" -X POST -d "data=x&signature=y" http://127.0.0.1:9631/api/billing/epoint/result
curl -s -o /dev/null -w "admin: %{http_code}\n" http://127.0.0.1:9631/admin
curl -s -o /dev/null -w "admin/tests: %{http_code}\n" http://127.0.0.1:9631/admin/tests
journalctl -u ragimoff-api -n 5 --no-pager | cut -c1-160
