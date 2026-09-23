# skill_hub

个人 / 团队的 Agent Skill 合集。**按领域分类存放**，每个 Skill 放在 `<分类>/<skill名>/` 下，并自带一份 `README.md` 说明用途与用法。

> 设计原则：后续会有大量 Skill 陆续入库，统一用「分类 → Skill」两级目录，避免平铺在根目录造成杂乱。

## 分类索引

| 分类 | 说明 | 已收录 |
|------|------|--------|
| `legal/` | 法律 / 法规类 Skill | [`civil-code-cn`](legal/civil-code-cn/) —— 《民法典》法条检索 |

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
