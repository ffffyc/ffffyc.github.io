"""把「题面」与「学生解答」换回正确位置。

原先公开的 homework-N.pdf 其实是自己写的解答（带姓名），加密的 *-solution.pdf 反而是题面。
互换两者内容，条目路径不变：公开 = 题面，加密 = 解答。
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "static" / "files" / "notes"
PRIV = ROOT / "static" / "private" / "notes"
COURSES = ("linear-algebra", "algorithm-design", "math4csai")

for course in COURSES:
    pub_dir, priv_dir = PUB / course, PRIV / course
    if not priv_dir.exists():
        print("skip", course)
        continue
    for sheet in sorted(pub_dir.glob("homework-*.pdf")):
        if sheet.stem.endswith(("-solution", "-answer")):
            continue
        n = sheet.stem.split("-")[-1]
        solution = priv_dir / f"homework-{n}-solution.pdf"
        if not solution.exists():
            print("  missing solution", course, n)
            continue
        tmp = sheet.with_suffix(".swap")
        sheet.rename(tmp)
        solution.rename(sheet)
        tmp.rename(solution)
        print(f"  swapped {course} homework-{n}")
print("done")
