"""逐份比对素材与站内文件的哈希，列出需要同步的内容。"""

from __future__ import annotations

import hashlib
import io
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THU = Path(r"C:\Users\Rain\Desktop\THU\2026 秋")

PAIRS: list[tuple[Path, Path]] = []


def add(src: Path, dst: Path) -> None:
    PAIRS.append((src, dst))


# 线代：第 1–7 讲中英笔记
for n in range(1, 8):
    for lang, suffix in (("zh", "cn"), ("en", "en")):
        add(
            THU / "线性代数" / "Notes" / f"Lecture{n}_notes_{lang}.pdf",
            ROOT / "static" / "files" / "notes" / "linear-algebra" / f"note-lecture-{n}-{suffix}.pdf",
        )

# 线代：作业题面（公开）与自己写的解答（加密）
for week, n in ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)):
    add(
        THU / "线性代数" / f"Lecture {week}" / f"Linear_Algebra_Homework{n}.pdf",
        ROOT / "static" / "files" / "notes" / "linear-algebra" / f"homework-{n}.pdf",
    )
for week, src_name, dst_name in (
    (1, "Homework1.pdf", "homework-1-solution.pdf"),
    (2, "Homework2.pdf", "homework-2-solution.pdf"),
    (3, "Homework__Linear_Algebra_3.pdf", "homework-3-solution.pdf"),
    (4, "Homework_Linear_Algebra_4.pdf", "homework-4-solution.pdf"),
    (5, "Homework_Linear_Algebra_5.pdf", "homework-5-solution.pdf"),
    (6, "Homework_Linear_Algebra_6.pdf", "homework-6-solution.pdf"),
    (7, "Homework_Linear_Algebra_7.pdf", "homework-7-solution.pdf"),
):
    add(
        THU / "线性代数" / f"Lecture {week}" / src_name,
        ROOT / "static" / "private" / "notes" / "linear-algebra" / dst_name,
    )

# 线代：历年期中试题
for year in (2023, 2025):
    add(
        THU / "线性代数" / f"midterm{year}.pdf",
        ROOT / "static" / "files" / "notes" / "linear-algebra" / f"midterm-{year}.pdf",
    )
add(
    THU / "线性代数" / "linear_algebra-midterm_review.pdf",
    ROOT / "static" / "files" / "notes" / "linear-algebra" / "midterm-review.pdf",
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
add(
    THU / "线性代数" / "Lecture 5" / "第三次习题课课堂记录.pdf",
    ROOT / "static" / "files" / "notes" / "linear-algebra" / "tutorial-3-record.pdf",
)
add(
    THU / "线性代数" / "Lecture 6" / "tutorial_1030.pdf",
    ROOT / "static" / "files" / "notes" / "linear-algebra" / "tutorial-4.pdf",
)
add(
    THU / "线性代数" / "Lecture 7" / "第五次习题课课堂记录.pdf",
    ROOT / "static" / "files" / "notes" / "linear-algebra" / "tutorial-5-record.pdf",
)
add(
    THU / "线性代数" / "Lecture 4" / "tutorial_session_2_solutions.pdf",
    ROOT / "static" / "private" / "notes" / "linear-algebra" / "tutorial-2-solution.pdf",
)

# 高微：作业题面（《高等微积分1》第N次作业，公开）与自己写的解答（HomeworkN，加密）
AC = THU / "高等微积分" / "Homeworks"
CN_NUM = ["一", "二", "三", "四", "五", "六", "七"]
for n in range(1, 8):
    add(
        AC / f"《高等微积分1》第{CN_NUM[n - 1]}次作业.pdf",
        ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / f"homework-{n}.pdf",
    )
for n, src_name in (
    (1, "Homework1.pdf"),
    (2, "Homework2.pdf"),
    (3, "Homework3.pdf"),
    (4, "Homework4.pdf"),
    (5, "Homework5.pdf"),
    (6, "Homework6.pdf"),
    (7, "Homework7.pdf"),
):
    add(
        AC / src_name,
        ROOT / "static" / "private" / "notes" / "advanced-calculus-1" / f"homework-{n}-solution.pdf",
    )

# 高微：期中样卷与真题
add(
    THU / "高等微积分" / "样卷试题合集.pdf",
    ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / "sample-exams.pdf",
)
add(
    THU / "高等微积分" / "2025年秋季《高等微积分1》期中试题A卷.pdf",
    ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / "midterm-2025-a.pdf",
)

# 高微：七周笔记 + 全部课堂记录
for n in range(1, 9):
    add(
        THU / "高等微积分" / "Notes" / f"高等微积分1_第{n}周笔记.pdf",
        ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / f"note-week-{n}.pdf",
    )
for month, day in (
    (9, 16),
    (9, 18),
    (9, 20),
    (9, 23),
    (9, 30),
    (10, 9),
    (10, 14),
    (10, 16),
    (10, 21),
    (10, 23),
    (10, 28),
    (10, 30),
    (11, 4),
    (11, 6),
):
    add(
        THU / "高等微积分" / "Records" / f"2026年{month}月{day}日高微记录.pdf",
        ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / f"record-2026-{month}-{day}.pdf",
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
    THU / "高等微积分" / "习题课" / "高等微积分-第7周习题课.pdf",
    ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / "tutorial-week-7.pdf",
)
add(
    THU / "高等微积分" / "习题课" / "高等微积分-第8周习题课.pdf",
    ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / "tutorial-week-8.pdf",
)
add(
    THU / "高等微积分" / "习题课" / "2026年秋季《高等微积分1》第二次习题课材料参考解答.pdf",
    ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / "tutorial-2-solution.pdf",
)
add(
    THU / "高等微积分" / "习题课" / "2026年秋季《高等微积分1》第三次习题课材料.pdf",
    ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / "tutorial-3.pdf",
)
add(
    THU / "高等微积分" / "习题课" / "2026年秋季《高等微积分1》第三次习题课材料参考解答.pdf",
    ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / "tutorial-3-solution.pdf",
)
add(
    THU / "高等微积分" / "习题课" / "2026年秋季《高等微积分1》第四次习题课材料.pdf",
    ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / "tutorial-4.pdf",
)
add(
    THU / "高等微积分" / "习题课" / "2026年秋季《高等微积分1》第四次习题课材料参考解答.pdf",
    ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / "tutorial-4-solution.pdf",
)
add(
    THU / "高等微积分" / "习题课" / "2026年秋季《高等微积分1》第五次习题课材料.pdf",
    ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / "tutorial-5.pdf",
)
add(
    THU / "高等微积分" / "Notes" / "练习题集" / "高等微积分1_公式手册.pdf",
    ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / "formula-handbook.pdf",
)
add(
    THU / "高等微积分" / "高微期中复习.pdf",
    ROOT / "static" / "files" / "notes" / "advanced-calculus-1" / "midterm-review.pdf",
)

# 计入门：课件与作业
for week in (1, 2, 3, 5, 6, 7, 8):
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
    (7, "intro2cs-hw-6.pdf", "homework-6.pdf"),
    (8, "Intro_to_CS_HW_7.pdf", "homework-7.pdf"),
):
    add(CS / f"Week{week}" / src, ICS / dst)
