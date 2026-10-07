# whiteboard-video：手绘白板讲解视频

> 来源：[trustfuture/simon-skills](https://github.com/trustfuture/simon-skills) 的 `whiteboard-video`，本目录是**竖屏改造版**。

**手绘白板风格的"边画边讲"讲解视频**，以 Agent Skill 的形式开源。给 AI 一句选题，它查资料、写旁白、画场景、配音对字幕、逐笔渲染、混配乐，交回：一条成片、封面、字幕、旁白稿、发布文案。

不露脸，不开剪辑软件，画面上每一笔都是代码画的。

## 本目录相对上游的改造（竖屏版）

- **画布改成竖屏 1080×1920**（上游默认 1920×1080 横屏），适合视频号 / 抖音 / 小红书。
- **结构改成"单场景多 beat"**：整段旁白写在一个 Scene 里用 `|` 切拍，一拍=一句话=一个完整画面，拍与拍之间用换页隐藏，页面间无停顿，语音一口气念完。
- **每拍 3~5 个元素**，语音是主线、画面跟配音走（画面不拖长，不出现"念完了还在干画"）。
- **封面 3:4 竖版**（1080×1440），顶部系列标签 + 中间反差标题 + 底部品牌行。
- **字幕位 / 语速按竖屏实测调过**：`captions.baselineY=1810`、`safeTop=1700`、`tts.speed=1.15`、片尾卡 3.6s。
- **每拍贴纸各不相同**：同一张贴纸一期正片只用 1 次（避免同一形象反复出现看腻）；缺图用母本参考图 image-to-image 生成新贴纸，保持形象统一。
- 配套有 `制作标准.md`（流程与自检清单）、`季度选题批.md`（按类型成批做）等运营文档，可视需要在你的副本里维护。

> 注：上游是"6~8 场景、2~2.5 分钟"的长视频结构；本改造版按竖屏短视频（约 27~32 秒、5 拍）走。两者共用同一套 `lib/`、`bin/wb` 与 `references/`，结构差异体现在每期 `scenes.js` 的写法上。

## 它是怎么做的

```
选题 → 查证（数字进 README）→ 写旁白（按 | 切段）→ 出 Logo 与贴纸 → 画场景（逐段静帧检查）
    → 火山 TTS 配音（逐字时间戳对字幕）→ 浏览器里逐笔渲染 → 混配乐 → 封面 → 发布文案
```

| 环节 | 用什么 |
| --- | --- |
| 手绘线条 | [rough.js](https://roughjs.com/)（Excalidraw 底层同一个库），场景同时导出 Excalidraw 格式，装了 Obsidian Excalidraw 插件能直接打开改 |
| 逐笔动画 | Playwright 在 Chromium 里逐帧截图，4 路并行，2.5 分钟的片子渲染约 35 秒 |
| 人物、道具贴纸 | 本地 [codex](https://github.com/openai/codex) CLI 生图，一次 2×2 四宫格，自动抠白底、去杂点 |
| 公司、产品 Logo | Wikimedia Commons 官方 SVG，出处自动记录 |
| 配音与字幕 | 火山引擎语音合成（官方音色或你自己的声音复刻），原生 1.2 倍语速，返回的逐字时间戳直接对字幕 |
| 合成 | ffmpeg：拼帧、烧字幕、说话时自动压低配乐 |

几条写死在 skill 里的规矩：

- **先写旁白，再决定画什么。** 每一段都得有东西能画，画不出来的句子并进相邻段。
- **字幕区和水印区是禁区。** 底部 y≥960 留给字幕，右上角 320×130 留给水印，元素压进去就报警告。
- **讲公司用官方 Logo，讲人用照片参考的漫画像。** AI 画的拟人机器人和通用小人，观众认不出是谁。
- **数字先查再写。** 出处和口径进期目录 README，旁白、字幕、封面、文案里的数字从同一处取。
- **每期都一样的东西进配置文件。** 语速、配乐音量、字幕字号、品牌名都在 `config.json`，AI 只写每期不一样的部分。

## 仓库内容

| 路径 | 说明 |
| --- | --- |
| `SKILL.md` | 技能入口，AI 读这个 |
| `references/` | 场景 API、版式坐标、贴纸与 Logo、发布文案 |
| `../video-common/` | 合集共用的公共工序：事实核查、合规、成片验收 |
| `bin/wb` | 命令行：`new` `scenes` `stills` `image` `logo` `tts` `render` `mix` `cover` `build` `clean` |
| `lib/scene-dsl.js` | 场景 DSL：一行代码一个元素，导出 Excalidraw 场景图、旁白稿、封面 |
| `lib/render.html` `lib/render.js` | 逐笔渲染器：子路径顺序描边、双描边 A/B 层、按字数排期、铅笔跟随、并行出帧 |
| `lib/tts-volc.mjs` `lib/tts/` | 火山 TTS，带缓存与半段音频自动重试 |
| `lib/captions.cjs` | 逐字时间戳切 6~20 字短句，烧录并导出 SRT |
| `lib/gen-image.mjs` | codex 生图贴纸 + 抠图 |
| `lib/fetch-logo.mjs` | Wikimedia Commons 官方 Logo，`--vs` 拼对比封面图 |
| `lib/mix-bgm.mjs` | 闪避配乐：说话时压低，停顿时抬起，尾部淡出 |
| `templates/` | 每期 `scenes.js` 与 `发布.md` 模板 |
| `examples/` | 一期完整示例：旁白、7 个场景、4 张贴纸、封面函数、资料来源、发布稿 |
| `config.json` | 全部参数：目录、语速、配乐、笔速、字幕、品牌层、封面 |

## 环境

| 依赖 | 说明 |
| --- | --- |
| Node.js 20.12 以上 | 用到了 `process.loadEnvFile` |
| ffmpeg | `brew install ffmpeg` |
| Playwright Chromium | `npm install` 会自动装 |
| codex CLI | 只有出贴纸（`wb image`）用到，登录后走你自己的额度 |
| 火山引擎账号 | 开通语音合成，凭证填 `.env`；想用自己的声音就在控制台做一次声音复刻 |

macOS 上实测。Linux 应该能跑，`wb open` 用的 `open` 命令除外。

## 使用

```bash
git clone https://github.com/trustfuture/simon-skills.git
cd simon-skills/skills/whiteboard-video
npm install
cp .env.example .env          # 填火山凭证和音色

# 先把示例渲染一遍，确认环境没问题
mkdir -p episodes && cp -R examples/* episodes/
bin/wb build 懂很多道理          # 约一分钟，成片在 build/<期>/outputs/final.mp4
```

然后把 `skills/whiteboard-video` 和 `skills/video-common` 一起放进 AI 工具的 skills 目录（Claude Code 是 `~/.claude/skills/`，软链也行，两个要平级，安装命令见[合集 README](../../README.md)），对它说：

> 做一期白板视频：为什么定了计划总是坚持不下去

它会按 `SKILL.md` 建期目录、查资料、写旁白、出贴纸、画场景，逐段出静帧给你看，最后出片、出封面、写发布稿。中途任何一步都可以停下来改。

自己动手也行：

```bash
bin/wb new "为什么定了计划总是坚持不下去"   # 建期目录，编辑里面的 scenes.js
bin/wb stills 计划                        # 每段一张静帧，检查排版
bin/wb build 计划                         # 出片
```

## 换成你的账号

- **品牌**：`config.json` → `brand.name`（水印与片尾的手写名）、`brand.accent`（品牌色）、`brand.slogan`、`brand.endCard.cta`；有透明底 logo 就填 `brand.logo`。
- **声音**：`.env` 的 `VOLC_TTS_VOICE`。官方 2.0 音色配 `VOLC_TTS_RESOURCE_ID=seed-tts-2.0`，声音复刻音色（`S_` 开头）配 `volc.megatts.default`。
- **配乐**：仓库不附带音乐。放一首无版权音乐到 `assets/bgm.mp3`，或改 `config.json` 的 `bgm.file`；没有配乐就出无配乐成片。
- **目录**：`config.json` → `dirs.projects` 可以指到你的 Obsidian 仓库里，每期文件夹就能在 Obsidian 里直接看、直接改场景图。
- **封面标签**：`cover.seriesTag`。
- **发布文案口吻与话题**：`references/publish.md`、`templates/发布.md`。

## 许可

- 代码与文档：MIT，见合集根目录 `LICENSE`。
- `assets/fonts/Xiaolai-Regular.ttf`：[小赖字体](https://github.com/lxgw/kose-font)，SIL Open Font License 1.1，许可证见 `assets/fonts/OFL.txt`。
- `examples/` 里的贴纸由 codex 生成，随示例一起提供，可自由使用。
- 用 `wb logo` 取到的公司 Logo 版权归各自所有者，只适合在评论和报道语境中原样使用。
