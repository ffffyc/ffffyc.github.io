"""把当前登录浏览器里洛谷站点的 Cookie 导出到 data/cookies.json，供抓取脚本复用。"""

import json
import os
from pathlib import Path

os.environ.setdefault("CDP_PORT", "9222")

from cdp import Session  # noqa: E402

DATA = Path(__file__).resolve().parent / "data"
s = Session("luogu.com.cn")
res = s.send("Network.getCookies", urls=["https://www.luogu.com.cn/"])
cookies = {c["name"]: c["value"] for c in res.get("cookies", [])}
s.close()
(DATA / "cookies.json").write_text(json.dumps(cookies, ensure_ascii=False), encoding="utf-8")
print("导出 Cookie:", {k: len(v) for k, v in cookies.items()})
