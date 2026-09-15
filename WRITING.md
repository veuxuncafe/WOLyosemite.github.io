# 日常操作手册

本站是 Jekyll + GitHub Pages（用户站点），地址 `https://veuxuncafe.github.io/`。

---

## 一、发一篇文章

### 1. 新建文件

放到 **`_posts/`** 目录下，文件名必须是 **`YYYY-MM-DD-英文短名.md`**：

```
_posts/2026-09-20-my-new-post.md
```

- 文件名里的日期就是这个文章的发布日期
- 短名会成为网址：上面的文件对应 `https://veuxuncafe.github.io/posts/my-new-post/`
- 网址格式由 `_config.yml` 的 `permalink: /posts/:title/` 决定

### 2. 内容格式

```markdown
---
layout: post
title: 文章标题
date: 2026-09-20
categories: 技术
description: 一句话摘要，会显示在首页文章列表里。
---

正文用 Markdown 写，随便写。

## 二级标题

- 列表
- 都可以
```

**两个字段要注意：**

| 字段 | 说明 |
|---|---|
| `categories` | **只能是 `技术` 或 `随笔`**。首页的筛选按钮就是「全部 / 技术 / 随笔」，列表按第一个分类归组；不写默认归为「随笔」 |
| `description` | 显示在首页列表的摘要。不写就自动截取正文前 90 字 |

### 3. 发布

```bash
cd "E:\pilot projects\WOLyosemite.github.io"
git add .
git commit -m "post: 文章标题"
git push
```

推上去后 **1–2 分钟**自动出现在首页文章列表里——**不需要手动在首页加链接**（首页用 `{% for post in site.posts %}` 自动列出）。

也可以在 GitHub 网页上直接 New file 创建，效果一样。

> **本机 push 说明**：仓库已配置 SSH remote + 部署密钥（`core.sshCommand` 指向 `E:\pilot projects\.keys\woly_deploy`），所以在上面这个目录里 `git push` **不需要输密码**。
> 但如果你要在**别的仓库**用 HTTPS 推，需要先跑一次：`git config --global http.sslBackend openssl`（本机 SChannel 后端有问题）。

---

## 二、更新研究页

研究页在 `https://veuxuncafe.github.io/research/`，**只需要改一个文件**：

```
research/data/findings.json      ← 唯一真值
```

里面每个字段的含义：

| 字段 | 内容 |
|---|---|
| `meta.project` / `english` | 标题与英文副题 |
| `meta.data_freeze` | 数据冻结日（页面会显示"已 N 天"） |
| `meta.status` | 研究状态一句话 |
| `meta.integrity` | 「验证门」表格，键值对 |
| `question` | 研究问题 |
| `thesis` | 核心论点 |
| `layers` | 三层分解表（通道 / 实例 / 竞争） |
| `p01` / `p02` | 两部分结果：rates、contingency、tautology、q1、q2 等 |
| `related_work` | 与最接近工作的划界表 |
| `limitations` | 限制与披露列表 |

**改完后有两种生效方式：**

- **等自动**：云端 GitHub Actions 每天 09:17、本地计划任务每天 09:40（时间戳是日期粒度，谁先跑谁提交，一天最多一次提交）
- **立刻生效**：
  ```bash
  cd "E:\pilot projects\WOLyosemite.github.io"
  python research/generate_progress.py     # 重新生成 research/index.html
  git add . && git commit -m "research: 更新数据" && git push
  ```

> ⚠️ **绝对不要手改 `research/index.html`** —— 它是生成产物，下次生成会被覆盖。要改内容只改 `findings.json`。

> 想加一整个新章节（比如第三部分结果），那要改生成器 `research/generate_progress.py` 里 `build()` 的模板，我可以代劳。

---

## 三、本地预览

```bash
cd "E:\pilot projects\WOLyosemite.github.io"
python -m http.server 8000
```

然后打开 `http://localhost:8000/`。

> 直接双击 `research/index.html` **看不到网站的导航和样式**——因为它是 Jekyll 内容页，布局由 `_layouts/default.html` 渲染，必须先经 Jekyll 构建。所以要用上面的起服务方式。

---

## 四、目录结构速查

| 路径 | 作用 | 要手动改吗 |
|---|---|---|
| `_posts/*.md` | **文章** | ✅ 新增文章 |
| `_layouts/default.html` | 全站布局（header / 导航 / footer） | 改导航时 |
| `_layouts/post.html` | 文章页布局 | 很少 |
| `index.html` | 首页（hero + 文章列表 + 引言） | 改首页文案时 |
| `about.html` | 关于页 | 改自我介绍时 |
| `styles.css` | 全部样式 | 调外观时 |
| `script.js` | 深浅色切换 + 首页分类筛选 | 很少 |
| `_config.yml` | 站点配置（标题、作者、网址、baseurl） | 很少，**改 `baseurl` 会让全站资源 404，别乱动** |
| `research/data/findings.json` | **研究数据** | ✅ 更新研究 |
| `research/generate_progress.py` | 研究页生成器（零依赖） | 加新章节时 |
| `research/index.html` | 研究页产物 | ❌ **不要手改** |
| `.github/workflows/daily-research-update.yml` | 云端每日自动更新 | 一般不动 |

---

## 五、已知遗留问题（建议有空清理）

1. **根目录有 3 个 `2026-08-*.md` 文件不是文章**
   `2026-08-12-slowly.md`、`2026-08-18-github-pages.md`、`2026-08-21-hello-world.md`
   它们写着 `layout: post`，但**不在 `_posts/` 里**，所以不会被首页列出，而是各自发布成 `/2026-08-12-slowly.html` 这样的独立页面。
   → 想当文章看，就把它们 `git mv` 进 `_posts/`。

2. **`github-pages.html` 是独立 HTML 文档**
   自己写了 `<head>` 并引用 `../styles.css`，不走 Jekyll 布局，外观和站内其它页不一致。内容与 `2026-08-18-github-pages.md` 重复（都在讲 GitHub Pages 搭建）。
   → 建议二选一删掉。

3. **`README.md` 的写文章说明已过时**
   它说"复制 `posts/hello-world.html`，再在 `index.html` 的文章列表里加一条链接"——但 `posts/` 目录不存在，而且现在文章由 Jekyll 自动列出，不需要手动加链接。

---

## 六、两条自动更新通道

| 通道 | 时间 | 依赖 | 备注 |
|---|---|---|---|
| GitHub Actions | 每天 09:17（北京时间） | 不需要你的电脑 | 需要仓库 Settings → Actions → General → Workflow permissions 设为 **Read and write** |
| Windows 计划任务 | 每天 09:40，错过会补跑 | 电脑开机且已登录 | 任务名 `WOLyosemite Research Daily Update`；日志在 `E:\pilot projects\logs\daily-research-update.log` |

两者不会冲突：页面时间戳精确到**日期**，谁先跑谁提交，另一个发现无变化就不提交。

GitHub 会在仓库 60 天无活动后禁用定时工作流；机器人的提交本身算活动，万一停摆，去 Actions 页面点一次 **Run workflow** 即可唤醒。
