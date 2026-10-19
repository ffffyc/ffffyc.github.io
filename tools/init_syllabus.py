"""给每门课补上表格列配置与 _syllabus.yaml 骨架。"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "content" / "notes"

CONF = {
    "advanced-calculus-1": ("周", ["record", "note", "homework", "solution", "tutorial"]),
    "linear-algebra": ("讲", ["note", "homework", "solution"]),
    "algorithm-design": ("次", ["homework", "solution"]),
    "introduction-to-cs": ("周", ["homework", "solution"]),
}

for slug, (unit, columns) in CONF.items():
    folder = NOTES / slug
    if not folder.exists():
        continue
    yml = folder / "_subject.yaml"
    text = yml.read_text(encoding="utf-8")
    if "unit:" not in text:
        text = text.rstrip("\n") + f"\nunit: {unit}\n"
    if "columns:" not in text:
        text += "columns: [" + ", ".join(columns) + "]\n"
    yml.write_text(text, encoding="utf-8")

    orders = set()
    for md in folder.glob("*.md"):
        m = re.search(r"^order: (\d+)", md.read_text(encoding="utf-8"), re.M)
        if m and int(m.group(1)):
            orders.add(int(m.group(1)))

    syl = folder / "_syllabus.yaml"
    old = {}
    if syl.exists():
        import yaml

        old = yaml.safe_load(syl.read_text(encoding="utf-8")) or {}
    lines = ["# 每周/每讲涉及的课程内容，键是周次或讲次；留空则不显示"]
    for n in sorted(orders):
        text = str(old.get(n, "") or "").replace('"', '\\"')
        lines.append(f'{n}: "{text}"')
    syl.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(slug, unit, columns, sorted(orders))
