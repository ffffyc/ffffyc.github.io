"""解锁一篇隐藏文章并截图。"""

import base64
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("CDP_PORT", "9223")

from cdp import Session  # noqa: E402

lid = sys.argv[1] if len(sys.argv) > 1 else "zb4f1qz8"
out = Path(sys.argv[2] if len(sys.argv) > 2 else "shot-hidden-post.png")

s = Session()
s.send("Emulation.setDeviceMetricsOverride", width=1500, height=1050, deviceScaleFactor=1, mobile=False)
s.goto(f"http://127.0.0.1:8811/hidden/{lid}/", wait=3)
s.js("document.getElementById('lock-pass').value='ansk99';"
     "document.getElementById('lock-form').requestSubmit();")
time.sleep(3)
data = s.send("Page.captureScreenshot", format="png")["data"]
out.write_bytes(base64.b64decode(data))
print("已保存", out, "| 目录", s.js("document.querySelectorAll('#secret-toc a').length"),
      "| 报错", s.js("document.querySelectorAll('.katex-error').length"))
s.close()
