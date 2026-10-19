"""从每讲笔记 PDF 首页提取「涉及内容」，写进 _syllabus.yaml。"""

from __future__ import annotations

import re
from pathlib import Path

import pymupdf
import yaml

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "content" / "notes"

SKIP = ("依据", "课堂记录", "本讲在", "两本教材", "参考书", "对应关系")
FORCE = True


def join_paragraph(parts: list[str]) -> str:
    """PDF 折行后重新拼成一段：西文补空格，行末连字符去掉。"""
    out = parts[0].rstrip()
    for nxt in parts[1:]:
        nxt = nxt.strip()
        if out.endswith("-") and nxt[:1].islower():
            out = out[:-1] + nxt
        elif out[-1:].isascii() and out[-1:].isalnum() and nxt[:1].isascii():
            out = out + " " + nxt
        else:
            out = out + nxt
    return out


def topics_from_pdf(path: Path) -> str:
    doc = pymupdf.open(path)
    text = doc[0].get_text()
    doc.close()
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    # 优先找「本讲主题」那一段：PDF 会在栏宽处折行，需要把后续行接上，直到句号
    for idx, ln in enumerate(lines[:12]):
        if ln.startswith("本讲主题"):
            parts = [re.sub(r"^本讲主题[.．:：]?\s*", "", ln)]
            if "。" not in parts[0]:
                for nxt in lines[idx + 1 : idx + 6]:
                    parts.append(nxt)
                    if "。" in nxt:
                        break
            return join_paragraph(parts).split("。")[0].strip()

    for ln in lines[1:8]:
        if any(k in ln for k in SKIP) or "§" in ln:
            continue
        if re.match(r"^第\d+\s*(讲|周)", ln) or len(ln) < 6:
            continue
        return ln[:110]
    return ""


def main() -> None:
    for folder in sorted(NOTES.iterdir()):
        if not folder.is_dir():
            continue
        syl = folder / "_syllabus.yaml"
        data = {}
        if syl.exists():
            data = yaml.safe_load(syl.read_text(encoding="utf-8")) or {}
        changed = False
        for md in sorted(folder.glob("note-*.md")):
            text = md.read_text(encoding="utf-8")
            meta = yaml.safe_load(text.split("---")[1])
            if meta.get("kind") != "note":
                continue
            if md.stem.endswith("-en") or "_en" in md.stem:
                continue
            pdf = ROOT / "static" / meta["pdf"]
            if not pdf.exists():
                continue
            order = int(meta.get("order") or 0)
            current = str(data.get(order) or "")
            if not FORCE and current and "§" not in current and "《" not in current:
                continue
            topic = topics_from_pdf(pdf)
            if topic:
                data[order] = topic
                changed = True
        if changed:
            lines = ["# 每周/每讲涉及的课程内容，键是周次或讲次；留空则不显示"]
            for n in sorted(data):
                value = str(data[n] or "").replace('"', '\\"')
                lines.append(f'{n}: "{value}"')
            syl.write_text("\n".join(lines) + "\n", encoding="utf-8")
            print(folder.name, "更新", len(data), "行")


if __name__ == "__main__":
    main()
