# 研究进展页：每日自动更新

## 这个改动包含什么

| 文件 | 作用 |
|---|---|
| `research/data/findings.json` | **唯一真值**。所有数字都在这里，改这个文件即可更新页面 |
| `research/generate_progress.py` | 生成器（**零依赖**，仅 Python 标准库；图为手写内联 SVG） |
| `research.html` | 生成产物（Jekyll 页面，`layout: default`）——**由机器人提交，不要手改** |
| `.github/workflows/daily-research-update.yml` | 每天 09:17（北京时间）自动重生成并在有变化时提交 |
| `_layouts/default.html`、`_layouts/post.html` | **修复**：原来放在根目录，Jekyll 解析不到 |
| `_config.yml` | 把生成器与数据目录排除出发布产物 |

## 为什么必须同时修 `_layouts/`

Jekyll 只在 **`_layouts/`** 目录里找布局（`layouts_dir` 默认值）。原来 `default.html` 和 `post.html` 躺在仓库**根目录**，所以：

- `index.html` 的 `layout: default` → 解析失败 → 页面丢掉 header/导航/`styles.css` 的 `<link>`/footer
- 各文章的 `layout: post` → 同样失败
- `index.md` 的 `layout: home` → **该布局根本不存在**

这也是站点看起来"没有样式"的原因。

## 启用步骤

1. **检查 GitHub Pages 是否已启用**
   Settings → Pages → Source 选 **Deploy from a branch**，Branch 选 **main** / **(root)**，Save。
   （仓库已改名为 `veuxuncafe.github.io`，与账号同名，因此是**用户站点**，服务在域名根路径 `https://veuxuncafe.github.io/`，且 `baseurl` 必须为 `""`。）

2. **放开 Actions 写权限**
   Settings → Actions → General → Workflow permissions → **Read and write permissions**。

3. **手动跑一次验证**
   Actions → **Daily research progress update** → **Run workflow**。
   日志应显示 `wrote research.html`，随后 `No change ... (nothing to commit)`。

4. 访问 **`https://veuxuncafe.github.io/research.html`**（主页导航已加"研究"入口）。

## 以后怎么更新数字

只改 `research/data/findings.json`，提交即可。想立刻生效就手动 Run workflow 一次。

本地预览：

```bash
python research/generate_progress.py
python -m http.server 8000    # 然后打开 http://localhost:8000/research.html
```

（注意：直接双击 `research.html` 看不到站点的导航和样式，因为它依赖 Jekyll 渲染布局。）

## 两个已知行为

- **每天都会有一次提交**，因为页面里的"本页刷新"时间戳每天变。这是刻意的。
  不想要的话，删掉 `generate_progress.py` 里 `build()` 中的"本页刷新"一段即可。
- **GitHub 会在仓库 60 天无活动后禁用定时任务**。机器人自身的提交算活动；万一停了，
  用 Actions 页面的 **Run workflow** 按钮唤醒一次。

## 其它发现（未改动，供你判断）

- `index.md` 与 `index.html` **同时存在且都做首页**，且 `index.md` 引用了不存在的 `layout: home`。建议删除 `index.md`。
- 根目录下有 3 个 `2026-08-*.md` 文件，用的是 `layout: post`，但**不在 `_posts/` 里**，
  所以它们不会出现在文章列表中，而是各自作为独立页面发布。若要当作文章，应移到 `_posts/`。
