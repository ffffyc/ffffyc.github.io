"""同步线性代数笔记：更新第 1–4 讲，新增第 5 讲（中英各一份）。"""

from __future__ import annotations

import shutil
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(r"C:\Users\Rain\Desktop\THU\2026 秋\线性代数\Notes")
FILES = ROOT / "static" / "files" / "notes" / "linear-algebra"
CONTENT = ROOT / "content" / "notes" / "linear-algebra"

FILES.mkdir(parents=True, exist_ok=True)

for n in range(1, 6):
    for lang in ("zh", "en"):
        src = SRC / f"Lecture{n}_notes_{lang}.pdf"
        if not src.exists():
            print("缺少", src.name)
            continue
        suffix = "cn" if lang == "zh" else "en"
        shutil.copy2(src, FILES / f"note-lecture-{n}-{suffix}.pdf")
        md = CONTENT / f"note-lecture-{n}-{suffix}.md"
        if md.exists():
            text = md.read_text(encoding="utf-8")
            text = re.sub(r"^order:.*$", f"order: {n}", text, flags=re.M)
            md.write_text(text, encoding="utf-8")
            print("更新", md.name)
        else:
            cn = "零一二三四五六七八九十"[n] if n <= 10 else str(n)
            title = f"第{cn}讲笔记-" + ("CN" if suffix == "cn" else "EN")
            body = (
                "---\n"
                f'title: "{title}"\n'
                "kind: note\n"
                f"order: {n}\n"
                f"pdf: files/notes/linear-algebra/note-lecture-{n}-{suffix}.pdf\n"
                "tags: []\n"
                "---\n"
            )
            md.write_text(body, encoding="utf-8")
            print("新增", md.name)
