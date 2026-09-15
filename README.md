# 个人博客（veuxuncafe）

基于 **Jekyll** 的中文个人博客，部署在 GitHub Pages（用户站点）：

**https://veuxuncafe.github.io/**

## 日常操作

发文章、更新研究页、本地预览等所有操作，见 **[WRITING.md](WRITING.md)**（完整操作手册）。

## 目录速览

| 路径 | 作用 |
|---|---|
| `_posts/` | **文章**。Markdown，文件名 `YYYY-MM-DD-短名.md` |
| `_layouts/` | 布局：`default.html`（全站 header/导航/footer）、`post.html`（文章页） |
| `index.html` | 首页（hero + 文章列表 + 引言） |
| `about.html` | 关于页 |
| `styles.css` / `script.js` | 样式、深浅色切换与首页分类筛选 |
| `_config.yml` | 站点配置。**改 `baseurl` 会让全站资源 404，别乱动** |
| `research/` | 研究页：数据 `data/findings.json`、生成器 `generate_progress.py`、产物 `index.html` |
| `.github/workflows/` | 云端每日自动更新工作流 |
| `WRITING.md` | 完整操作手册 |

## 部署

仓库 `veuxuncafe/veuxuncafe.github.io` → Settings → Pages →
Source 选 **Deploy from a branch** → **main** / **(root)**。

推送后 1–2 分钟自动发布。
