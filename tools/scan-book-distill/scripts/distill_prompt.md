# 蒸馏 Prompt 模板（给子 agent 用）

把下面的模板复制给一个 general-purpose 子 agent，**每本书单独一个 agent**（独立上下文，避免长书爆上下文）。
把 `{占位符}` 替换为实际值。

---

你正在把一本理财/投资书蒸馏成一个 Agent Skill（book-to-skill 开放标准）。独立完成，最后用一段话汇报（章节数、文件数、作者判定、质量提示）。

【书】
- 书名：《{TITLE}》(英文原名如有：{EN_TITLE})
- 作者：{AUTHOR}（用「中文名+英文名」标注；若不确定就从 OCR 文本的封面/版权页核实）
- slug：{SLUG}
- 源 OCR 章节文件：{WORKDIR}/skills/{SLUG}/_raw/ch01.md … chNN.md。请全部读完（大文件用 Read 的 offset/limit 分段读）。

【先读示例以对齐格式与语气】
- {WORKDIR}/skills/investing-simplest-thing/SKILL.md
- {WORKDIR}/skills/investing-simplest-thing/chapters/ch01-yi-shi-ye-yan-guang.md （章节模板）
- 同目录下的 glossary.md、patterns.md、cheatsheet.md
（若示例不存在，按下方「产出格式」自行构造，保持 SKILL.md 含 name/description frontmatter 即可）

【产出文件（写到 {WORKDIR}/skills/{SLUG}/）】
1. SKILL.md —— frontmatter：
   name: {SLUG}
   description: "从《{TITLE}》（{AUTHOR}）蒸馏的<一句话领域>知识 skill。当用户想理解<3-5个核心概念>或引用{AUTHOR}观点时使用。"
   license: see-source
   正文含：这本书解决什么 / 章节索引表(文件|核心命题|章节文件) / 主题索引(速查) / 给 AI 陪练的使用说明（作者名用核实出的名字）。
2. chapters/chNN-<拼音或英文slug>.md —— 把 _raw 文件归并为约 10–20 个逻辑章节，每章必含：
   ## 核心命题（用「> 这是{AUTHOR}的观点：…」框起核心论点）
   ## 关键模型或框架
   ## 原书案例或作者原话
   ## 可操作
   ## 常见误区
   ## 测验题示例(Q+A)
3. glossary.md —— 编号列关键概念，每条标注「({AUTHOR}观点)」。
4. patterns.md —— 约 10–15 条可执行原则，每条标注「({AUTHOR}观点)」。
5. cheatsheet.md —— 一页速查卡。

【关键约束】
- 源文是 OCR 文本，保真度约 70–80%，专有名词、数字、引文常有错字。**禁止把 OCR 原文当精确引文照抄**；以提炼概念、框架、决策模型为主；引用作者观点时明确标注「这是{AUTHOR}的观点」并意译。
- 教学导向、实用导向。整本 skill 中文约 9000–16000 字（不是逐字转录）。
- 所有观点必须归属作者，不要当成普世事实陈述。
- 不要编造文中不明确的案例数字；不确定就写框架性描述。
- 写完后自检：SKILL.md frontmatter 合法（name+description 必填）、章节索引表列出的文件均真实存在。

【完成后】跑一次 lint（可选）：
  python3 {SKILL_REPO}/tools/validate_skill.py {WORKDIR}/skills/{SLUG}/SKILL.md
（0 error / 0 warning 即通过）

完成后汇报一句话总结（含你判定的作者）。
