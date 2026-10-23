"""逐份比对素材与站内文件的哈希，列出需要同步的内容。"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THU = Path(r"C:\Users\Rain\Desktop\THU\2026 秋")

PAIRS: list[tuple[Path, Path]] = []


def add(src: Path, dst: Path) -> None:
    PAIRS.append((src, dst))


# 线代：第 1–5 讲中英笔记
for n in range(1, 6):
    for lang, suffix in (("zh", "cn"), ("en", "en")):
        add(
            THU / "线性代数" / "Notes" / f"Lecture{n}_notes_{lang}.pdf",
            ROOT / "static" / "files" / "notes" / "linear-algebra" / f"note-lecture-{n}-{suffix}.pdf",
        )

# 线代：作业题面（公开）与自己写的解答（加密）
for week, n in ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)):
    add(
        THU / "线性代数" / f"Lecture {week}" / f"Linear_Algebra_Homework{n}.pdf",
        ROOT / "static" / "files" / "notes" / "linear-algebra" / f"homework-{n}.pdf",
    )
for week, src_name, dst_name in (
    (1, "Homework1.pdf", "homework-1-solution.pdf"),
    (2, "Homework2.pdf", "homework-2-solution.pdf"),
    (3, "Homework__Linear_Algebra_3.pdf", "homework-3-solution.pdf"),
    (4, "Homework_Linear_Algebra_4.pdf", "homework-4-solution.pdf"),
):
    add(
        THU / "线性代数" / f"Lecture {week}" / src_name,
        ROOT / "static" / "private" / "notes" / "linear-algebra" / dst_name,
    )

# 线代第二次习题课
add(
    THU / "线性代数" / "Lecture 4" / "tutorial_session_1016.pdf",
    ROOT / "static" / "files" / "notes" / "linear-algebra" / "tutorial-2.pdf",
)
add(
    THU / "线性代数" / "Lecture 4" / "Tutorial_Session_1016_.pdf",
    ROOT / "static" / "files" / "notes" / "linear-algebra" / "tutorial-2-record.pdf",
)

# 高微：作业题面（《高等微积分1》第N次作业，公开）与自己写的解答（HomeworkN，加密）
AC = THU / "高等微积分" / "Homeworks"
for n, order in ((1, 1), (2, 2), (3, 4), (4, 5), (5, 6)):
    add(
        AC / f"《高等微积分1》第{['一', '二', '三', '四', '五'][n - 1]}次作业.pdf",
        ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / f"homework-{n}.pdf",
    )
    add(
        AC / f"Homework{n}.pdf",
        ROOT / "static" / "private" / "notes" / "advanced-calculus-1" / f"homework-{n}-solution.pdf",
    )

# 高微：六周笔记 + 10-23 课堂记录
for n in range(1, 7):
    add(
        THU / "高等微积分" / "Notes" / f"高等微积分1_第{n}周笔记.pdf",
        ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / f"note-week-{n}.pdf",
    )
add(
    THU / "高等微积分" / "Records" / "2026年10月23日高微记录.pdf",
    ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / "record-2026-10-23.pdf",
)

# 高微习题课
add(
    THU / "高等微积分" / "习题课" / "2026年秋季《高等微积分1》第一次习题课材料.pdf",
    ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / "tutorial-1.pdf",
)
add(
    THU / "高等微积分" / "习题课" / "2026年秋季《高等微积分1》第一次习题课材料参考解答.pdf",
    ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / "tutorial-1-solution.pdf",
)
add(
    THU / "高等微积分" / "习题课" / "2026年秋季《高等微积分1》第二次习题课材料.pdf",
    ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / "tutorial-2.pdf",
)
add(
    THU / "高等微积分" / "习题课" / "高等微积分-第5周习题课.pdf",
    ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / "tutorial-week-5.pdf",
)
add(
    THU / "高等微积分" / "习题课" / "高等微积分-第6周习题课.pdf",
    ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / "tutorial-week-6.pdf",
)
add(
    THU / "高等微积分" / "习题课" / "2026年秋季《高等微积分1》第一次习题课材料参考解答.pdf",
    ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / "tutorial-1-solution.pdf",
)
add(
    THU / "高等微积分" / "Notes" / "练习题集" / "高等微积分1_公式手册.pdf",
    ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / "formula-handbook.pdf",
)

# 计入门：课件与作业
for week in (1, 2, 3, 5, 6):
    for src in sorted((THU / "计算机入门" / f"Week{week}").glob("week0?-prof-*.pdf")):
        add(src, ROOT / "static" / "files" / "notes" / "introduction-to-cs" / f"slide-week-{week}.pdf")

ICS = ROOT / "static" / "files" / "notes" / "introduction-to-cs"
ICS_PRIVATE = ROOT / "static" / "private" / "notes" / "introduction-to-cs"
CS = THU / "计算机入门"
# 题面（公开）
for week, src, dst in (
    (1, "intro2cs-hw-1.pdf", "homework-1.pdf"),
    (2, "intro2cs-hw-2.pdf", "homework-2.pdf"),
    (3, "intro2cs-hw-3-v2.pdf", "homework-3.pdf"),
    (5, "Intro2CS_HW4.pdf", "homework-4.pdf"),
    (6, "Intro_to_CS_HW_Week_6.pdf", "homework-5.pdf"),
):
    add(CS / f"Week{week}" / src, ICS / dst)
# 官方答案（公开）
for week, src, dst in (
    (1, "Intro_to_CS_HW_1_Answer.pdf", "homework-1-answer.pdf"),
    (2, "Intro2CS_HW2_Answer.pdf", "homework-2-answer.pdf"),
):
    add(CS / f"Week{week}" / src, ICS / dst)
# 自己写的解答（加密）
for week, src, dst in (
    (1, "Homework1.pdf", "homework-1-solution.pdf"),
    (2, "Homework_Intro2cs_2.pdf", "homework-2-solution.pdf"),
    (3, "Homework__Intro2cs_3.pdf", "homework-3-solution.pdf"),
    (5, "Homework_Intro2cs_4.pdf", "homework-4-solution.pdf"),
):
    add(CS / f"Week{week}" / src, ICS_PRIVATE / dst)

# 计入门：习题课（TA 讲解材料）
for src, dst in (
    ("Week1/week01-office-hour/Intro to LaTeX.pdf", "tutorial-week-1.pdf"),
    ("Week2/week02-paper-reading.pdf", "tutorial-week-2.pdf"),
    ("Week3/week03-paper-reading.pdf", "tutorial-week-3.pdf"),
    ("Week6/week06-linux.pdf", "tutorial-week-6.pdf"),
):
    add(THU / "计算机入门" / src, ICS / dst)
# 第五周在 zip 里，解包后单独比对
LLM_PDF = (
    Path(os.environ.get("TEMP", ""))
    / "ics_oh"
    / "week05-office-hour-responsible-use-of-llm-for-information-search.pdf"
)
if LLM_PDF.exists():
    add(LLM_PDF, ICS / "tutorial-week-5.pdf")

# 算法设计：第五次作业题面与解答
add(
    THU / "算法设计" / "Homework" / "Homework5" / "hw5.pdf",
    ROOT / "static" / "files" / "notes" / "algorithm-design" / "homework-5.pdf",
)
add(
    THU / "算法设计" / "Homework" / "Homework5" / "Homework_Algorithm_Design_5.pdf",
    ROOT / "static" / "private" / "notes" / "algorithm-design" / "homework-5-solution.pdf",
)


# 课程安排相关文件
add(
    THU / "线性代数" / "Lecture 1" / "Lecture 1.pptx",
    ROOT / "static" / "files" / "notes" / "linear-algebra" / "lecture-1.pptx",
)
add(
    THU / "计算机入门" / "Week1" / "week01-course-info.pdf",
    ROOT / "static" / "files" / "notes" / "introduction-to-cs" / "course-info.pdf",
)

# 计应数（2026 春）：整本课程笔记（放在 books 目录，属于参考资料）
add(
    Path(r"C:\Users\Rain\Desktop\THU\2026 春\计算机与人工智能应用数学\lecture_notes.pdf"),
    ROOT / "static" / "files" / "books" / "math4csai" / "lecture-notes.pdf",
)


def md5(p: Path) -> str:
    h = hashlib.md5()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


same, stale, missing_dst, missing_src = [], [], [], []
for src, dst in PAIRS:
    if not src.exists():
        missing_src.append(src.name)
        continue
    if not dst.exists():
        missing_dst.append(dst)
        continue
    (same if md5(src) == md5(dst) else stale).append((src, dst))

print(f"一致 {len(same)} 份")
for src, dst in stale:
    print(f"  [待同步] {src.name} -> {dst.name}")
for dst in missing_dst:
    print(f"  [站内缺失] {dst}")
for name in missing_src:
    print(f"  [素材缺失] {name}")
