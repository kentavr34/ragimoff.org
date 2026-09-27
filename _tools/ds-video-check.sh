#!/bin/bash
# 1) Поллинг t2v-задачи (wan2.6) — до результата.
# 2) Проба image-to-video моделей с публичным фото владельца.

K1="sk-ws-H.DHIIIPP.CZHl.MEQCIEaBzGBGC2dlNRVO4UaP7Cmi-5yjMSliby31Iq0zifF3AiBGYAUz8iCyg0oYdBJ8TWrP0T0IU-GBK7yLVZhR1Qpr2g"
H1="ws-hjjvdfh3rd6k4o9g"
B="https://$H1.ap-southeast-1.maas.aliyuncs.com/api/v1"

echo "=== 1. Поллинг t2v wan2.6 (task e9882a05) ==="
for i in $(seq 1 24); do
  sleep 5
  R=$(curl -s -m 30 "$B/tasks/e9882a05-e1d4-44da-b513-01fd66108a53" -H "Authorization: Bearer $K1")
  ST=$(echo "$R" | grep -o '"task_status":"[A-Z]*"' | head -1 | sed 's/.*:"//;s/"//')
  echo "  [$i] $ST"
  if [ "$ST" = "SUCCEEDED" ] || [ "$ST" = "FAILED" ]; then
    echo "$R" > /tmp/ds-vid-task.json
    node -e "
const fs=require('fs');
const j=JSON.parse(fs.readFileSync(process.argv[1],'utf8'));
const o=j.output||{};
console.log('status:', o.task_status);
const v=o.video_url||(o.results&&o.results[0]&&(o.results[0].video_url||o.results[0].url));
if(v){ console.log('video_url:', v.slice(0,140)); fs.writeFileSync('/tmp/ds-video-url.txt', v); }
if(o.message) console.log('message:', o.message.slice(0,200));
if(o.code) console.log('code:', o.code, o.message?o.message.slice(0,150):'');
" "$(cygpath -m /tmp/ds-vid-task.json)"
    break
  fi
done

echo ""
echo "=== 2. image-to-video: какие модели принимают задачу ==="
PHOTO="https://ragimoff.org/images/kenan/photo-portal-crop.jpg"
for m in wan2.5-i2v-preview wan2.6-i2v wan2.2-i2v-plus wan2.1-i2v-turbo; do
  r=$(curl -s -m 60 -X POST "$B/services/aigc/video-generation/video-synthesis" \
    -H "Authorization: Bearer $K1" -H "Content-Type: application/json" -H "X-DashScope-Async: enable" \
    -d "{\"model\":\"$m\",\"input\":{\"prompt\":\"the man slowly walks forward, cinematic\",\"img_url\":\"$PHOTO\"},\"parameters\":{\"resolution\":\"720P\",\"duration\":5}}" 2>&1 | head -c 200)
  case "$r" in *'"task_id"'*) echo "  ✅ I2V $m → $(echo "$r" | grep -o '"task_id":"[^"]*"')";; *) echo "  ?  I2V $m → $(echo "$r" | head -c 130)";; esac
done
