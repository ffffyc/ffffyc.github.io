"""把 tools/data 里的洛谷文章转换成站点内容（content/past/）。

统一归类规则：
  旧标签「题解」        -> 题解
  旧标签「学习笔记」    -> 算法·理论
  旧标签「日报」        -> 算法·理论
  旧标签「杂项」        -> 生活·游记
  无旧标签              -> 沿用新专栏分类

隐藏与否取自后台清单的 status 字段：2 为已公开，其余（草稿、审核中、未通过）算隐藏。
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "past"
TZ = timezone(timedelta(hours=8))

from classify import classify, contest_tags  # noqa: E402

IMG = re.compile(r"!\[([^\]]*)\]\((https?://[^)]+)\)")
# 洛谷原文里有一部分命令写成双反斜杠（\\bmod、\\to），TeX 会把它当成换行，需要还原成单反斜杠
BS_PAIR = re.compile(r"\\\\(?=[A-Za-z])")


SYMBOL = {
    "det": "det", "gcd": "gcd", "min": "min", "max": "max", "log": "log",
    "sum": "Σ", "prod": "∏", "times": "×", "leq": "≤", "le": "≤", "ge": "≥",
    "neq": "≠", "in": "∈", "to": "→", "infty": "∞",
}


def math_to_text(m: re.Match) -> str:
    """把公式压成可读的纯文本，供列表页摘要使用。"""
    s = m.group(0).strip("$")
    s = re.sub(r"\\text\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\operatorname\{([^{}]*)\}", r"\1", s)

    def cmd(mm: re.Match) -> str:
        return SYMBOL.get(mm.group(1), "")

    s = re.sub(r"\\([a-zA-Z]+)", cmd, s)
    s = s.replace("{", "").replace("}", "").replace("^", "").replace("_", "")
    return s


def clean_summary(text: str, limit: int = 88) -> str:
    s = re.sub(r"<[^>]+>", "", text)
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\$\$?.+?\$\$?", math_to_text, s, flags=re.S)
    s = re.sub(r"[*_`>#]", "", s)
    s = re.sub(r"(^|\s)-\s", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip(" -|")
    return s[:limit]


def escape_yaml(value: str) -> str:
    """一律用 JSON 字符串，避免摘要以 - 或 : 开头时被 YAML 误读。"""
    return json.dumps(value, ensure_ascii=False)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    items = json.loads((DATA / "list.json").read_text(encoding="utf-8"))
    mine_path = DATA / "mine.json"
    status = {}
    tops = {}
    if mine_path.exists():
        for entry in json.loads(mine_path.read_text(encoding="utf-8")):
            status[entry["lid"]] = str(entry.get("status"))
            tops[entry["lid"]] = int(entry.get("top") or 0)
    made = 0
    for entry in items:
        lid = entry["lid"]
        path = DATA / "articles" / f"{lid}.json"
        art = json.loads(path.read_text(encoding="utf-8"))

        old_tag = art.get("categoryOld") or ""
        category = classify(art["title"], old_tag, art.get("category", ""))
        tags = []
        coll = art.get("collection")
        coll_name = coll.get("name") if isinstance(coll, dict) else ""
        if category == "游记":
            found = contest_tags(art["title"])
            if found:
                tags.extend(found)
            elif coll_name:
                tags.append(coll_name)
        else:
            if coll_name:
                tags.append(coll_name)
            if old_tag and old_tag != category:
                tags.append(old_tag)

        body = art.get("content", "").replace("\r\n", "\n").strip()
        body = BS_PAIR.sub(r"\\", body)
        when = datetime.fromtimestamp(int(art["time"]), TZ)
        state = status.get(lid, "2")
        hidden = state != "2"

        lines = [
            "---",
            f"title: {escape_yaml(art['title'])}",
            f"date: {when.strftime('%Y-%m-%d')}",
            f"category: {escape_yaml(category)}",
        ]
        if tags:
            lines.append("tags: [" + ", ".join(escape_yaml(t) for t in tags) + "]")
        summary = clean_summary(body)
        if summary:
            lines.append(f"summary: {escape_yaml(summary)}")
        lines.append(f"math: {'true' if '$' in body else 'false'}")
        lines.append(f"top: {tops.get(lid, 0)}")
        if hidden:
            lines.append("hidden: true")
        lines.append(f"source: https://www.luogu.com.cn/article/{lid}")
        lines.append(f"slug: {lid}")
        lines.append("---")
        lines.append("")
        lines.append(body)
        lines.append("")

        (OUT / f"{lid}.md").write_text("\n".join(lines), encoding="utf-8")
        made += 1

    print(f"已生成 {made} 篇到 {OUT}")


if __name__ == "__main__":
    main()
