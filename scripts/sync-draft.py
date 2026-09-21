#!/usr/bin/env python3
"""index.html から文面原本 lp_draft_202607.md を再生成する。

LP の文言を変えたら必ずこれを実行して原本を本番と一致させる。
末尾の「変更記録」以降は引き継ぐ。
"""
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "index.html")
DST = os.path.join(ROOT, "lp_draft_202607.md")
LOG_MARK = "# 変更記録"


def text(fragment: str) -> str:
    fragment = re.sub(r"<br\s*/?>", "\n", fragment)
    fragment = re.sub(r"<strong>(.*?)</strong>", r"**\1**", fragment, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def main() -> None:
    s = open(SRC, encoding="utf-8").read()

    def one(pattern: str):
        m = re.search(pattern, s, re.S)
        assert m, f"not found: {pattern[:50]}"
        return m

    out = [
        "# CBC LP 文面原本（本番 index.html と同期）\n",
        "> scripts/sync-draft.py が index.html から生成する写し。"
        "文言は index.html を編集し、このスクリプトで再生成する。\n",
        f'**meta description:** {one(chr(60) + "meta name=.description. content=.(.*?).>").group(1)}\n',
        "---\n",
        "## Hero\n",
        text(one(r'<p class="hero-subtitle">(.*?)</p>').group(1)) + "\n",
        f'**{text(one(r"<h1>(.*?)</h1>").group(1)).replace(chr(10), "")}**\n',
        text(one(r'<p class="hero-description">(.*?)</p>').group(1)) + "\n",
        "---\n",
        "## 理念\n",
        text(one(r'<div class="mission-quote fade-in">(.*?)</div>').group(1)) + "\n",
        "---\n",
        "## 取り組み・実績\n",
        text(one(r'<p class="projects-lead[^>]*>(.*?)</p>').group(1)) + "\n",
    ]

    for card in re.findall(r'<div class="project-card fade-in">(.*?)\n            </div>\n', s, re.S):
        loc = text(re.search(r'<div class="location">(.*?)</div>', card, re.S).group(1)).replace("\n", " ")
        out += [
            f"### {loc}\n",
            f'**{text(re.search(r"<h3>(.*?)</h3>", card, re.S).group(1))}**\n',
            text(re.search(r"</h3>\s*<p>(.*?)</p>", card, re.S).group(1)) + "\n",
        ]
        target = re.search(r'<p class="project-target"[^>]*>(.*?)</p>', card, re.S)
        if target:
            out.append(text(target.group(1)) + "\n")
        for url, label in re.findall(r'<a href="([^"]+)"[^>]*class="project-link">(.*?)</a>', card, re.S):
            out.append(f"- {text(label)} {url}")
        out.append("")
        press = re.search(r'<div class="project-press">(.*?)<figure', card, re.S)
        if press:
            out += [
                "**メディア掲載**",
                text(re.search(r'project-press-title">(.*?)</p>', press.group(1), re.S).group(1)),
                text(re.search(r'project-press-comment">(.*?)</p>', press.group(1), re.S).group(1)),
                f'写真キャプション: {text(re.search(r"<figcaption>(.*?)</figcaption>", card, re.S).group(1))}',
                "",
            ]
        out += [text(x) for x in re.findall(r'<span class="project-highlight">(.*?)</span>', card, re.S)]
        out.append("")

    out += ["---\n", "## CBCの強み\n"]
    cards = re.findall(r'<div class="service-card fade-in"[^>]*>(.*?)<div class="service-tags">(.*?)</div>', s, re.S)
    for i, (card, tag_block) in enumerate(cards, 1):
        tags = " / ".join(text(x) for x in re.findall(r'<span class="service-tag">(.*?)</span>', tag_block, re.S))
        out += [
            f'### {i}. {text(re.search(r"<h3>(.*?)</h3>", card, re.S).group(1))}\n',
            text(re.search(r"<p>(.*?)</p>", card, re.S).group(1)) + "\n",
            f"タグ: {tags}\n",
        ]

    ptags = " / ".join(text(x) for x in re.findall(r'<span class="strength-tag">(.*?)</span>', s, re.S))
    out += [
        "---\n",
        "## 会社概要\n",
        "**有限会社CBC**\n",
        text(one(r"<p>(2001年、総合商社.*?)</p>").group(1)) + "\n",
        "**代表取締役 米永 憲司**\n",
        text(one(r"<p>(米国駐在、欧州系.*?)</p>").group(1)) + "\n",
        f"タグ: {ptags}\n",
    ]

    contact = re.search(r'<section class="contact".*?<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>', s, re.S)
    if contact:
        out += ["---\n", "## お問い合わせ\n", f"**{text(contact.group(1))}**\n", text(contact.group(2)) + "\n"]

    out += [
        "---\n",
        "## English Summary\n",
        text(one(r'<div class="footer-english"[^>]*>(.*?)</div>').group(1)) + "\n",
    ]

    logs = ""
    if os.path.exists(DST):
        old = open(DST, encoding="utf-8").read()
        if LOG_MARK in old:
            logs = old[old.find(LOG_MARK):]

    body = "\n".join(out)
    body = re.sub(r"\n[ \t]+(?=\S)", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    open(DST, "w", encoding="utf-8").write(body + "\n---\n\n" + (logs or LOG_MARK + "\n"))
    print(f"synced: {DST}")


if __name__ == "__main__":
    main()
