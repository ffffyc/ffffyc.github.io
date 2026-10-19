"""比较习题课页与作业解答页的容器与阅读器宽度。"""

import os

os.environ.setdefault("CDP_PORT", "9223")
from cdp import Session  # noqa: E402

JS = (
    "JSON.stringify(["
    "document.querySelector('main').getBoundingClientRect().width,"
    "document.querySelector('.pdf-frame') ? "
    "document.querySelector('.pdf-frame').getBoundingClientRect().width : 0"
    "])"
)

s = Session()
for url in (
    "http://127.0.0.1:8811/notes/advanced-calculus-1/tutorial-1/",
    "http://127.0.0.1:8811/notes/linear-algebra/homework-1-solution/",
):
    s.goto(url, wait=2)
    print(url.rsplit("/", 2)[-2], s.js(JS))
s.close()
