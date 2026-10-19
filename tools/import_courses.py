"""把 THU 课程目录里的作业题面、笔记、课堂记录、习题课导入站点。

作业解答与习题课解答标记为隐藏；教材、讲义幻灯片等由 copy_resources.py 单独处理。
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THU = Path(r"C:\Users\Rain\Desktop\THU")
FILES = ROOT / "static" / "files" / "notes"
OUT = ROOT / "content" / "notes"

CN = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8}
NUM = "零一二三四五六七八九十"


def cn(n: int) -> str:
    if n <= 10:
        return NUM[n]
    if n < 20:
        return "十" + NUM[n - 10]
    return str(n)


# (正则, 类别, slug 模板, 是否隐藏)
RULES: dict[str, dict] = {
    "linear-algebra": {
        "root": "2026 秋",
        "dir": "线性代数",
        "rules": [
            (r"Notes/Lecture(\d+)_notes_zh\.pdf", "note", "note-lecture-{n}-cn", False),
            (r"Notes/Lecture(\d+)_notes_en\.pdf", "note", "note-lecture-{n}-en", False),
            (r"Lecture \d+/Homework(\d+)\.pdf", "homework", "homework-{n}", False),
            (r"Lecture \d+/Homework_+Linear_Algebra_(\d+)\.pdf", "homework", "homework-{n}", False),
            (r"Lecture \d+/Linear_Algebra_Homework(\d+)\.pdf", "homework", "homework-{n}-solution", True),
        ],
    },
    "advanced-calculus-1": {
        "root": "2026 秋",
        "dir": "高等微积分",
        "rules": [
            (r"Notes/高等微积分1_第(\d+)周笔记\.pdf", "note", "note-week-{n}", False),
            (r"Records/(\d{4})年(\d{1,2})月(\d{1,2})日高微记录\.pdf", "record", "record-{y}-{m}-{d}", False),
            (r"Homeworks/《高等微积分1》第(.)次作业\.pdf", "homework", "homework-{n}", False),
            (r"Homeworks/Homework(\d+)\.pdf", "homework", "homework-{n}-solution", True),
            (r"习题课/2026年秋季《高等微积分1》第(.)次习题课材料\.pdf", "tutorial", "tutorial-{n}", False),
            (r"习题课/2026年秋季《高等微积分1》第(.)次习题课材料参考解答\.pdf", "tutorial", "tutorial-{n}-solution", True),
            (r"习题课/第(.)次习题课材料_解答\.pdf", "tutorial", "tutorial-{n}-solution", True),
        ],
    },
    "algorithm-design": {
        "root": "2026 秋",
        "dir": "算法设计",
        "rules": [
            (r"Homework/Homework(\d+)/Homework(\d+)\.pdf", "homework", "homework-{n}", False),
            (r"Homework/Homework(\d+)/Homework__Algorithm_Design_(\d+)\.pdf", "homework", "homework-{n}", False),
            (r"Homework/Homework(\d+)/hw(\d+)\.pdf", "homework", "homework-{n}-solution", True),
        ],
    },
    "introduction-to-cs": {
        "root": "2026 秋",
        "dir": "计算机入门",
        "rules": [
            (r"Week(\d+)/Homework_+Intro2cs_(\d+)\.pdf", "homework", "homework-{n}", False),
            (r"Week(\d+)/Homework(\d+)\.pdf", "homework", "homework-{n}", False),
            (r"Week(\d+)/Intro2CS_HW(\d+)\.pdf", "homework", "homework-{n}", False),
            (r"Week(\d+)/intro2cs-hw-(\d+)(?:-v\d+)?\.pdf", "homework", "homework-{n}-solution", True),
        ],
    },
    "sys-intro": {
        "root": "2026 春",
        "dir": "计算机系统概论",
        "rules": [
            (r"Homework/Homework(\d+)/HW.*\.pdf", "homework", "homework-{n}", False, "first"),
            (r"Homework/Homework(\d+)/Homework\d+_.*\.pdf", "homework", "homework-{n}-solution", True),
            (r"Lecture notes/[^/]*?(?:lec|lecture)_?(\d+)[^/]*\.pdf", "note", "note-lec-{n}", False),
            (r"lec(\d+)-[^/]*\.(?:pdf|pptx)", "slide", "slide-{n}", False),
        ],
    },
    "math4csai": {
        "root": "2026 春",
        "dir": "计算机与人工智能应用数学",
        "rules": [
            (r"Homework/Homework(\d+)/Homework(\d+)\.pdf", "homework", "homework-{n}", False),
            (r"Homework/Homework(\d+)/hw(\d+)\.pdf", "homework", "homework-{n}-solution", True),
        ],
    },
    "theory-of-computation": {
        "root": "2026 春",
        "dir": "计算理论",
        "rules": [
            (r"Homework/Homework(\d+)/problem-set-(\d+)\.pdf", "homework", "homework-{n}", False),
            (r"Homework/Homework(\d+)/Homework(\d+)\.pdf", "homework", "homework-{n}-solution", True),
            (r"2026_Lecture_(\d+)\.pdf", "slide", "slide-{n}", False),
        ],
    },
}


def yaml_str(value: str) -> str:
    return '"' + value.replace('"', '\\"') + '"'


def title_for(kind: str, n: int, hidden: bool, name: str, groups: list) -> str:
    if kind == "note":
        if "_zh" in name:
            return f"第{cn(n)}讲笔记-CN"
        if "_en" in name:
            return f"第{cn(n)}讲笔记-EN"
        if "note-week" in name or "周笔记" in name:
            return f"第{cn(n)}周笔记"
        return f"第{cn(n)}讲笔记"
    if kind == "slide":
        return f"第{cn(n)}讲课件"
    if kind == "homework":
        return f"第{cn(n)}次作业" + ("解答" if hidden else "")
    if kind == "tutorial":
        return f"第{cn(n)}次习题课" + ("解答" if hidden else "材料")
    y, m, d = groups[0], groups[1], groups[2]
    return f"{int(m)} 月 {int(d)} 日课堂记录"


def main() -> None:
    total = 0
    for slug, conf in RULES.items():
        src_dir = THU / conf["root"] / conf["dir"]
        out_dir = OUT / slug
        if not src_dir.exists():
            print("跳过（目录不存在）", src_dir)
            continue
        out_dir.mkdir(parents=True, exist_ok=True)
        dest_dir = FILES / slug
        dest_dir.mkdir(parents=True, exist_ok=True)

        for old in out_dir.glob("*.md"):
            old.unlink()
        for old in dest_dir.glob("*.pdf"):
            old.unlink()
        private_dir = ROOT / "static" / "private" / "notes" / slug
        if private_dir.exists():
            for old in private_dir.glob("*.pdf"):
                old.unlink()

        for path in sorted(src_dir.rglob("*")):
            if path.suffix.lower() not in (".pdf", ".pptx"):
                continue
            rel = path.relative_to(src_dir).as_posix()
            for rule in conf["rules"]:
                pattern, kind, slug_tpl, hidden = rule[:4]
                pos = rule[4] if len(rule) > 4 else "last"
                m = re.fullmatch(pattern, rel)
                if not m:
                    continue
                nums = []
                for g in m.groups():
                    g2 = CN.get(g, g)
                    if str(g2).isdigit():
                        nums.append(int(g2))
                if not nums or kind == "record":
                    n = 0
                else:
                    n = nums[0] if pos == "first" else nums[-1]
                year, month, day = (list(m.groups()) + ["0", "0", "0"])[:3] if kind == "record" else ("0", "0", "0")

                title = title_for(kind, n, hidden, path.name, [year, month, day])
                name = slug_tpl.format(
                    n=n,
                    y=int(year) if str(year).isdigit() else 0,
                    m=int(month) if str(month).isdigit() else 0,
                    d=int(day) if str(day).isdigit() else 0,
                )

                ext = path.suffix.lower()
                file_stem = name if kind != "slide" else path.stem
                if hidden:
                    target = ROOT / "static" / "private" / "notes" / slug / f"{file_stem}{ext}"
                    target.parent.mkdir(parents=True, exist_ok=True)
                    pdf_field = f"private/notes/{slug}/{file_stem}{ext}"
                else:
                    target = dest_dir / f"{file_stem}{ext}"
                    pdf_field = f"files/notes/{slug}/{file_stem}{ext}"
                if not target.exists():
                    shutil.copy2(path, target)

                # 习题课从第五周开始：第一次习题课 = 第 5 周；课堂记录按日期由生成器推算周次
                if kind == "record":
                    order = 0
                elif kind == "tutorial":
                    order = 4 + n
                else:
                    order = n

                lines = ["---", f"title: {yaml_str(title)}"]
                if kind == "record":
                    lines.append(f"date: {int(year):04d}-{int(month):02d}-{int(day):02d}")
                lines += [
                    f"kind: {kind}",
                    f"order: {order}",
                    f"pdf: {pdf_field}",
                ]
                if hidden:
                    lines.append("hidden: true")
                lines += ["tags: []", "---", "", ""]
                (out_dir / f"{name}.md").write_text("\n".join(lines), encoding="utf-8")
                total += 1
                break

    print("导入条目", total)


if __name__ == "__main__":
    main()
