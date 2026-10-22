"""习题课按「上课那一周」落位：第 N 次习题课在第 4+N 周（材料提前一周发布）。

第一次 → 第 5 周，第二次 → 第 6 周；同周先列材料，再列当天习题课课件。
"""

from pathlib import Path

AC = Path(__file__).resolve().parent.parent / "content" / "notes" / "advanced-calculus-1"

PLAN = {
    "tutorial-1.md": (5, 1),
    "tutorial-1-solution.md": (5, 2),
    "tutorial-week-5.md": (5, 3),
    "tutorial-2.md": (6, 1),
    "tutorial-week-6.md": (6, 2),
}

for name, (order, seq) in PLAN.items():
    p = AC / name
    if not p.exists():
        print("缺少", name)
        continue
    lines = p.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines:
        if line.startswith("order:"):
            out.append(f"order: {order}")
        elif line.startswith("seq:"):
            out.append(f"seq: {seq}")
        else:
            out.append(line)
            if line.startswith("kind:") and not any(l.startswith("seq:") for l in lines):
                out.append(f"seq: {seq}")
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("设置", name, "order", order, "seq", seq)
