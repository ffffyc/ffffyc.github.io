"""从头像原图生成网站图标。

把分辨率最高的头像放到 static/files/avatar.png（或 .jpg），再运行本脚本：
    python make_favicon.py
"""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
FILES = ROOT / "static" / "files"

src = None
for name in ("avatar.png", "avatar.jpg", "avatar.jpeg", "avatar.webp"):
    candidate = FILES / name
    if candidate.exists():
        src = candidate
        break

if src is None:
    raise SystemExit("没有找到 static/files/avatar.*")

img = Image.open(src).convert("RGBA")
print("原图", src.name, img.size)

side = min(img.size)
left = (img.width - side) // 2
top = (img.height - side) // 2
square = img.crop((left, top, left + side, top + side))

for size in (32, 180, 512):
    out = FILES / f"icon-{size}.png"
    square.resize((size, size), Image.LANCZOS).save(out, "PNG", optimize=True)
    print("输出", out.name)

square.resize((256, 256), Image.LANCZOS).save(
    FILES / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)]
)
print("输出 favicon.ico")
