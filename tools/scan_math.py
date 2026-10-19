"""抽查若干页面，统计 KaTeX 报错与折叠嵌套情况。"""

import os
import random
import time
from pathlib import Path

os.environ.setdefault("CDP_PORT", "9223")

from cdp import Session  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
pages = [p.parent.name for p in (ROOT / "docs" / "past").glob("*/index.html")]
random.seed(7)
sample = random.sample(pages, 6)

s = Session()
for name in sample:
    s.goto(f"http://127.0.0.1:8811/past/{name}/", wait=4)
    print(
        name,
        "| 报错", s.js("document.querySelectorAll('.katex-error').length"),
        "| 公式", s.js("document.querySelectorAll('.katex').length"),
        "| 折叠", s.js("document.querySelectorAll('details.fold').length"),
        "| 嵌套", s.js("document.querySelectorAll('details.fold details.fold').length"),
    )
s.close()
