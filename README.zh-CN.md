# Research-Demo：四个研究讲解视频

这是四个独立讲解视频的源文件包，每个视频讲 Yuechun Sun 在 LLM 与形式化验证方向的一项工作。分镜、旁白、Manim 场景代码和来源核对都在这里，视频在你自己的电脑上渲染。

| 集 | 主题 | 时长（旁白） |
|---|---|---|
| 1 ExVerus（ICML 2026） | 用 counterexample 推理修复 Verus 证明 | 约 7 分钟 |
| 2 TopoVerus（NeurIPS 2026） | 用 RL 训练模型自己给出 counterexample 和修复；safety gate；拓扑图奖励 | 约 7 分钟 |
| 3 Vero（NeurIPS 2026） | AI agent 能否构建经过形式化验证的整个代码仓库？benchmark、checker、spec 审计 | 约 7 分钟 |
| 4 Vekto（在做） | 用 QCP + Coq 在 C 层证明 SIMD kernel 迁移（NEON/SSE → RVV/HVX）等价 | 约 7 分钟 |

每个视频以对应论文的 arXiv 版本为准（Vekto 以研究仓库为准），四个视频画面风格统一，内容互不依赖。详见 `docs/SERIES.md`。

## 本地生成

```bash
git clone https://github.com/Etha-Sun/Research-Demo.git && cd Research-Demo
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# macOS: brew install cairo pango ffmpeg pkg-config
```

```bash
./render.sh exverus l none      # 480p 无声快速预览
```

```bash
./render.sh all h kokoro        # 四集全部：1080p60、英文配音、中英字幕
```

参数：
- `./render.sh 集名 画质 配音引擎 语言`
  - 画质：`l` / `m` / `h` / `k`
  - 配音引擎：`kokoro`（本地，无需 API key）/ `say`（macOS 自带）/ `none`
  - 语言：`en` 或 `zh`。选 `zh` 就是中文配音，字幕两种语言都会生成。
- 字体：`export VIDEO_FONT_SANS="PingFang SC" VIDEO_FONT_MONO="Menlo"`
- 输出：`out/<集名>.mp4`，字幕在 `out/<集名>.en.srt` 和 `out/<集名>.zh.srt`。

修改流程：
1. 改 `episodes/<集>/narration.json`；
2. 运行 `python tools/check_episode.py <集>` 检查；
3. 用 `l none` 出预览看一遍；
4. 再出 `h` 正式版。

只有改过的旁白会重新配音，动画时长会自动跟随配音长度。

## 来源与可信度

- 屏幕上的每个数字都标了出处，代码都逐字取自论文或代码仓库。删节写在示例文件头和 `SOURCES.md` 里。
- 论文中前后不一致的数字只用各表格里的原值，见 `docs/SERIES.md`。
- `verify/` 里有在本地用 Verus 重新检查这些例子的脚本。
- 终审记录和待作者确认的问题在 `docs/REVIEW.md`。