# 官方答案（公开）
for week, src, dst in (
    (1, "Intro_to_CS_HW_1_Answer.pdf", "homework-1-answer.pdf"),
    (2, "Intro2CS_HW2_Answer.pdf", "homework-2-answer.pdf"),
    (3, "intro2cs-hw3-sol.pdf", "homework-3-answer.pdf"),
):
    add(CS / f"Week{week}" / src, ICS / dst)
# 自己写的解答（加密）
for week, src, dst in (
    (1, "Homework1.pdf", "homework-1-solution.pdf"),
    (2, "Homework_Intro2cs_2.pdf", "homework-2-solution.pdf"),
    (3, "Homework__Intro2cs_3.pdf", "homework-3-solution.pdf"),
    (5, "Homework_Intro2cs_4.pdf", "homework-4-solution.pdf"),
    (6, "Homework_Intro2cs_5.pdf", "homework-5-solution.pdf"),
    (7, "Homework_Intro2cs_6.pdf", "homework-6-solution.pdf"),
    (8, "Homework_Intro2cs_7.pdf", "homework-7-solution.pdf"),
):
    add(CS / f"Week{week}" / src, ICS_PRIVATE / dst)

# 计入门：习题课（TA 讲解材料）
for src, dst in (
    ("Week1/week01-office-hour/Intro to LaTeX.pdf", "tutorial-week-1.pdf"),
    ("Week2/week02-paper-reading.pdf", "tutorial-week-2.pdf"),
    ("Week3/week03-paper-reading.pdf", "tutorial-week-3.pdf"),
    ("Week6/week06-linux.pdf", "tutorial-week-6.pdf"),
    ("Week7/week07-LLM-programming.pdf", "tutorial-week-7.pdf"),
    ("Week8/week08-office-hour.pdf", "tutorial-week-8.pdf"),
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

# 算法设计：作业题面与解答（HomeworkN 目录）
for n in (5, 6):
    add(
        THU / "算法设计" / "Homework" / f"Homework{n}" / f"hw{n}.pdf",
        ROOT / "static" / "files" / "notes" / "algorithm-design" / f"homework-{n}.pdf",
    )
    add(
        THU / "算法设计" / "Homework" / f"Homework{n}" / f"Homework_Algorithm_Design_{n}.pdf",
        ROOT / "static" / "private" / "notes" / "algorithm-design" / f"homework-{n}-solution.pdf",
    )

# 算法设计：历年期中试题
for year in (2023, 2024, 2025):
    add(
        THU / "算法设计" / f"midterm{year}.pdf",
        ROOT / "static" / "files" / "notes" / "algorithm-design" / f"midterm-{year}.pdf",
    )
add(
    THU / "算法设计" / "midterm-review.pdf",
    ROOT / "static" / "files" / "notes" / "algorithm-design" / "midterm-review.pdf",
)
add(
    THU / "算法设计" / "算法设计_简明题面与答案.pdf",
    ROOT / "static" / "files" / "notes" / "algorithm-design" / "all-exercises.pdf",
)
add(
    THU / "算法设计" / "Midterm_Exam_Questions_English.pdf",
    ROOT / "static" / "files" / "notes" / "algorithm-design" / "midterm-2026.pdf",
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

# 目录扫描：最近几天改过、又不在上面的映射里的素材，说明是还没收录的新文件。
IGNORED_NAMES = {"算法设计_期中笔记_A4.pdf", "cs_2024_lhz.pdf"}
RECENT_DAYS = 3
_cutoff = time.time() - RECENT_DAYS * 86400
_known = {str(src) for src, _ in PAIRS}
unlisted: list[Path] = []
for _course in ("线性代数", "高等微积分", "算法设计", "计算机入门"):
    for _p in sorted((THU / _course).rglob("*")):
        if not _p.is_file() or _p.suffix.lower() not in {".pdf", ".pptx"}:
            continue
        if str(_p) in _known or _p.name in IGNORED_NAMES:
            continue
        if _p.stat().st_mtime >= _cutoff:
            unlisted.append(_p)


def md5(p: Path) -> str:
    h = hashlib.md5()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# 哈希缓存：文件大小与修改时间都没变时直接复用上次的摘要，避免整份重读。
CACHE_FILE = ROOT / "tools" / "data" / "check_cache.json"
STATUS_FILE = ROOT / "tools" / "data" / "last_check.json"


def load_cache() -> dict:
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


_cache = load_cache()
_used: dict[str, list] = {}


def md5_cached(p: Path) -> str:
    st = p.stat()
    key = str(p)
    hit = _cache.get(key)
    if hit and hit[0] == st.st_size and hit[1] == st.st_mtime_ns:
        _used[key] = hit
        return hit[2]
    digest = md5(p)
    _used[key] = [st.st_size, st.st_mtime_ns, digest]
    return digest


same, stale, missing_dst, missing_src, rasterized, rasterized_late = [], [], [], [], [], []

# 超过 20 MB 的素材由 shrink_pdf.py 栅格化后入库，体积与内容都变了，哈希必然不同，
# 这类只核对站内文件不旧于素材。
RASTERIZED_LIMIT = 20 * 1024 * 1024

for src, dst in PAIRS:
    if not src.exists():
        missing_src.append(src.name)
        continue
    if not dst.exists():
        missing_dst.append(dst)
        continue
    if src.stat().st_size > RASTERIZED_LIMIT:
        (rasterized if dst.stat().st_mtime >= src.stat().st_mtime else rasterized_late).append(
            (src, dst)
        )
        continue
    (same if md5_cached(src) == md5_cached(dst) else stale).append((src, dst))

QUIET = "--quiet" in sys.argv
_sink = io.StringIO() if QUIET else None
if _sink is not None:
    sys.stdout = _sink

print(f"一致 {len(same)} 份")
for src, dst in stale:
    print(f"  [待同步] {src.name} -> {dst.name}")
for src, dst in rasterized_late:
    print(f"  [可能过期] {src.name} -> {dst.name}（栅格化产物比素材旧）")
if rasterized:
    names = "、".join(src.name for src, _ in rasterized)
    print(f"  [栅格化] {len(rasterized)} 份，哈希不可比，站内不旧于素材：{names}")
for dst in missing_dst:
    print(f"  [站内缺失] {dst}")
for name in missing_src:
    print(f"  [素材缺失] {name}")
unlisted_text = [p.relative_to(THU).as_posix() for p in unlisted]
if unlisted_text:
    print(f"  [未收录] {len(unlisted_text)} 份新素材：" + "、".join(unlisted_text))

changed = [f"{src.name} -> {dst.name}" for src, dst in stale]
stale_raster = [f"{src.name} -> {dst.name}" for src, dst in rasterized_late]
pending = changed + stale_raster

CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
CACHE_FILE.write_text(json.dumps(_used, ensure_ascii=False), encoding="utf-8")
STATUS_FILE.write_text(
    json.dumps(
        {
            "time": datetime.now().isoformat(timespec="seconds"),
            "same": len(same),
            "changed": changed,
            "rasterized_stale": stale_raster,
            "missing_src": missing_src,
            "missing_dst": [str(d) for d in missing_dst],
            "unlisted": unlisted_text,
        },
        ensure_ascii=False,
        indent=1,
    ),
    encoding="utf-8",
)

if QUIET:
    sys.stdout = sys.__stdout__
    if pending or unlisted_text or missing_src or missing_dst:
        summary = "、".join(pending) if pending else ""
        if unlisted_text:
            summary += ("；" if summary else "") + "未收录 " + "、".join(unlisted_text)
        if missing_src:
            summary += ("；" if summary else "") + "素材缺失 " + "、".join(missing_src)
        if missing_dst:
            summary += ("；" if summary else "") + "站内缺失 " + str(len(missing_dst)) + " 份"
        print(f"有更新：{summary}")
        sys.exit(1)
    print("无更新")
    sys.exit(0)
