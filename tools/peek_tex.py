"""打印各周 tex 里 \\author{...} 的首行，确认主题句是否带 LaTeX。"""

import re
from pathlib import Path

NOTES = Path(r"C:\Users\Rain\Desktop\THU\2026 秋\高等微积分\Notes")

for tex in sorted(NOTES.glob("*.tex")):
    text = tex.read_text(encoding="utf-8")
    m = re.search(r"\\author\{(.+?)\}", text, re.S)
    if not m:
        print(tex.name, "NO AUTHOR")
        continue
    first = m.group(1).split("\\\\")[0].strip()
    print(tex.name, "::", first[:90])
