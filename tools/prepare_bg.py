"""把桌面壁纸压缩成适合网页的尺寸，放到 static/files/background.jpg。"""

from pathlib import Path

from PIL import Image

SRC = Path(r"D:\QQ\Download\754C9B2A78F851DAC6F3F352152D6C10.jpg")
ROOT = Path(__file__).resolve().parent.parent
DST = ROOT / "static" / "files" / "background.jpg"

img = Image.open(SRC).convert("RGB")
w, h = img.size
print("原图", w, h, f"{SRC.stat().st_size / 1048576:.1f} MB")

if w > 2000:
    img = img.resize((2000, round(h * 2000 / w)), Image.LANCZOS)

img.save(DST, "JPEG", quality=82, optimize=True, progressive=True)
print("输出", DST, f"{DST.stat().st_size / 1024:.0f} KB")
