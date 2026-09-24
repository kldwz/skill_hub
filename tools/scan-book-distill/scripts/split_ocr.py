#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 OCR 全文（<workdir>/<slug>_ocr.txt）按章节标题切成章节文件，
落到 <workdir>/skills/<slug>/_raw/chNN.md，供子 agent 逐章蒸馏。

切分策略：
  - 检测「第X章 / Chapter X / 序|前言|导言|引言|绪论|后记|附录|结语|致谢」。
  - 关键：OCR 页脚会在每页重复「第X章」，所以按「章节号」去重，只保留首次
    出现；用首次出现到下一章首次出现之间的文本作为该章内容。
  - 若去重后章节数不在 [3,30] 区间，退化为按字符数等分为 12 段。

用法：
  python3 split_ocr.py <slug> [--workdir DIR]
"""
import argparse, os, re, sys

CN_NUM = {"零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5,
          "六": 6, "七": 7, "八": 8, "九": 9, "十": 10, "百": 100, "千": 1000}


def cn_to_int(s):
    if s.isdigit():
        return int(s)
    total, cur = 0, 0
    for ch in s:
        if ch in CN_NUM:
            v = CN_NUM[ch]
            if v >= 100:
                total += (cur if cur else 1) * v
                cur = 0
            elif v == 10:
                total += (cur if cur else 1) * 10
                cur = 0
            else:
                cur = v
    return total + cur


def normalize(raw):
    raw = raw.strip()
    m = re.match(r'第\s*([一二三四五六七八九十百零0-9]+)\s*章', raw)
    if m:
        return "章:" + str(cn_to_int(m.group(1)))
    m = re.match(r'Chapter\s+(\d+)', raw, re.IGNORECASE)
    if m:
        return "ch:" + m.group(1)
    return "其它:" + raw


PATTERNS = [
    re.compile(r'第\s*[一二三四五六七八九十百零0-9]+\s*章[^\n]*'),
    re.compile(r'Chapter\s+\d+[^\n]*', re.IGNORECASE),
    re.compile(r'(?:序|前言|导言|引言|绪论|引子|后记|附录|结语|致谢)[^\n]*'),
]


def find_headings(text):
    seen = {}
    matches = []
    for pat in PATTERNS:
        for m in pat.finditer(text):
            label = normalize(m.group(0))
            if label in seen:
                continue
            seen[label] = True
            matches.append((m.start(), m.group(0).strip()))
    matches.sort()
    return matches


def write_chunk(rawdir, idx, title, seg):
    fn = os.path.join(rawdir, f"ch{idx:02d}.md")
    with open(fn, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{seg.strip()}\n")


def split_book(slug, workdir):
    txt_path = os.path.join(workdir, f"{slug}_ocr.txt")
    if not os.path.exists(txt_path):
        print(f"[{slug}] 无 OCR 文本 {txt_path}，请先跑 ocr_book.py", file=sys.stderr)
        return 0
    text = open(txt_path, encoding="utf-8", errors="ignore").read()
    text = re.sub(r"\n*===== 第\d+页 =====\n*", "\n", text)
    headings = find_headings(text)
    rawdir = os.path.join(workdir, "skills", slug, "_raw")
    os.makedirs(rawdir, exist_ok=True)
    for f in os.listdir(rawdir):
        try:
            os.remove(os.path.join(rawdir, f))
        except Exception:
            pass

    if not (3 <= len(headings) <= 30):
        mode = "标题数=%d 不在[3,30]" % len(headings) if headings else "无标题"
        print(f"[{slug}] {mode}，改用等分为 12 段")
        n = 12
        step = max(1, len(text) // n)
        for i in range(n):
            s = i * step
            e = (i + 1) * step if i < n - 1 else len(text)
            write_chunk(rawdir, i + 1, f"第{i+1}部分", text[s:e])
        print(f"[{slug}] 写出 {n} 个分段 -> {rawdir}")
        return n

    print(f"[{slug}] 检测到 {len(headings)} 个真实章节")
    for idx, (pos, txt) in enumerate(headings, 1):
        nxt = headings[idx][0] if idx < len(headings) else len(text)
        seg = text[pos:nxt]
        write_chunk(rawdir, idx, txt, seg)
    print(f"[{slug}] 写出 {len(headings)} 个章节 -> {rawdir}")
    return len(headings)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="OCR 文本按章节切分")
    ap.add_argument("slug")
    ap.add_argument("--workdir", default=".", help="工作目录，默认当前目录")
    args = ap.parse_args()
    split_book(args.slug, os.path.abspath(args.workdir))
    print("DONE")
