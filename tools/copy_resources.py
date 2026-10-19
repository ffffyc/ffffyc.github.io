"""把课本与讲义复制到 static/files/books，并写进各科目 _subject.yaml 的 resources。"""

from __future__ import annotations

import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
THU = Path(r"C:\Users\Rain\Desktop\THU\2026 秋")
BOOKS = ROOT / "static" / "files" / "books"
NOTES = ROOT / "content" / "notes"

RES = {
    "linear-algebra": [
        ("线性代数/David C. Lay—Linear Algebra and Its Applications 4e.pdf", "lay-4e.pdf", "Linear Algebra and Its Applications（Lay，4e）"),
        ("线性代数/[[Stephen_H._Friedberg_Arnold_J._Insel_Lawrence_E] Linear algebra.pdf", "friedberg-4e.pdf", "Linear Algebra（Friedberg / Insel / Spence，4e）"),
    ],
    "advanced-calculus-1": [
        ("高等微积分/《高等微积分》讲义.pdf", "lecture-notes.pdf", "《高等微积分》讲义（艾颖华）"),
        ("高等微积分/2026年秋季《高等微积分1》课程安排.pdf", "schedule.pdf", "2026 年秋季课程安排"),
        ("高等微积分/数学分析教程（上册）（第3版）(常庚哲_史济怀)(z-library.sk_1lib.sk_z-li.pdf", "analysis-textbook.pdf", "数学分析教程（上册，常庚哲 / 史济怀）"),
        ("高等微积分/全国大学生数学竞赛（非数学专业）分类题目.pdf", "contest-problems.pdf", "全国大学生数学竞赛分类题目"),
    ],
    "algorithm-design": [
        ("算法设计/Algorithm Design (Jon Kleinberg, Éva Tardos).pdf", "kleinberg-tardos.pdf", "Algorithm Design（Kleinberg / Tardos）"),
        ("算法设计/Introduction to Algorithms.pdf", "clrs.pdf", "Introduction to Algorithms（CLRS）"),
        ("算法设计/lec7.pdf", "lec7.pdf", "课程讲义 lec7"),
        ("算法设计/lec8.pdf", "lec8.pdf", "课程讲义 lec8"),
        ("算法设计/scc.pdf", "scc.pdf", "课程讲义 scc"),
    ],
}


def main() -> None:
    BOOKS.mkdir(parents=True, exist_ok=True)
    for slug, items in RES.items():
        dest_dir = BOOKS / slug
        dest_dir.mkdir(parents=True, exist_ok=True)
        entries = []
        for src_rel, name, title in items:
            src = THU / src_rel
            if not src.exists():
                print("缺失", src_rel)
                continue
            target = dest_dir / name
            if not target.exists():
                shutil.copy2(src, target)
            entries.append({"title": title, "file": f"files/books/{slug}/{name}"})

        yml = NOTES / slug / "_subject.yaml"
        data = yaml.safe_load(yml.read_text(encoding="utf-8")) or {}
        data["resources"] = entries
        yml.write_text(
            yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8"
        )
        print(slug, len(entries), "份参考资料")


if __name__ == "__main__":
    main()
