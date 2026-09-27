#!/bin/bash
# Перебор ключей × моделей × эндпоинтов DashScope: что реально генерирует фото/видео.
# Вывод: компактные статусы (без секретов).

K1="sk-ws-H.DHIIIPP.CZHl.MEQCIEaBzGBGC2dlNRVO4UaP7Cmi-5yjMSliby31Iq0zifF3AiBGYAUz8iCyg0oYdBJ8TWrP0T0IU-GBK7yLVZhR1Qpr2g"
H1="ws-hjjvdfh3rd6k4o9g"
K2="sk-ws-H.DDMPDIH.9dZ1.MEYCIQCuwtVIELZ7JzZn9LAzfLsEpD8hctmRGSYRokmEWxe6NgIhAKg73JNg4J8FadBlvM1ho8OeHJVZpJMSYfXgMYhdRoh3"
H2="ws-mucsfuhay761ev1c"
K3="sk-ws-H.IIMDMD.Z1MB.MEQCIF6Js6WTjVPdVuDd25to3lyLmR79VoZNgK_7Eqs0Dt0RAiBDQaWPFWOA6LXwMTCD0bmk45OoIIpyJ5o6DTfZCx9Q7g"
H3="ws-nwpcf59km4481co4"
K4="sk-ws-H.DDIHRPR.5luJ.MEYCIQDLxADVSD5wHxXgav6gpIzKyl21y074_gBg0tYsq30V_QIhANt6Emo7K7QZXwlWg25CFO31DDqiv8CNeRIFmTbrT9RG"
H4="ws-29108of7qflqu4kt"

probe_img_compat () { # $1=key $2=host $3=model
  local r=$(curl -s -m 45 -X POST "https://$2.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/images/generations" \
    -H "Authorization: Bearer $1" -H "Content-Type: application/json" \
    -d "{\"model\":\"$3\",\"prompt\":\"dark luxurious gold abstract\",\"size\":\"1024x1024\",\"n\":1}" 2>&1 | head -c 200)
  echo "$r" | grep -o '"error"\|"data"\|"url"\|Model not exist\|InvalidParameter\|Unauthorized\|Access denied\|quota' | head -1
}

probe_img_native () { # $1=key $2=host $3=model
  local r=$(curl -s -m 45 -X POST "https://$2.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis" \
    -H "Authorization: Bearer $1" -H "Content-Type: application/json" -H "X-DashScope-Async: enable" \
    -d "{\"model\":\"$3\",\"input\":{\"prompt\":\"dark luxurious gold abstract\"},\"parameters\":{\"size\":\"1024*1024\",\"n\":1}}" 2>&1 | head -c 200)
  echo "$r" | grep -o '"task_id"\|Model not exist\|InvalidParameter\|Unauthorized\|Access denied\|quota' | head -1
}

probe_vid_native () { # $1=key $2=host $3=model
  local r=$(curl -s -m 45 -X POST "https://$2.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/video-synthesis" \
    -H "Authorization: Bearer $1" -H "Content-Type: application/json" -H "X-DashScope-Async: enable" \
    -d "{\"model\":\"$3\",\"input\":{\"prompt\":\"gold ink flowing in darkness\"},\"parameters\":{\"size\":\"1280*720\"}}" 2>&1 | head -c 200)
  echo "$r" | grep -o '"task_id"\|Model not exist\|InvalidParameter\|Unauthorized\|Access denied\|quota' | head -1
}

IMGS="wanx2.1-t2i-turbo wanx2.2-t2i-flash wanx2.5-t2i-preview qwen-image wanx-v1"
VIDS="wan2.2-t2v-plus wan2.1-t2v-turbo wan2.5-t2v-preview wan2.2-i2v-plus"

for pair in "$K1|$H1|irada" "$K2|$H2|jobus" "$K3|$H3|s.ragimoff" "$K4|$H4|orxang"; do
  K="${pair%%|*}"; rest="${pair#*|}"; H="${rest%%|*}"; N="${rest##*|}"
  echo "════════ КЛЮЧ: $N ($H) ════════"
  for m in $IMGS; do
    printf "  img/compat  %-22s %s\n" "$m" "$(probe_img_compat "$K" "$H" "$m")"
  done
  for m in $IMGS; do
    printf "  img/native  %-22s %s\n" "$m" "$(probe_img_native "$K" "$H" "$m")"
  done
  for m in $VIDS; do
    printf "  vid/native  %-22s %s\n" "$m" "$(probe_vid_native "$K" "$H" "$m")"
  done
done
