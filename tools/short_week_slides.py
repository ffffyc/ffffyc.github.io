"""高微周习题课的链接文字改成「课件」。"""

from pathlib import Path

AC = Path(__file__).resolve().parent.parent / "content" / "notes" / "advanced-calculus-1"

for name in ("tutorial-week-5.md", "tutorial-week-6.md"):
    p = AC / name
    if not p.exists():
        continue
    lines = p.read_text(encoding="utf-8").splitlines()
    if any(line.startswith("short:") for line in lines):
        lines = [f'short: "课件"' if line.startswith("short:") else line for line in lines]
    else:
        out = []
        for line in lines:
            out.append(line)
            if line.strip() == "kind: tutorial":
                out.append('short: "课件"')
        lines = out
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("更新", name)
