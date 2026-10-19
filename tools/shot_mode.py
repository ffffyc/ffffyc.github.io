"""按指定配色模式截图，便于对比白天与夜间外观。"""

import base64
import os
import sys
from pathlib import Path

os.environ.setdefault("CDP_PORT", "9223")

from cdp import Session  # noqa: E402

mode = sys.argv[1] if len(sys.argv) > 1 else "light"
url = sys.argv[2] if len(sys.argv) > 2 else "http://127.0.0.1:8811/"
out = Path(sys.argv[3] if len(sys.argv) > 3 else f"shot-{mode}.png")

s = Session()
s.send("Emulation.setDeviceMetricsOverride", width=1400, height=950, deviceScaleFactor=1, mobile=False)
s.send("Emulation.setEmulatedMedia", features=[{"name": "prefers-color-scheme", "value": mode}])
s.goto(url, wait=5)
data = s.send("Page.captureScreenshot", format="png")["data"]
out.write_bytes(base64.b64decode(data))
print("已保存", out)
s.close()
