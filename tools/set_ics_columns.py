"""计入门的列：次 / 课件 / 作业（作业 · 解答 · 答案 并在同一格）。"""

from pathlib import Path

import yaml

FOLDER = Path(__file__).resolve().parent.parent / "content" / "notes" / "introduction-to-cs"

meta_path = FOLDER / "_subject.yaml"
meta = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
meta["columns"] = ["slide", "homework"]
meta.pop("inline_solutions", None)
meta_path.write_text(yaml.safe_dump(meta, allow_unicode=True, sort_keys=False), encoding="utf-8")

for n in (1, 2, 3, 4):
    p = FOLDER / f"homework-{n}-solution.md"
    if not p.exists():
        continue
    text = p.read_text(encoding="utf-8")
    if "seq:" not in text:
        text = text.replace("kind: homework", "kind: homework\nseq: 2")
        p.write_text(text, encoding="utf-8")
    a = FOLDER / f"homework-{n}-answer.md"
    if a.exists():
        text = a.read_text(encoding="utf-8")
        if "seq:" not in text:
            text = text.replace("kind: answer", "kind: answer\nseq: 3")
            a.write_text(text, encoding="utf-8")

print(meta["columns"])
