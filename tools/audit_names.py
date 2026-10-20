"""检查站内公开 PDF 里是否出现真实姓名，并按课程列出疑似「学生解答」。"""

from __future__ import annotations

from pathlib import Path

import pymupdf

DOCS = Path(__file__).resolve().parent.parent / "docs" / "files"

for p in sorted(DOCS.rglob("*.pdf")):
    try:
        doc = pymupdf.open(p)
        text = " ".join(doc[0].get_text().split())
        doc.close()
    except Exception:
        continue
    mark = "NAME" if "Yifan" in text or "yifan" in text else "    "
    if p.name.startswith(("homework", "tutorial", "slide")):
        print(f"{mark}  {p.relative_to(DOCS)}  ::  {text[:70]}")
