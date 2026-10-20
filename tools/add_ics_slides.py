"""给计算机入门补课件条目：每周一个 slide 条目，表格加「课件」列。"""

from pathlib import Path

import yaml

FOLDER = Path(__file__).resolve().parent.parent / "content" / "notes" / "introduction-to-cs"
TITLES = {1: "第一周课件", 2: "第二周课件", 3: "第三周课件", 5: "第五周课件"}

for n, title in TITLES.items():
    body = (
        "---\n"
        f'title: "{title}"\n'
        "kind: slide\n"
        f"order: {n}\n"
        f"pdf: files/notes/introduction-to-cs/slide-week-{n}.pdf\n"
        "tags: []\n"
        "---\n"
    )
    (FOLDER / f"slide-{n}.md").write_text(body, encoding="utf-8")

meta_path = FOLDER / "_subject.yaml"
meta = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
meta["columns"] = ["slide", "homework"]
meta.pop("show_text", None)
meta_path.write_text(yaml.safe_dump(meta, allow_unicode=True, sort_keys=False), encoding="utf-8")
print(meta)
