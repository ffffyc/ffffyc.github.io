"""复制 2026 春 课程的课本与讲义。"""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THU = Path(r"C:\Users\Rain\Desktop\THU\2026 春")

RES = {
    "math4csai": [
        ("计算机与人工智能应用数学/lecture_notes.pdf", "lecture-notes.pdf"),
        ("计算机与人工智能应用数学/Discrete-Mathematics.pdf", "discrete-mathematics.pdf"),
    ],
}

for slug, items in RES.items():
    dest = ROOT / "static" / "files" / "books" / slug
    dest.mkdir(parents=True, exist_ok=True)
    for src_rel, name in items:
        src = THU / src_rel
        target = dest / name
        if not src.exists():
            print("缺失", src_rel)
            continue
        if not target.exists():
            shutil.copy2(src, target)
        print("复制", name, f"{target.stat().st_size / 1048576:.1f} MB")
