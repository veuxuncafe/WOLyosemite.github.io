#!/usr/bin/env python3
"""Generate the research progress page for veuxuncafe.

Writes research.html at the repository root as a Jekyll page that reuses the
site's own layout (header, navigation, footer, styles.css, theme toggle), so the
page looks like the rest of the site instead of a standalone document.

Deliberately dependency-free: standard library only, and every figure is
hand-built inline SVG. That keeps the daily GitHub Actions run fast and immune
to plotting-library / font problems.

Usage:  python research/generate_progress.py
Writes: <repo-root>/research/index.html
"""
from __future__ import annotations

import datetime as dt
import html
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
DATA = HERE / "data" / "findings.json"
OUT = REPO_ROOT / "research" / "index.html"

# ------------------------------------------------------------------ palette
BASE_COLOR = "#6b7280"
GOOD_COLOR = "#2563eb"   # the proxy does see this channel
BLIND_COLOR = "#dc2626"  # the proxy is blind to this channel
MUTED_COLOR = "#9ca3af"
GRID_COLOR = "rgba(128,128,128,.35)"
TEXT_COLOR = "currentColor"


def esc(s) -> str:
    return html.escape(str(s), quote=True)


# ------------------------------------------------------------------ svg
def rate_chart(rows, base_rate: float, width=780, height=360, title="") -> str:
    """Horizontal bars with cluster-bootstrap CI whiskers plus a base-rate line."""
    L, R, T, B = 168, 92, 54, 40
    pw, ph = width - L - R, height - T - B
    slot = ph / len(rows)
    bar_h = min(30.0, slot * 0.52)

    def x(v: float) -> float:
        return L + max(0.0, min(100.0, v)) / 100.0 * pw

    p = [f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" '
         f'aria-label="{esc(title)}" xmlns="http://www.w3.org/2000/svg">']
    if title:
        p.append(f'<text x="{L}" y="24" font-size="14" font-weight="600" '
                 f'fill="{TEXT_COLOR}">{esc(title)}</text>')
    for v in range(0, 101, 25):
        gx = x(v)
        p.append(f'<line x1="{gx:.1f}" y1="{T}" x2="{gx:.1f}" y2="{T + ph:.1f}" '
                 f'stroke="{GRID_COLOR}" stroke-width="1"/>')
        p.append(f'<text x="{gx:.1f}" y="{T + ph + 20:.1f}" font-size="11" '
                 f'text-anchor="middle" fill="{TEXT_COLOR}" opacity="0.65">{v}%</text>')
    bx = x(base_rate)
    p.append(f'<line x1="{bx:.1f}" y1="{T - 8}" x2="{bx:.1f}" y2="{T + ph:.1f}" '
             f'stroke="{GOOD_COLOR}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    p.append(f'<text x="{bx + 6:.1f}" y="{T - 12}" font-size="11" font-weight="600" '
             f'fill="{GOOD_COLOR}">基率 {base_rate:.1f}%</text>')
    for i, row in enumerate(rows):
        cy = T + slot * i + slot / 2
        top = cy - bar_h / 2
        color = {"depleted": GOOD_COLOR, "blind": BLIND_COLOR}.get(row.get("kind"), MUTED_COLOR)
        rate, lo, hi = float(row["rate"]), float(row["lo"]), float(row["hi"])
        p.append(f'<text x="{L - 12}" y="{cy + 4:.1f}" font-size="12.5" '
                 f'text-anchor="end" fill="{TEXT_COLOR}">{esc(row["label"])}</text>')
        p.append(f'<rect x="{L}" y="{top:.1f}" width="{max(1.0, x(rate) - L):.1f}" '
                 f'height="{bar_h:.1f}" rx="3" fill="{color}" opacity="0.85"/>')
        p.append(f'<line x1="{x(lo):.1f}" y1="{cy:.1f}" x2="{x(hi):.1f}" y2="{cy:.1f}" '
                 f'stroke="{TEXT_COLOR}" stroke-width="1.4" opacity="0.7"/>')
        for v in (lo, hi):
            p.append(f'<line x1="{x(v):.1f}" y1="{cy - 5:.1f}" x2="{x(v):.1f}" '
                     f'y2="{cy + 5:.1f}" stroke="{TEXT_COLOR}" stroke-width="1.4" opacity="0.7"/>')
        p.append(f'<text x="{L + pw + 10:.1f}" y="{cy - 1:.1f}" font-size="12.5" '
                 f'font-weight="600" fill="{color}">{rate:.1f}%</text>')
        p.append(f'<text x="{L + pw + 10:.1f}" y="{cy + 13:.1f}" font-size="10.5" '
                 f'fill="{TEXT_COLOR}" opacity="0.6">n={row["n"]}, 结构={row["clusters"]}</text>')
    p.append("</svg>")
    return "".join(p)


