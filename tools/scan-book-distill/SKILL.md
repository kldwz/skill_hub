---
name: scan-book-distill
description: "专攻【扫描版 / 图片型 / 无文字层】PDF 的蒸馏流水线：OCR(pdftoppm+tesseract) → 按章节去重切分 → 派 agent 蒸馏成 Agent Skill(SKILL.md+chapters+glossary/patterns/cheatsheet)。当用户手里是扫描件/影印 PDF、pdftotext 抽不出字（<500字）时使用。与 book2skill-distill（文字层 PDF 专用）互补：文字层走 book2skill-distill，扫描层走本 skill。"
---

# scan-book-distill — 扫描书 → Agent Skill

专门处理**没有文字层**的 PDF（扫描件、影印件、扫描导出）。这类 PDF 用 `pdftotext` 抽不出字，必须先 OCR。

> 分工：**文字层 PDF → `book2skill-distill`**；**扫描层 PDF → 本 skill**。不要混用。

**核心原则**：抽取结构而非总结；OCR 保真度仅 70–80%，蒸馏以「框架+概念+测验」为主，勿照搬疑似错字的引文；所有观点标注作者。

## 何时用
- 用户：这本书是扫描版/影印的，帮我做成能问的 skill / 把扫描 PDF 灌进 agent
- `pdftotext 书.pdf - | wc -m` 输出 < 500，确认是扫描件

## 步骤

### 1. 准备：确定 slug 与工作目录
```bash
WORKDIR=/path/to/your/project     # 产物（ocr 文本/_raw/最终 skill）都落这里
SLUG=common-stocks-uncommon-profits   # 短标识，英文小写+连字符
PDF=/abs/path/to/扫描书.pdf
```

### 2. OCR（逐页识别成全文）
```bash
python3 scripts/ocr_book.py "$PDF" "$SLUG" --workdir "$WORKDIR"
# 产物：$WORKDIR/$SLUG_ocr.txt  （中间图在 $WORKDIR/.ocr/$SLUG/，确认无误后手动 rm -rf 释放空间）
```
- 长书（200+ 页）建议后台跑：`run_in_background: true`。
- 断点续跑：中断后再跑同一条命令，已合并页会自动跳过。

### 3. 切分（按章节去重切成 _raw 章节文件）
```bash
python3 scripts/split_ocr.py "$SLUG" --workdir "$WORKDIR"
# 产物：$WORKDIR/skills/$SLUG/_raw/chNN.md
```
- 自动识别「第X章 / Chapter X / 序前言…」，按章节号**去重**（OCR 页脚每页重复标题会识别成 200+ 章，已处理）。
- 去重后章节数不在 [3,30] 区间（标题噪声过多）→ 退化为按字符数等分为 12 段。

### 4. 蒸馏（派子 agent，每本一个，独立上下文）
把 `scripts/distill_prompt.md` 的模板复制给一个 general-purpose 子 agent，替换占位符（{TITLE}/{AUTHOR}/{SLUG}/{WORKDIR}/…）。**每本书单独一个 agent**，避免长书爆上下文。

产物：`$WORKDIR/skills/$SLUG/` 下 SKILL.md + chapters/ + glossary.md + patterns.md + cheatsheet.md

### 5. 校验 + 收编
```bash
python3 <本skill上级或 book2skill-distill 的>tools/validate_skill.py \
  "$WORKDIR/skills/$SLUG/SKILL.md"     # 0 error/0 warning 即通过
# 收编进 skills-manager 中心仓库（单一真源）：
skills-manager skills adopt "$WORKDIR/skills/$SLUG"
skills-manager skills deploy --agent workbuddy --agent hermes \
  --agent claude_code --agent codebuddy "$SLUG"
```

## 产物结构（对齐 book-to-skill 开放标准）
```
$SLUG/
  SKILL.md            # name+description 前置 + 核心框架 + 章节索引 + 主题索引
  chapters/chNN-*.md  # 每章：核心命题(标注作者)/框架/案例/可操作/误区/测验
  glossary.md         # 术语表（每条标注作者观点）
  patterns.md         # 可执行原则（每条标注作者观点）
  cheatsheet.md       # 一页速查卡
```

## 坑（已修复，勿回退）
- **tesseract 的 Leptonica 读不了 /tmp**：中间 PNG 必须落在 `workdir` 子树内（脚本已处理）。
- **沙箱批量删除保护**：脚本【不删除】任何中间文件；清空间手动 `rm -rf $WORKDIR/.ocr/$SLUG/`。
- **pdftoppm 后缀是真实页码**（非 -001.png）：`ocr_book.py` 用 `pg{i:04d}-{i:03d}.png`。
- **OCR 页脚重复标题**：`split_ocr.py` 按章节号去重，噪声过多退化等分。
- **版权**：受版权书不要随产品分发原文/整本摘要；只卖「体系+AI陪练」，让用户自带书。公版书（如《乌合之众》1895、《股票作手回忆录》1923）可内置。
- **OCR 保真度 ~70–80%**：蒸馏时禁止照抄疑似错字引文，观点一律标注「这是 X 的观点」并意译。

## 依赖
- 系统：`poppler`(pdftoppm/pdfinfo)、`tesseract` + `chi_sim`+`eng` 语言包
- Python：仅标准库
