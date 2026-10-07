# video-common：账号无关的视频公共工序

> 来源：[trustfuture/simon-skills](https://github.com/trustfuture/simon-skills) 的 `video-common`。

各视频流水线**共用的五道工序**，不直接触发，由具体账号 skill（如 [`../whiteboard-video`](../whiteboard-video/)）在对应环节引用。只收"换个账号做法也不变"的东西。

## 内容

| 文件 | 说明 |
| --- | --- |
| `SKILL.md` | 技能入口 |
| `references/fact-check.md` | 事实核查、来源台账、估算标注 |
| `references/cover-qa.md` | 封面比例与验收（白板用 Excalidraw 封面，不适用） |
| `references/platform-copy.md` | 多平台发布文案机制 |
| `references/delivery-qa.md` | 成片机器验收、交付边界 |
| `references/compliance.md` | 合规自查 |

## 安装

与 `whiteboard-video`（或其它视频 skill）**平级**放进同一 skills 目录即可，例如：

```
~/.codebuddy/skills/
├── whiteboard-video/
└── video-common/
```

`whiteboard-video` 的 `SKILL.md` 里用 `../video-common/references/...` 引用它，所以两者必须平级。

## 不共用的部分

音色、字幕样式、品牌、时长、口吻、平台集合等**各账号自己的东西不在这里**，留在各自的账号 skill 里。
