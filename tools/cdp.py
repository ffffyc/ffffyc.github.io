"""极简 Chrome DevTools Protocol 客户端，用于复用已登录的浏览器抓取页面。

依赖：requests、websockets（同步客户端）。
"""

from __future__ import annotations

import json
import os
import time

import requests
from websockets.sync.client import connect

DEBUG_PORT = int(os.environ.get("CDP_PORT", "9222"))


def _targets() -> list[dict]:
    r = requests.get(f"http://127.0.0.1:{DEBUG_PORT}/json/list", timeout=5)
    r.raise_for_status()
    return r.json()


def page_ws(url_part: str | None = None) -> str:
    pages = [t for t in _targets() if t.get("type") == "page"]
    if url_part:
        for p in pages:
            if url_part in p.get("url", ""):
                return p["webSocketDebuggerUrl"]
    if not pages:
        raise RuntimeError("没有可用的页面目标")
    return pages[0]["webSocketDebuggerUrl"]


class Session:
    def __init__(self, url_part: str | None = None):
        self.ws = connect(page_ws(url_part), max_size=64 * 1024 * 1024)
        self.n = 0
        self.send("Page.enable")
        self.send("Runtime.enable")

    def send(self, method: str, **params):
        self.n += 1
        msg_id = self.n
        self.ws.send(json.dumps({"id": msg_id, "method": method, "params": params}))
        while True:
            data = json.loads(self.ws.recv())
            if data.get("id") == msg_id:
                if "error" in data:
                    raise RuntimeError(f"{method}: {data['error']}")
                return data.get("result", {})

    def goto(self, url: str, wait: float = 2.5) -> None:
        self.send("Page.navigate", url=url)
        time.sleep(wait)

    def js(self, expression: str):
        r = self.send(
            "Runtime.evaluate",
            expression=expression,
            returnByValue=True,
            awaitPromise=True,
        )
        return r.get("result", {}).get("value")

    def close(self) -> None:
        try:
            self.ws.close()
        except Exception:
            pass


def context_json(session: Session) -> dict | None:
    """取洛谷页面内嵌的 lentille-context 数据。"""
    raw = session.js(
        "(() => { const e = document.getElementById('lentille-context');"
        " return e ? e.textContent : null; })()"
    )
    if not raw:
        return None
    return json.loads(raw)
