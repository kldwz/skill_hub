# skill_hub

个人 / 团队的 Agent Skill 合集。**按领域分类存放**，每个 Skill 放在 `<分类>/<skill名>/` 下，并自带一份 `README.md` 说明用途与用法。

> 设计原则：后续会有大量 Skill 陆续入库，统一用「分类 → Skill」两级目录，避免平铺在根目录造成杂乱。

## 分类索引

| 分类 | 说明 | 已收录 |
|------|------|--------|
| `legal/` | 法律 / 法规类 Skill | [`civil-code-cn`](legal/civil-code-cn/) —— 《民法典》法条检索 |
| `finance/` | 财商 / 投资经典书蒸馏 Skill（15 本） | 富爸爸穷爸爸、小狗钱钱、纳瓦尔宝典、穷查理宝典、乌合之众、股票作手回忆录、证券分析、投资中最简单的事、指数基金投资指南、股市长线法宝、一本书读懂财报、怎样选择成长股、聪明的投资者、投资最重要的事、资产配置的艺术 → [`finance/`](finance/) |
| `tools/` | 拆书 / 蒸馏流水线工具 | [`scan-book-distill`](tools/scan-book-distill/) —— 扫描版 PDF→Skill 的 OCR + 切分 + 蒸馏工具 |

## 目录约定

```
skill_hub/
├── README.md                # 本索引
└── <分类>/                  # 例如 legal/、finance/、health/ …
    └── <skill名>/
        ├── SKILL.md         # Agent 调用说明（必须）
        ├── README.md        # 该 Skill 的用途 / 用法 / 来源（必须）
        └── …                # 其他配套资源（章节文件、脚本等）
```

新增 Skill 时：先判断所属分类（没有就新建一个分类目录），在分类下建 Skill 子目录，放入 `SKILL.md` + `README.md` + 配套资源，再提交。

## 贡献 / 使用

每个子目录都是独立可用的 Agent Skill，可直接复制到 Agent 的 skills 目录（如 `~/.codebuddy/skills/`、`~/.claude/skills/` 等）后调用。
