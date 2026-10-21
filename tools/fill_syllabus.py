"""从每讲笔记 PDF 首页提取「涉及内容」，写进 _syllabus.yaml。"""

from __future__ import annotations

import re
from pathlib import Path

import pymupdf
import yaml

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "content" / "notes"
THU = Path(r"C:\Users\Rain\Desktop\THU")

# 有 LaTeX 源时优先用源里的 \author，主题句自带 $...$，比 PDF 里被替换成 Unicode 符号更准
TEX_DIRS = {
    "advanced-calculus-1": THU / "2026 秋" / "高等微积分" / "Notes",
    "linear-algebra": THU / "2026 秋" / "线性代数" / "Notes",
}

SKIP = ("依据", "课堂记录", "本讲在", "两本教材", "参考书", "对应关系")
FORCE = True


CJK_PUNCT = "、，。；：！？）】」』…"


def join_paragraph(parts: list[tuple[str, float]]) -> str:
    """把 PDF 折行拼回一段。

    同一行宽内的折行（左端 x 相同）直接连写，避免把「矩阵」拆成「矩，阵」；
    另起一行的条目（左端 x 不同）之间补一个「，」。
    """
    out = parts[0][0].rstrip()
    prev_x = parts[0][1]
    for text, x0 in parts[1:]:
        nxt = text.strip()
        wrapped = abs(x0 - prev_x) <= 1.5
        if out.endswith("-") and nxt[:1].islower():
            out = out[:-1] + nxt
        elif out[-1:].isascii() and out[-1:].isalnum() and nxt[:1].isascii():
            out = out + " " + nxt
        elif not wrapped and not out.endswith(tuple(CJK_PUNCT)) and not nxt[:1].isascii():
            out = out + "，" + nxt
        else:
            out = out + nxt
        prev_x = x0
    return out


STOP_START = ("依据", "课堂记录", "本讲在", "两本教材", "参考书", "对应关系", "主题", "讲义", "课堂")


def page_lines(path: Path) -> list[tuple[str, float]]:
    """首页的逐行文字与左端坐标。"""
    doc = pymupdf.open(path)
    lines: list[tuple[str, float]] = []
    for block in doc[0].get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            text = "".join(span["text"] for span in line["spans"]).strip()
            if text:
                lines.append((text, line["bbox"][0]))
    doc.close()
    return lines


def topic_from_tex(subject: str, order: int) -> str:
    """从同名 .tex 的 \\author{...} 首行取主题句，保留 $...$。"""
    folder = TEX_DIRS.get(subject)
    if not folder or not folder.is_dir():
        return ""
    for tex in folder.glob("*.tex"):
        name = tex.name
        if not (
            re.search(rf"第\s*{order}\s*周", name)
            or re.search(rf"[Ll]ecture\s*{order}\b", name)
            or re.search(rf"[_-]0*{order}[_-]", name)
        ):
            continue
        text = tex.read_text(encoding="utf-8")
        m = re.search(r"\\author\{(.+?)\}", text, re.S)
        if not m:
            continue
        first = m.group(1).split("\\\\")[0]
        first = re.sub(r"\s+", " ", first).strip()
        if first:
            return first
    return ""


def topics_from_pdf(path: Path) -> str:
    lines = page_lines(path)

    # 优先找「本讲主题」那一段：PDF 会在栏宽处折行，需要把后续行接上，直到句号
    for idx, (text, x0) in enumerate(lines[:12]):
        if text.startswith("本讲主题"):
            first = re.sub(r"^本讲主题[.．:：]?\s*", "", text)
            parts = [(first, x0)]
            if "。" not in first:
                for nxt in lines[idx + 1 : idx + 6]:
                    parts.append(nxt)
                    if "。" in nxt[0]:
                        break
            return join_paragraph(parts).split("。")[0].strip()

    # 没有「本讲主题」标签时，主题往往直接写在页码下面，且跨若干行
    for idx in range(1, min(10, len(lines))):
        text, x0 = lines[idx]
        if any(k in text for k in SKIP) or "§" in text:
            continue
        if re.match(r"^第\d+\s*(讲|周)", text) or len(text) < 6:
            continue
        parts = [(text, x0)]
        for nxt_text, nxt_x in lines[idx + 1 : idx + 8]:
            if nxt_text.startswith(STOP_START) or "§" in nxt_text or re.match(r"^\d", nxt_text):
                break
            parts.append((nxt_text, nxt_x))
            if nxt_text.endswith(("。", "．", ".")):
                break
        return join_paragraph(parts).split("。")[0].strip()
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
            topic = topic_from_tex(folder.name, order) or topics_from_pdf(pdf)
            if topic:
                data[order] = topic
                changed = True
        if changed:
            lines = ["# 每周/每讲涉及的课程内容，键是周次或讲次；留空则不显示"]
            for n in sorted(data):
                # 单引号写 YAML，反斜杠才不会被当成转义（主题句里可能有 $\epsilon$）
                value = str(data[n] or "").replace("'", "''")
                lines.append(f"{n}: '{value}'")
            syl.write_text("\n".join(lines) + "\n", encoding="utf-8")
            print(folder.name, "更新", len(data), "行")


if __name__ == "__main__":
    main()
