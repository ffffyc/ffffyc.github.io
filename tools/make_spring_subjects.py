"""为 2026 春 的三门课建立科目配置。"""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "content" / "notes"

SUBJECTS = {
    "sys-intro": ("计算机系统概论", "Introduction to Computer Systems", 1),
    "math4csai": ("计算机与人工智能应用数学", "Mathematics for Computer Science and AI", 2),
    "theory-of-computation": ("计算理论", "Theory of Computation", 3),
}

for slug, (name, name_en, order) in SUBJECTS.items():
    folder = NOTES / slug
    folder.mkdir(parents=True, exist_ok=True)
    data = {
        "name": name,
        "name_en": name_en,
        "order": order,
        "term": "2026 春",
        "unit": "次",
        "columns": ["homework", "solution"],
        "show_text": False,
    }
    (folder / "_subject.yaml").write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )
    syl = folder / "_syllabus.yaml"
    if not syl.exists():
        syl.write_text('# 留空则不显示涉及内容\n1: ""\n', encoding="utf-8")
    print(slug, name)
