#!/bin/bash
# 自动质检：对成片抽「每拍中点帧」+「每拍末尾帧」，供逐张看图判断
# 用法: bash scripts/qa.sh "<期名>"
EP="$1"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/build/$EP/outputs/final.mp4"
[ -f "$OUT" ] || { echo "找不到成片: $OUT"; exit 1; }
QADIR="/tmp/qa/$(echo "$EP" | tr ' /' '__')"; mkdir -p "$QADIR"; rm -f "$QADIR"/*.png
AUDIO="$ROOT/build/$EP/work/audio/01-main.json"
python3 - "$AUDIO" "$OUT" "$QADIR" <<'PY'
import json,sys,subprocess,os
audio,out,qadir=sys.argv[1],sys.argv[2],sys.argv[3]
d=json.load(open(audio,encoding='utf-8'))
st=d['segmentStarts']; dur=d['duration']
n=0
for i,s in enumerate(st):
    en=st[i+1] if i+1<len(st) else dur
    for tag,t in [('mid',(s+en)/2),('end',en-0.05)]:
        subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",f"{t:.2f}","-i",out,
                        "-frames:v","1",f"{qadir}/beat{i+1}-{tag}.png"])
        n+=1
print(f"抽出 {len(st)} 拍 × 2 帧 = {n} 张 -> {qadir}")
PY
echo "==> 逐张读 $QADIR 里的图，检查：① 该拍元素是否画完（不空、不缺字/图）② 画面是否贴合该拍语音"
