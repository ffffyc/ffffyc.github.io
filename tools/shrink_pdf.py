"""把体积过大的课件 PDF 按页栅格化重压，缩到适合网页传输的大小。

用法：python tools/shrink_pdf.py <输入.pdf> <输出.pdf> [dpi]
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

import pymupdf


def shrink(src: Path, dst: Path, dpi: int = 144, quality: int = 78) -> None:
    doc = pymupdf.open(src)
    out = pymupdf.open()
    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        img = pix.tobytes("jpeg", jpg_quality=quality)
        new = out.new_page(width=page.rect.width, height=page.rect.height)
        new.insert_image(new.rect, stream=img)
    out.save(dst, garbage=4, deflate=True)
    out.close()
    doc.close()
    print(f"{src.name}: {src.stat().st_size / 1048576:.1f} MB -> {dst.stat().st_size / 1048576:.1f} MB")


if __name__ == "__main__":
    shrink(Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 144)
