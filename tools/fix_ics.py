"""重整计算机入门的作业文件：题面公开、学生解答加密、官方答案公开。

区分依据（看首段文字）：
  题面   intro2cs-hw-N.pdf / Intro2CS_HW4.pdf        以 "Due: ..." 开头
  解答   Homework*.pdf                               以 "Homework N  <姓名>" 开头
  答案   *_Answer.pdf                                以 "Homework N Answer" 开头
"""

from __future__ import annotations

import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(r"C:\Users\Rain\Desktop\THU\2026 秋\计算机入门")
PUB = ROOT / "static" / "files" / "notes" / "introduction-to-cs"
PRIV = ROOT / "static" / "private" / "notes" / "introduction-to-cs"
CONTENT = ROOT / "content" / "notes" / "introduction-to-cs"

# 周次（表格行）、题面、学生解答、官方答案
PLAN = [
    (1, 1, "Week1/intro2cs-hw-1.pdf", "Week1/Homework1.pdf", "Week1/Intro_to_CS_HW_1_Answer.pdf"),
    (2, 2, "Week2/intro2cs-hw-2.pdf", "Week2/Homework_Intro2cs_2.pdf", "Week2/Intro2CS_HW2_Answer.pdf"),
    (3, 3, "Week3/intro2cs-hw-3-v2.pdf", "Week3/Homework__Intro2cs_3.pdf", None),
    (4, 5, "Week5/Intro2CS_HW4.pdf", "Week5/Homework_Intro2cs_4.pdf", None),
]

CN = {1: "一", 2: "二", 3: "三", 4: "四"}


def write_md(
    name: str, title: str, kind: str, order: int, pdf: str, hidden: bool = False, short: str = ""
) -> None:
    lines = ["---", f'title: "{title}"', f"kind: {kind}", f"order: {order}"]
    if short:
        lines.append(f'short: "{short}"')
    lines.append(f"pdf: {pdf}")
    if hidden:
        lines.append("hidden: true")
    lines += ["tags: []", "---", ""]
    (CONTENT / name).write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    PUB.mkdir(parents=True, exist_ok=True)
    PRIV.mkdir(parents=True, exist_ok=True)
    for n, week, sheet, own, answer in PLAN:
        shutil.copy2(SRC / sheet, PUB / f"homework-{n}.pdf")
        write_md(f"homework-{n}.md", f"第{CN[n]}次作业", "homework", week, f"files/notes/introduction-to-cs/homework-{n}.pdf")

        shutil.copy2(SRC / own, PRIV / f"homework-{n}-solution.pdf")
        write_md(
            f"homework-{n}-solution.md",
            f"第{CN[n]}次作业解答",
            "homework",
            week,
            f"private/notes/introduction-to-cs/homework-{n}-solution.pdf",
            hidden=True,
        )

        if answer:
            shutil.copy2(SRC / answer, PUB / f"homework-{n}-answer.pdf")
            write_md(
                f"homework-{n}-answer.md",
                f"第{CN[n]}次作业答案",
                "answer",
                week,
                f"files/notes/introduction-to-cs/homework-{n}-answer.pdf",
                short="答案",
            )

    meta_path = CONTENT / "_subject.yaml"
    meta = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
    meta["columns"] = ["slide", "homework", "answer"]
    meta_path.write_text(yaml.safe_dump(meta, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print("done", meta["columns"])


if __name__ == "__main__":
    main()
