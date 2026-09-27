#!/bin/bash
# Видео: ищем рабочий эндпоинт/режим на ключах irada и jobus.
# Гипотеза: новым моделям (wan2.5/2.6) нужен путь /services/aigc/video-generation/video-synthesis
# или синхронный режим (без заголовка X-DashScope-Async).

K1="sk-ws-H.DHIIIPP.CZHl.MEQCIEaBzGBGC2dlNRVO4UaP7Cmi-5yjMSliby31Iq0zifF3AiBGYAUz8iCyg0oYdBJ8TWrP0T0IU-GBK7yLVZhR1Qpr2g"
H1="ws-hjjvdfh3rd6k4o9g"
B="https://$H1.ap-southeast-1.maas.aliyuncs.com/api/v1"

try () { # $1=описание $2=url $3=async-заголовок $4=body
  local r=$(curl -s -m 60 -X POST "$2" -H "Authorization: Bearer $K1" -H "Content-Type: application/json" $3 -d "$4" 2>&1 | head -c 220)
  echo "── $1"
  echo "   $(echo "$r" | head -c 200)"
}

BODY_T2V='{"model":"MODEL","input":{"prompt":"liquid gold ink flowing in deep darkness, cinematic"},"parameters":{"size":"1280*720","duration":5}}'

for m in wan2.5-t2v-preview wan2.6-t2v wan2.2-t2v-plus wan2.1-t2v-turbo; do
  try "video-generation (async) · $m" "$B/services/aigc/video-generation/video-synthesis" "-H X-DashScope-Async:enable" "$(echo $BODY_T2V | sed s/MODEL/$m/)"
done

for m in wan2.5-t2v-preview wan2.6-t2v; do
  try "video-synthesis (СИНХРОН, без async) · $m" "$B/services/aigc/video-synthesis" "" "$(echo $BODY_T2V | sed s/MODEL/$m/)"
done

echo ""
echo "=== синхронная картинка: qwen-image-edit / qwen-image-max без async ==="
for m in qwen-image-max qwen-image-edit qwen-image-edit-plus z-image-turbo; do
  try "img sync · $m" "$B/services/aigc/text2image/image-synthesis" "" "{\"model\":\"$m\",\"input\":{\"prompt\":\"dark gold abstract\"},\"parameters\":{\"size\":\"1024*1024\"}}"
done