def count_chart(items, total: int, width=780, height=210, title="") -> str:
    L, R, T, B = 168, 92, 54, 30
    pw, ph = width - L - R, height - T - B
    slot = ph / len(items)
    bar_h = min(28.0, slot * 0.5)
    p = [f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" '
         f'aria-label="{esc(title)}" xmlns="http://www.w3.org/2000/svg">']
    if title:
        p.append(f'<text x="{L}" y="24" font-size="14" font-weight="600" '
                 f'fill="{TEXT_COLOR}">{esc(title)}</text>')
    for v in range(0, total + 1, max(1, total // 4)):
        gx = L + v / total * pw
        p.append(f'<line x1="{gx:.1f}" y1="{T}" x2="{gx:.1f}" y2="{T + ph:.1f}" '
                 f'stroke="{GRID_COLOR}" stroke-width="1"/>')
        p.append(f'<text x="{gx:.1f}" y="{T + ph + 18:.1f}" font-size="11" '
                 f'text-anchor="middle" fill="{TEXT_COLOR}" opacity="0.65">{v}</text>')
    for i, it in enumerate(items):
        cy = T + slot * i + slot / 2
        w = max(1.0, it["value"] / total * pw)
        color = it.get("color", MUTED_COLOR)
        p.append(f'<text x="{L - 12}" y="{cy + 4:.1f}" font-size="12.5" '
                 f'text-anchor="end" fill="{TEXT_COLOR}">{esc(it["label"])}</text>')
        p.append(f'<rect x="{L}" y="{cy - bar_h / 2:.1f}" width="{w:.1f}" '
                 f'height="{bar_h:.1f}" rx="3" fill="{color}" opacity="0.85"/>')
        p.append(f'<text x="{L + w + 10:.1f}" y="{cy + 4:.1f}" font-size="12.5" '
                 f'font-weight="600" fill="{color}">{it["value"]}</text>')
    p.append("</svg>")
    return "".join(p)


def contingency_table(spec) -> str:
    head = "".join(f"<th>{esc(c)}</th>" for c in spec["cols"])
    body = []
    for row in spec["rows"]:
        cells = []
        for j, v in enumerate(row["values"]):
            bad = (j == 1 and row["label"] in ("新增失败", "代理反向"))
            cells.append(f'<td class="{"warn" if bad and v else ""}">{v}</td>')
        body.append(f'<tr><th scope="row">{esc(row["label"])}</th>{"".join(cells)}</tr>')
    return (f'<table class="r-ct"><thead><tr><th></th>{head}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table>')


# ------------------------------------------------------------------ page
SCOPED_CSS = """
<style>
.research table{border-collapse:collapse;width:100%;margin:1.1em 0;font-size:.9rem}
.research th,.research td{border:1px solid rgba(128,128,128,.35);padding:7px 10px;
  text-align:left;vertical-align:top}
.research thead th{background:rgba(128,128,128,.08);font-weight:600}
.research td.num,.research th.num{text-align:right;font-variant-numeric:tabular-nums}
.research td.hl{color:#2563eb}
body.dark .research td.hl{color:#93c5fd}
.research .r-ct td{text-align:center;font-weight:600;font-variant-numeric:tabular-nums}
.research .r-ct td.warn{background:rgba(220,38,38,.12);color:#dc2626}
body.dark .research .r-ct td.warn{color:#f87171}
.research figure{margin:1.6em 0;padding:14px 12px 8px;border:1px solid rgba(128,128,128,.35);
  border-radius:10px;overflow-x:auto;background:rgba(128,128,128,.05)}
.research figcaption{font-size:.84rem;opacity:.7;margin-top:6px}
.research .thesis{border-left:3px solid #2563eb;padding:.2em 0 .2em 1em;margin:1.2em 0}
.research .q{font-weight:600;border-left:3px solid #2563eb;padding:.1em 0 .1em .9em;margin:1.2em 0}
.research code{background:rgba(128,128,128,.12);border-radius:5px;padding:1px 5px;
  font-size:.86em;word-break:break-all}
.research .r-meta{font-size:.85rem;opacity:.72}
.research ul{padding-left:1.2em}
</style>
"""


def build(data: dict) -> str:
    meta = data["meta"]
    today = dt.date.today()
    try:
        frozen = dt.date.fromisoformat(meta["data_freeze"])
        frozen_txt = f"{frozen.isoformat()}（数据冻结，已 {days_str(frozen, today)} 天）"
    except ValueError:
        frozen_txt = meta["data_freeze"]
    bj = dt.datetime.now(dt.timezone.utc).astimezone(dt.timezone(dt.timedelta(hours=8)))

    p01, p02 = data["p01"], data["p02"]
    base = next(r for r in p01["rates"] if r["kind"] == "base" and "基率" in r["label"])

    fig1 = rate_chart(p01["rates"], base["rate"],
                      title="图 1｜代理改善率与 95% 聚类区间（独立单位 = 结构）")
    fig3 = count_chart([{"label": "代理反向", "value": 17, "color": GOOD_COLOR},
                        {"label": "行为反向", "value": 1, "color": BLIND_COLOR},
                        {"label": "两者同时发生", "value": 0, "color": BLIND_COLOR}],
                       132, title="图 3｜实例层：代理反向是否预测行为反向（α = 0.25）")

    layers = "".join(
        f'<tr><td><b>{esc(l["name"])}</b> <span class="r-meta">{esc(l["channel"])}</span></td>'
        f'<td>{esc(l["projects_onto"])}</td><td class="hl">{esc(l["complement"])}</td></tr>'
        for l in data["layers"])
    cond = "".join(f'<tr><td>{esc(c["label"])}</td><td class="num">{c["k"]}/{c["n"]}</td>'
                   f'<td>{esc(c["verdict"])}</td></tr>'
                   for c in p01["tautology"]["conditions"])
    q1cols = "".join(f"<th class=\"num\">{esc(c)}</th>" for c in p02["q1"]["cols"])
    q1rows = "".join(f'<tr><th scope="row">{esc(r["state"])}</th>'
                     + "".join(f'<td class="num">{v}</td>' for v in r["values"]) + "</tr>"
                     for r in p02["q1"]["rows"])
    rw = "".join(f'<tr><td><b>{esc(w["work"])}</b><br><span class="r-meta">{esc(w["title"])}</span></td>'
                 f'<td>{esc(w["point"])}</td><td class="hl">{esc(w["impact"])}</td></tr>'
                 for w in data["related_work"])
    lims = "".join(f"<li>{esc(x)}</li>" for x in data["limitations"])
    ces = "".join(f"<li>{esc(x)}</li>" for x in p01["counterexamples"])
    integ = "".join(f'<tr><td>{esc(k)}</td><td class="num">{esc(v)}</td></tr>'
                    for k, v in meta["integrity"].items())
    beh = "".join(f'<tr><th scope="row">{esc(b["state"])}</th>'
                  f'<td class="num">{b["correct"]}/{b["n"]}</td></tr>'
                  for b in p02["behaviour_correct"])

    body = f"""{SCOPED_CSS}
<main class="page container research">
  <p class="eyebrow">RESEARCH / PROXY PROTECTION</p>
  <h1>{esc(meta['project'])}</h1>
  <p class="r-meta">{esc(meta['english'])}<br>
  本页刷新：{bj.strftime('%Y-%m-%d')} (UTC+8)　·　{frozen_txt}　·　状态：{esc(meta['status'])}</p>

  <p class="q">{esc(data['question'])}</p>
  <div class="thesis"><p style="margin:0">{esc(data['thesis'])}</p></div>

  <table>
    <thead><tr><th>层</th><th>投影到</th><th>被丢掉的正交补（失败发生处）</th></tr></thead>
    <tbody>{layers}</tbody>
  </table>

  <h2>P0-1　通道特异性失明</h2>
  <p class="r-meta">{esc(p01['population'])}　·　eligible {p01['eligible_rows']} 行　·　新增失败 {p01['new_failures']}（排序 {p01['new_failures_ranking']} + 遗漏 {p01['new_failures_omission']}）</p>
  <figure>{fig1}<figcaption>代理改善率按失败通道分解。蓝色虚线为基率；排序类整体位于基率之下，遗漏类整体与基率重合。</figcaption></figure>
  <p>{esc(p01['finding'])}</p>
  <p>{esc(p01['mechanism'])}</p>

  <h3>代理方向 × 行为结果</h3>
  {contingency_table(p01['contingency'])}

  <h3>{esc(p01['tautology']['title'])}</h3>
  <p>{esc(p01['tautology']['note'])}</p>
  <table><thead><tr><th>条件</th><th class="num">成立</th><th>性质</th></tr></thead>
  <tbody>{cond}</tbody></table>

  <h3>必须同时报告的反例</h3>
  <ul>{ces}</ul>

  <h2>P0-2　实例层：代理信号不是行为信号</h2>
  <p class="r-meta">{esc(p02['population'])}</p>
  <table><thead><tr><th>状态</th><th class="num">完全正确</th></tr></thead>
  <tbody>{beh}</tbody></table>

  <h3>{esc(p02['q1']['title'])}</h3>
  <table><thead><tr><th>状态</th>{q1cols}</tr></thead><tbody>{q1rows}</tbody></table>
  <p>{esc(p02['q1']['finding'])}</p>

  <figure>{fig3}<figcaption>在全部 132 条输入中，代理反向 17 个、行为反向 1 个，而两者同时发生为 0。</figcaption></figure>
  <p>{esc(p02['finding'])}</p>

  <h3>代理反向 × 行为反向</h3>
  {contingency_table(p02['contingency'])}
  <p class="r-meta">{esc(p02['contingency']['note'])}</p>

  <h2>与最接近的既有工作的关系</h2>
  <table><thead><tr><th>工作</th><th>要点</th><th>对本文的影响</th></tr></thead>
  <tbody>{rw}</tbody></table>

  <h2>验证门（每个数字都逐位通过）</h2>
  <table><tbody>{integ}</tbody></table>

  <h2>限制与披露</h2>
  <ul>{lims}</ul>

  <p class="r-meta">本页由 <code>research/generate_progress.py</code> 每日自动生成；
  数值源为 <code>research/data/findings.json</code>，研究数据本身不随每日刷新变化。</p>
</main>
"""

    front = ("---\n"
             "layout: default\n"
             f"title: {meta['project']} | veuxuncafe\n"
             f"description: {data['question']}\n"
             "---\n")
    return front + body


def days_str(frozen: dt.date, today: dt.date) -> int:
    return (today - frozen).days


def main() -> int:
    if not DATA.exists():
        print(f"missing data file: {DATA}", file=sys.stderr)
        return 1
    data = json.loads(DATA.read_text(encoding="utf-8"))
    page = build(data)
    # Liquid would choke on stray template braces; fail loudly instead of shipping a broken page.
    if "{{" in page or "{%" in page:
        print("refusing to write: output contains Liquid delimiters", file=sys.stderr)
        return 2
    OUT.write_text(page, encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(REPO_ROOT)} ({len(page)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
