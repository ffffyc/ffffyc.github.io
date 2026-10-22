"""同步高微习题课与公式手册，并更新算法设计第五次解答。

周次按文件日期判定：10-07 属第 4 周、10-15/10-18 属第 5 周、10-22 属第 6 周。
"""

from __future__ import annotations

import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
THU = Path(r"C:\Users\Rain\Desktop\THU\2026 秋")
AC_FILES = ROOT / "static" / "files" / "notes" / "advanced-calculus-1"
AC = ROOT / "content" / "notes" / "advanced-calculus-1"

# 1. 教材式材料按日期落周：第一次→4 周，第二次→5 周
for name, order in (("tutorial-1", 4), ("tutorial-1-solution", 4), ("tutorial-2", 5)):
    p = AC / f"{name}.md"
    if not p.exists():
        continue
    text = p.read_text(encoding="utf-8")
    lines = [f"order: {order}" if line.startswith("order:") else line for line in text.splitlines()]
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("调整周次", name, order)

# 2. 第 5、6 周习题课（助教课件）
JOBS = [
    ("高等微积分-第5周习题课.pdf", "tutorial-week-5.pdf", "tutorial-week-5.md", "第五周习题课", 5, 2),
    ("高等微积分-第6周习题课.pdf", "tutorial-week-6.pdf", "tutorial-week-6.md", "第六周习题课", 6, 1),
]
for src_name, pdf_name, md_name, title, order, seq in JOBS:
    src = THU / "高等微积分" / "习题课" / src_name
    if not src.exists():
        print("缺少", src)
        continue
    shutil.copy2(src, AC_FILES / pdf_name)
    body = (
        "---\n"
        f'title: "{title}"\n'
        "kind: tutorial\n"
        f"order: {order}\n"
        f"seq: {seq}\n"
        f"pdf: files/notes/advanced-calculus-1/{pdf_name}\n"
        "tags: []\n"
        "---\n"
    )
    (AC / md_name).write_text(body, encoding="utf-8")
    print("导入", md_name)

# 3. 公式手册挂到参考资料
handbook_src = THU / "高等微积分" / "Notes" / "练习题集" / "高等微积分1_公式手册.pdf"
if handbook_src.exists():
    shutil.copy2(handbook_src, AC_FILES / "formula-handbook.pdf")
    meta_path = AC / "_subject.yaml"
    meta = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
    resources = meta.get("resources") or []
    entry = {
        "title": "公式手册（展开、等价无穷小、三角恒等式、常用求和）",
        "file": "files/notes/advanced-calculus-1/formula-handbook.pdf",
    }
    if not any(r.get("file") == entry["file"] for r in resources):
        resources.append(entry)
    meta["resources"] = resources
    meta_path.write_text(yaml.safe_dump(meta, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print("加入公式手册")

# 4. 算法设计第五次作业解答有更新
ad_src = THU / "算法设计" / "Homework" / "Homework5" / "Homework_Algorithm_Design_5.pdf"
if ad_src.exists():
    shutil.copy2(ad_src, ROOT / "static" / "private" / "notes" / "algorithm-design" / "homework-5-solution.pdf")
    print("更新算法设计第五次解答")
