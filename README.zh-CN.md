# Research-Demo：从失败的证明到可信的证明

这是一个四集讲解视频系列的源文件包，讲的是 Yuechun Sun 在 LLM 与形式化验证方向的研究。分镜、旁白、Manim 场景代码和来源核对都在这里，视频在你自己的电脑上渲染。

| 集 | 主题 | 时长（旁白） |
|---|---|---|
| 1 ExVerus（ICML 2026） | 用 counterexample 推理修复 Verus 证明；兼作系列开场 | 约 9 分钟 |
| 2 TopoVerus（NeurIPS 2026） | 用 RL 训练模型自己给出 counterexample 和修复；safety gate；拓扑图奖励 | 约 8 分钟 |
| 3 Vero（2026） | AI agent 能否构建经过形式化验证的整个代码仓库？benchmark、checker、spec 审计 | 约 8 分钟 |
| 4 Vekto（进行中） | 用 QCP + Coq 在 C 层证明 SIMD kernel 迁移（NEON/SSE → RVV/HVX）等价 | 约 9 分钟 |

主线有两条：**counterexample 把失败的证明和修复连起来**；**证明的可信程度取决于 spec 和 checker**。详见 `docs/SERIES.md`。

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
- TopoVerus 的 Case B 修复我们没有重跑，旁白写的是 "the paper reports"。`verify/` 里有在本地用 Verus 重新检查这些例子的脚本。
- Vekto 尚未发表，视频里把结论分成 "已确立 / 进行中 / 未开始" 三类标注。
- 终审记录和待作者确认的问题在 `docs/REVIEW.md`。
