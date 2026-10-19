"""抓取洛谷专栏的文章清单与全文，原始数据存到 tools/data/。

用法：
    python fetch_luogu.py list       只抓清单
    python fetch_luogu.py articles   按清单抓全文（可重复执行，已抓过的跳过）
"""

from __future__ import annotations

import json
import math
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

UID = 365127
BASE = "https://www.luogu.com.cn"
HEAD = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.luogu.com.cn/",
}
DATA = Path(__file__).resolve().parent / "data"
DATA.mkdir(exist_ok=True)
ART_DIR = DATA / "articles"
ART_DIR.mkdir(exist_ok=True)


def extract_ctx(html: str) -> dict | None:
    marker = 'id="lentille-context"'
    i = html.find(marker)
    if i < 0:
        return None
    start = html.find(">", i) + 1
    end = html.find("</script>", start)
    try:
        return json.loads(html[start:end])
    except json.JSONDecodeError:
        return None


def new_session() -> requests.Session:
    session = requests.Session()
    ck = DATA / "cookies.json"
    if ck.exists():
        session.cookies.update(json.loads(ck.read_text(encoding="utf-8")))
    return session


def get(url: str, session: requests.Session) -> str:
    last = None
    for _ in range(3):
        try:
            r = session.get(url, headers=HEAD, timeout=25)
            if r.status_code == 200:
                return r.text
            last = f"HTTP {r.status_code}"
        except Exception as exc:  # noqa: BLE001
            last = str(exc)
        time.sleep(1.5)
    raise RuntimeError(f"{url} 失败：{last}")


def fetch_list() -> list[dict]:
    session = new_session()
    first = extract_ctx(get(f"{BASE}/user/{UID}/article?page=1", session))
    if not first:
        raise RuntimeError("清单页没有数据")
    total = first["data"]["articles"]["count"]
    per_page = first["data"]["articles"]["perPage"]
    pages = math.ceil(total / per_page)
    print(f"共 {total} 篇，分 {pages} 页")

    items: list[dict] = list(first["data"]["articles"]["result"])
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {
            pool.submit(get, f"{BASE}/user/{UID}/article?page={p}", new_session()): p
            for p in range(2, pages + 1)
        }
        for fut in as_completed(futures):
            ctx = extract_ctx(fut.result())
            items.extend(ctx["data"]["articles"]["result"])
    order = {it["lid"]: i for i, it in enumerate(items)}
    (DATA / "list.json").write_text(
        json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(f"清单写入 {DATA / 'list.json'}，{len(items)} 篇")
    return items


def fetch_article(lid: str) -> dict:
    target = ART_DIR / f"{lid}.json"
    if target.exists():
        return json.loads(target.read_text(encoding="utf-8"))
    session = new_session()
    ctx = extract_ctx(get(f"{BASE}/article/{lid}", session))
    if not ctx or "article" not in ctx.get("data", {}):
        raise RuntimeError(f"{lid} 无正文")
    art = ctx["data"]["article"]
    target.write_text(json.dumps(art, ensure_ascii=False), encoding="utf-8")
    return art


def fetch_articles() -> None:
    items = json.loads((DATA / "list.json").read_text(encoding="utf-8"))
    todo = [it for it in items if not (ART_DIR / f"{it['lid']}.json").exists()]
    print(f"待抓 {len(todo)} 篇")
    done = 0
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(fetch_article, it["lid"]): it for it in todo}
        for fut in as_completed(futures):
            it = futures[fut]
            try:
                fut.result()
            except Exception as exc:  # noqa: BLE001
                print("失败", it["lid"], it.get("title"), exc)
            done += 1
            if done % 20 == 0:
                print(f"进度 {done}/{len(todo)}", flush=True)
    print("全部完成")


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "list"
    if action == "list":
        fetch_list()
    else:
        fetch_articles()
