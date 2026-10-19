"""读取「我的专栏」后台的全部文章（274 篇），区分公开、推荐与未公开。"""

from __future__ import annotations

import json
import math
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from fetch_luogu import DATA, extract_ctx, get, new_session


def page_items(page: int) -> dict:
    session = new_session()
    html = get(f"https://www.luogu.com.cn/article/mine?page={page}", session)
    ctx = extract_ctx(html)
    if not ctx:
        raise RuntimeError(f"第 {page} 页没有数据")
    return ctx["data"]


first = page_items(1)
total = first["articles"]["count"]
per_page = first["articles"]["perPage"]
pages = math.ceil(total / per_page)
items = list(first["articles"]["result"])
print(f"共 {total} 篇，{pages} 页；统计字段 {first.get('stat')}")

with ThreadPoolExecutor(max_workers=4) as pool:
    futures = {pool.submit(page_items, p): p for p in range(2, pages + 1)}
    for fut in as_completed(futures):
        items.extend(fut.result()["articles"]["result"])


def visible(entry: dict) -> bool:
    """status=2 已通过并公开；其余（草稿、审核中、未通过）视为隐藏。"""
    return str(entry.get("status")) == "2"


public = [it for it in items if visible(it)]
hidden = [it for it in items if not visible(it)]
print("总数", len(items), "公开", len(public), "隐藏", len(hidden))
print("隐藏文章 status 分布:", Counter(str(it.get("status")) for it in hidden))
print("公开文章 promoteStatus 分布:", Counter(str(it.get("promoteStatus")) for it in public))

(DATA / "mine.json").write_text(
    json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8"
)
(DATA / "hidden_lids.json").write_text(
    json.dumps([it["lid"] for it in hidden], ensure_ascii=False), encoding="utf-8"
)
print("已写入", DATA / "mine.json")
