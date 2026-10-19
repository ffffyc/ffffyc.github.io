"""按需截图若干页面。"""

import base64
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("CDP_PORT", "9223")

from cdp import Session  # noqa: E402

url, out, unlock = sys.argv[1], sys.argv[2], "--unlock" in sys.argv

s = Session()
s.send("Emulation.setDeviceMetricsOverride", width=1300, height=820, deviceScaleFactor=1, mobile=False)
sep = "&" if "?" in url else "?"
s.goto(f"{url}{sep}_={int(time.time())}", wait=3)
if unlock:
    s.js("document.getElementById('lock-pass').value='ansk99';"
         "document.getElementById('lock-form').requestSubmit();")
    time.sleep(3)
    s.js("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(0.6)
    s.js("window.scrollTo(0, 0)")
    time.sleep(0.4)
data = s.send("Page.captureScreenshot", format="png")["data"]
Path(out).write_bytes(base64.b64decode(data))
print("已保存", out)
s.close()
