#!/bin/bash
export PYTHONIOENCODING=utf-8
S="C:/Users/KENAN/AppData/Local/Temp/claude/3ca209efa740dac0/2cb03bd9-8ce0-43df-ad73-ea49dba638c8/scratchpad/shot.py"
O="D:/Projects/Ragimoff/site/test/11/_agent/shots/critic_pg"
K() { powershell -NoProfile -File "$O/kill.ps1" >/dev/null 2>&1; sleep 1; }
name=$1; url=$2; W=$3; H=$4; lang=${5:-ru}; theme=$6; hh=$7
K
if [ -z "$hh" ]; then
 hh=$(EVAL="document.documentElement.scrollHeight" WAIT=3 python "$S" "$url" $W $H "$O/_tmp" 0 2>&1 | grep EVAL | sed 's/EVAL //; s/"//g')
 K
fi
ys=""; y=0; while [ $y -lt $hh ]; do ys="$ys $y"; y=$((y+H-40)); done
echo "$name H=$hh ys=$ys"
pre="1"
if [ "$lang" != "ru" ]; then pre="localStorage.setItem('r11_lang','$lang');location.reload()"; fi
if [ -n "$theme" ]; then pre="document.documentElement.dataset.theme='$theme'"; fi
EVAL="$pre" python "$S" "$url" $W $H "$O/$name" $ys 2>&1 | grep -v EVAL | tr '\n' ' '
K
echo
