#!/bin/bash
# Проверка полного цикла генерации изображения (qwen-image) + расширенный поиск моделей
# на двух активных ключах: irada, jobus.

K1="sk-ws-H.DHIIIPP.CZHl.MEQCIEaBzGBGC2dlNRVO4UaP7Cmi-5yjMSliby31Iq0zifF3AiBGYAUz8iCyg0oYdBJ8TWrP0T0IU-GBK7yLVZhR1Qpr2g"
H1="ws-hjjvdfh3rd6k4o9g"
K2="sk-ws-H.DDMPDIH.9dZ1.MEYCIQCuwtVIELZ7JzZn9LAzfLsEpD8hctmRGSYRokmEWxe6NgIhAKg73JNg4J8FadBlvM1ho8OeHJVZpJMSYfXgMYhdRoh3"
H2="ws-mucsfuhay761ev1c"

BASE="https://$H1.ap-southeast-1.maas.aliyuncs.com/api/v1"

echo "=== 1. Запуск генерации qwen-image (irada) ==="
TASK=$(curl -s -m 60 -X POST "$BASE/services/aigc/text2image/image-synthesis" \
  -H "Authorization: Bearer $K1" -H "Content-Type: application/json" -H "X-DashScope-Async: enable" \
  -d '{"model":"qwen-image","input":{"prompt":"Ultra-luxurious dark abstract: liquid gold flowing across deep midnight blue-black, cinematic volumetric light, elegant premium, no text, no people, 16:9"},"parameters":{"size":"1664*928","n":1,"prompt_extend":true}}' \
  | node -e "let s='';process.stdin.on('data',d=>s+=d).on('end',()=>{try{const j=JSON.parse(s);console.log(j.output&&j.output.task_id||'');}catch(e){console.log('');}})")
echo "task_id: $TASK"
if [ -z "$TASK" ]; then echo "не удалось создать задачу"; exit 1; fi

echo "=== 2. Ожидание результата ==="
for i in $(seq 1 30); do
  sleep 5
  R=$(curl -s -m 30 "$BASE/tasks/$TASK" -H "Authorization: Bearer $K1")
  ST=$(echo "$R" | grep -o '"task_status":"[A-Z]*"' | head -1)
  echo "  [$i] $ST"
  case "$ST" in
    *SUCCEEDED*)
      echo "$R" > /tmp/ds-image-task.json
      node -e "
const fs=require('fs');
const j=JSON.parse(fs.readFileSync(process.argv[1],'utf8'));
const res=(j.output&&j.output.results)||[];
console.log('результатов:', res.length);
if(res[0]&&res[0].url){ console.log('URL:', res[0].url.slice(0,120)); fs.writeFileSync('/tmp/ds-url.txt', res[0].url); }
if(res[0]&&res[0].message) console.log('message:', res[0].message);
" "$(cygpath -m /tmp/ds-image-task.json)"
      break ;;
    *FAILED*|*CANCELED*)
      echo "$R" | head -c 400; break ;;
  esac
done

echo ""
echo "=== 3. Расширенный поиск моделей на двух ключах ==="
IMGS="qwen-image qwen-image-plus qwen-image-max qwen-image-edit qwen-image-edit-plus wan2.5-t2i wan2.5-t2i-preview wanx2.5-t2i wanx2.5-t2i-preview z-image-turbo flux-schnell flux-dev stable-diffusion-3.5-large sd3.5-large imagegen-t2i"
VIDS="wan2.5-t2v wan2.5-t2v-preview wan2.5-i2v wan2.5-i2v-preview wan2.6-t2v wan2.6-i2v wan2.2-t2v wan2.2-i2v kling-v1 vidu-q1 video-synthesis wan2.1-t2v wan2.1-i2v"
for pair in "$K1|$H1|irada" "$K2|$H2|jobus"; do
  K="${pair%%|*}"; rest="${pair#*|}"; H="${rest%%|*}"; N="${rest##*|}"
  B="https://$H.ap-southeast-1.maas.aliyuncs.com/api/v1"
  echo "── $N ──"
  for m in $IMGS; do
    r=$(curl -s -m 30 -X POST "$B/services/aigc/text2image/image-synthesis" -H "Authorization: Bearer $K" -H "Content-Type: application/json" -H "X-DashScope-Async: enable" -d "{\"model\":\"$m\",\"input\":{\"prompt\":\"test\"},\"parameters\":{\"size\":\"1024*1024\"}}" 2>&1 | head -c 160)
    case "$r" in *'"task_id"'*) echo "  ✅ IMG $m";; *'Model not exist'*) : ;; *'InvalidParameter'*) : ;; *) echo "  ?  IMG $m → $(echo "$r" | head -c 90)";; esac
  done
  for m in $VIDS; do
    r=$(curl -s -m 30 -X POST "$B/services/aigc/video-synthesis" -H "Authorization: Bearer $K" -H "Content-Type: application/json" -H "X-DashScope-Async: enable" -d "{\"model\":\"$m\",\"input\":{\"prompt\":\"test\"},\"parameters\":{\"size\":\"1280*720\"}}" 2>&1 | head -c 160)
    case "$r" in *'"task_id"'*) echo "  ✅ VID $m";; *'Model not exist'*) : ;; *'InvalidParameter'*) : ;; *) echo "  ?  VID $m → $(echo "$r" | head -c 90)";; esac
  done
done
