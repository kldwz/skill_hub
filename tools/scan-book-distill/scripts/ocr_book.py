#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描版 PDF -> OCR 文本。专供「图片型 / 无文字层」PDF 使用。
文字层 PDF（pdftotext 能抽字）请用 book2skill-distill，不要走这条。

用法：
  python3 ocr_book.py <pdf_path> <slug> [--workdir DIR]

参数：
  pdf_path   源 PDF（绝对或相对路径均可）
  slug       输出与后续切分用的短标识，如 common-stocks-uncommon-profits
  --workdir  工作目录，默认当前目录。产物落点：
               <workdir>/<slug>_ocr.txt        合并后的 OCR 全文
               <workdir>/.ocr/<slug>/          逐页 PNG + 单页 txt（不自动删）
               <workdir>/skills/<slug>/_raw/   切分后章节（由 split_ocr.py 生成）

已踩过的坑（已修复，勿回退）：
  - tesseract 的 Leptonica 读不了 /tmp，中间图必须落在 workdir 子树内（非 /tmp）。
  - 沙箱对「批量删除」有保护，本脚本【不删除】任何中间文件；清空间请手动
    rm -rf <workdir>/.ocr/<slug>/。
  - pdftoppm 输出后缀是「真实页码」（-001.png 这种是错的），本脚本用 pg{i:04d}-{i:03d}.png。
  - 盗版扫描件每页重复的页眉/页脚水印行（如「第一财富网」「请勿用于商业用途」）
    会被正则过滤掉，避免污染正文。
  - 断点续跑：已合并的页跳过；已存在的单页 txt 直接读取合并，不必重识别。
"""
import argparse, subprocess, os, re, sys, time

WM = re.compile(
    r"第一财富网|财高网|d1money|该文档源自网络|请勿用于商业用途|让理财更轻松|"
    r"学理财就上|book\d*|内部交流|www\.|微信号|公众号|淘宝|闲鱼|代找"
)


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def page_count(pdf):
    try:
        out = run(["pdfinfo", pdf]).stdout
        for line in out.splitlines():
            if line.lower().startswith("pages:"):
                return int(line.split(":", 1)[1].strip())
    except Exception:
        pass
    return 0


def ocr_book(pdf, slug, workdir):
    pdf = os.path.abspath(pdf)
    if not os.path.exists(pdf):
        print(f"[{slug}] PDF 不存在：{pdf}", file=sys.stderr)
        return 1
    ocr_dir = os.path.join(workdir, ".ocr", slug)
    os.makedirs(ocr_dir, exist_ok=True)
    out_txt = os.path.join(workdir, f"{slug}_ocr.txt")
    n = page_count(pdf)
    if n == 0:
        print(f"[{slug}] 无法获取页数（pdfinfo 失败或 PDF 损坏）", file=sys.stderr)
        return 1
    print(f"[{slug}] 共 {n} 页，开始 OCR …", flush=True)
    t0 = time.time()
    done = 0
    existing_pages = set()
    if os.path.exists(out_txt):
        with open(out_txt, encoding="utf-8", errors="ignore") as fh:
            for m in re.finditer(r"===== 第(\d+)页 =====", fh.read()):
                existing_pages.add(int(m.group(1)))
    with open(out_txt, "a", encoding="utf-8") as fout:
        for i in range(1, n + 1):
            prefix = os.path.join(ocr_dir, f"pg{i:04d}")
            png = prefix + f"-{i:03d}.png"
            tocr = prefix + ".txt"
            if i in existing_pages:
                done += 1
                continue
            if not os.path.exists(tocr):
                if not os.path.exists(png):
                    run(["pdftoppm", "-png", "-f", str(i), "-l", str(i),
                         "-r", "300", pdf, prefix])
                if not os.path.exists(png):
                    print(f"  ! 第{i}页转图失败，跳过", flush=True)
                    continue
                r = run(["tesseract", png, prefix, "-l", "chi_sim+eng", "--psm", "6"])
                if r.returncode != 0:
                    print(f"  ! 第{i}页OCR失败: {r.stderr[:80]}", flush=True)
                    continue
            try:
                lines = open(tocr, encoding="utf-8", errors="ignore").read().splitlines()
            except Exception:
                lines = []
            clean = [ln for ln in lines if not WM.search(ln)]
            if clean:
                fout.write(f"\n\n===== 第{i}页 =====\n")
                fout.write("\n".join(clean) + "\n")
            done += 1
            if i % 20 == 0:
                print(f"  …{slug} 已完成 {i}/{n} 页 ({time.time()-t0:.0f}s)", flush=True)
    sz = os.path.getsize(out_txt)
    print(f"[{slug}] 完成：{done}/{n} 页，输出 {sz/1024/1024:.1f} MB -> {out_txt}", flush=True)
    print("提示：中间图在 .ocr/%s/ ，确认无误后可手动 rm -rf 释放空间" % slug, flush=True)
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="扫描版 PDF -> OCR 文本")
    ap.add_argument("pdf", help="源 PDF 路径")
    ap.add_argument("slug", help="输出短标识")
    ap.add_argument("--workdir", default=".", help="工作目录，默认当前目录")
    args = ap.parse_args()
    sys.exit(ocr_book(args.pdf, args.slug, os.path.abspath(args.workdir)))
