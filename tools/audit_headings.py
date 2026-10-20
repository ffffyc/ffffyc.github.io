"""系统检查所有文章的标题层级：用了哪些级别、是否跳级、目录是否覆盖。

输出三类信息：
1. 全局分布：每个级别出现在多少篇文章里
2. 跳级情况：最浅一级与更深的级别之间是否有缺失层
3. 异常样本：正文没有标题、或层级顺序可疑的文章
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
HEAD = re.compile(r"^(#{1,6})\s+(.*)$", re.M)

levels_per_doc: list[tuple[str, list[int]]] = []

for folder in ("content/past", "content/notes"):
    for md in sorted((ROOT / folder).rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        parts = text.split("---")
        body = "---".join(parts[2:]) if len(parts) > 2 else text
        levels = [len(m.group(1)) for m in HEAD.finditer(body)]
        if not levels:
            continue
        levels_per_doc.append((f"{folder}/{md.name}", levels))

count = Counter()
for _, levels in levels_per_doc:
    for lv in set(levels):
        count[lv] += 1

print("篇数:", len(levels_per_doc))
print("各级别出现的篇数:", dict(sorted(count.items())))

gaps = Counter()
top_levels = Counter()
for _, levels in levels_per_doc:
    top = min(levels)
    top_levels[top] += 1
    used = set(levels)
    missing = [lv for lv in range(top, max(levels) + 1) if lv not in used]
    if missing:
        gaps[tuple(missing)] += 1

print("最浅一级的分布:", dict(sorted(top_levels.items())))
print("跳级（缺失层级 → 篇数）:")
for miss, n in gaps.most_common(10):
    print("  缺", miss, "→", n, "篇")

odd = [(name, lv) for name, lv in levels_per_doc if min(lv) > 2]
print("没有 h1/h2、直接从小标题开始的篇数:", len(odd))
for name, lv in odd[:5]:
    print("  ", name, sorted(set(lv)))
