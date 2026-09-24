# scan-book-distill

专攻【扫描版 / 图片型 / 无文字层】PDF 的蒸馏流水线：OCR(pdftoppm+tesseract) → 按章节去重切分 → 派 agent 蒸馏成 Agent Skill(SKILL.md+chapters+glossary/patterns/cheatsheet)。当用户手里是扫描件/影印 PDF、pdftotext 抽不出字（<500字）时使用。与 book2skill-distill（文字层 PDF 专用）互补：文字层走 book2skill-distill，扫描层走本 skill。

## 用途
把**没有文字层**的扫描版 / 影印版 PDF 蒸馏成 Agent Skill 的流水线工具：OCR（pdftoppm + tesseract）→ 按章节去重切分 → 派 agent 蒸馏。与 `book2skill-distill`（文字层 PDF 专用）互补。

## 来源
本项目「财商启蒙 OS」拆书工具链。

## 用法
详见同目录 `SKILL.md`。核心三步：

```bash
python3 scripts/ocr_book.py <pdf> <slug> --workdir <dir>   # 1. OCR 成全文
python3 scripts/split_ocr.py <slug> --workdir <dir>        # 2. 按章节切分
# 3. 按 scripts/distill_prompt.md 模板派 agent 蒸馏成 Skill
```
