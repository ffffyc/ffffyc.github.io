"""放大截图，便于核对小图标。"""

import base64
import os
import sys
from pathlib import Path

os.environ.setdefault("CDP_PORT", "9223")

from cdp import Session  # noqa: E402

url, out = sys.argv[1], sys.argv[2]
scale = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0

s = Session()
s.send("Emulation.setDeviceMetricsOverride", width=900, height=520, deviceScaleFactor=scale, mobile=False)
s.goto(url, wait=3)
data = s.send("Page.captureScreenshot", format="png")["data"]
Path(out).write_bytes(base64.b64decode(data))
print("已保存", out)
s.close()
