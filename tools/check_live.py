"""测量线上几个文件页的实际宽度，确认布局是否统一。"""

import json
import os

os.environ.setdefault("CDP_PORT", "9223")
from cdp import Session  # noqa: E402

JS = (
    "JSON.stringify({"
    "main: Math.round(document.querySelector('main').getBoundingClientRect().width),"
    "post: Math.round(document.querySelector('.post').getBoundingClientRect().width),"
    "frame: document.querySelector('.pdf-frame') ? "
    "Math.round(document.querySelector('.pdf-frame').getBoundingClientRect().width) : 0,"
    "cls: document.querySelector('main').className"
    "})"
)

URLS = (
    "https://ffffyc.github.io/notes/advanced-calculus-1/tutorial-1-solution/",
    "https://ffffyc.github.io/notes/advanced-calculus-1/tutorial-1/",
    "https://ffffyc.github.io/notes/linear-algebra/homework-1-solution/",
    "https://ffffyc.github.io/notes/sys-intro/slide-5/",
)

s = Session()
for url in URLS:
    s.goto(url, wait=3)
    print(url.rsplit("/", 2)[-2], json.loads(s.js(JS)))
s.close()
