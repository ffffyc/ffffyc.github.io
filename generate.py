#!/usr/bin/env python
"""把 content/ 下的 Markdown 生成为静态站点，输出到 docs/。

用法：python generate.py
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import shutil
from datetime import date, datetime
from pathlib import Path

import yaml
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from urllib.parse import quote
from jinja2 import Environment, FileSystemLoader
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
OUT = ROOT / "docs"

FRONT_MATTER = re.compile(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n", re.S)

CATEGORY_KEYS = {
    "题解": "solutions",
    "算法·理论": "theory",
    "游记": "travel",
    "解题思路": "ideas",
    "杂项": "misc",
    "工具": "tools",
    "个人记录": "diary",
    "文化课": "coursework",
}
PAGE_SIZE = 20

COLUMN_LABEL = {
    "record": "课堂记录",
    "note": "笔记",
    "homework": "作业",
    "solution": "解答",
    "tutorial": "习题课",
    "tutorial_solution": "解答",
    "slide": "课件",
    "lectures": "对应讲次",
    "other": "其他",
}


def load_config() -> dict:
    with (ROOT / "config.yaml").open(encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    cfg.setdefault("title", "Blog")
    cfg.setdefault("tagline", "")
    cfg.setdefault("description", "")
    cfg.setdefault("footer", "")
    cfg.setdefault("base", "/")
    if not cfg["base"].endswith("/"):
        cfg["base"] += "/"
    cfg.setdefault(
        "kinds",
        {"note": "笔记", "homework": "作业", "record": "课堂记录", "other": "其他"},
    )
    return cfg


def read_doc(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    m = FRONT_MATTER.match(text)
    if not m:
        return {}, text
    meta = yaml.safe_load(m.group(1)) or {}
    return meta, text[m.end():]


MATH_RE = re.compile(r"\$\$.+?\$\$|\$(?:[^$\\]|\\.)+?\$", re.S)
CONTAINER_OPEN = re.compile(r"^:::(\w+)(?:\[(.*?)\])?(?:\{([^}]*)\})?\s*$")
SLOT = '<div class="fold-slot" data-i="%d"></div>'
HEAD_RE = re.compile(r"<h([1-6])>(.*?)</h\1>", re.S)


def build_toc(html: str) -> tuple[str, list[dict]]:
    """给一至六级标题加锚点，并生成侧栏目录。

    不动原文的标题等级；目录的缩进按「相对本篇最浅一级」计算，跳级也不会错位。
    """
    toc: list[dict] = []

    def rep(m: re.Match) -> str:
        level = int(m.group(1))
        inner = m.group(2)
        text = re.sub(r"<[^>]+>", "", inner).strip()
        if not text:
            return m.group(0)
        anchor = f"s{len(toc) + 1}"
        toc.append({"level": level, "text": text, "id": anchor})
        mark = f'<a class="anchor" href="#{anchor}" aria-label="本节链接">#</a>'
        return f'<h{level} id="{anchor}">{inner}{mark}</h{level}>'

    html = HEAD_RE.sub(rep, html)
    if toc:
        # 按大纲栈算缩进：只比父级深一层，跳过空层不会再叠加缩进
        stack: list[int] = []
        for t in toc:
            while stack and stack[-1] >= t["level"]:
                stack.pop()
            t["depth"] = min(3, len(stack))
            t["top"] = t["depth"] == 0
            stack.append(t["level"])
    return html, toc


def make_fold(md: MarkdownIt, kind: str, title: str, flags: str, buf: list[str], state: list[str]) -> str:
    """生成折叠块；`{open}` 表示默认展开。"""
    inner = render_md(md, "\n".join(buf), state).strip()
    open_attr = " open" if "open" in flags.replace(" ", "").split(",") else ""
    return (
        f'<details class="fold fold-{kind}"{open_attr}><summary>{title or "展开"}</summary>'
        f'<div class="fold-body">{inner}</div></details>'
    )


def expand_containers(md: MarkdownIt, text: str, state: list[str]) -> str:
    """把 :::info[标题]{open} … ::: 转成折叠块，支持嵌套与默认展开。"""
    if ":::" not in text:
        return text
    out: list[str] = []
    stack: list[tuple[str, str, str, list[str]]] = []

    for line in text.split("\n"):
        open_m = CONTAINER_OPEN.match(line.strip())
        if open_m:
            stack.append(
                (
                    open_m.group(1) or "info",
                    open_m.group(2) or "",
                    open_m.group(3) or "",
                    [],
                )
            )
            continue
        if line.strip() == ":::" and stack:
            kind, title, flags, buf = stack.pop()
            state.append(make_fold(md, kind, title, flags, buf, state))
            target = stack[-1][3] if stack else out
            target.extend(["", SLOT % (len(state) - 1), ""])
            continue
        (stack[-1][3] if stack else out).append(line)

    # 原文偶尔少一个结尾标记，这里从内向外补上
    while stack:
        kind, title, flags, buf = stack.pop()
        state.append(make_fold(md, kind, title, flags, buf, state))
        target = stack[-1][3] if stack else out
        target.extend(["", SLOT % (len(state) - 1), ""])
    return "\n".join(out)


def render_md(md: MarkdownIt, text: str, boxes: list[str] | None = None) -> str:
    """先把公式整段替换成占位符，避免 Markdown 把 * 与 _ 当成强调符号。"""
    top = boxes is None
    if boxes is None:
        boxes = []
    store: list[str] = []

    def keep(m: re.Match) -> str:
        store.append(m.group(0))
        return f"@@MATH{len(store) - 1}@@"

    text = expand_containers(md, text, boxes)

    protected = MATH_RE.sub(keep, text)
    html = md.render(protected)
    for i, piece in enumerate(store):
        safe = piece.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        html = html.replace(f"@@MATH{i}@@", safe)

    if top:
        for _ in range(10):
            changed = False
            for i, box in enumerate(boxes):
                token = SLOT % i
                if token in html:
                    html = html.replace(token, box)
                    changed = True
            if not changed:
                break
    return html


def make_markdown() -> MarkdownIt:
    md = MarkdownIt("commonmark", {"html": True})
    md.enable(["table", "strikethrough"])

    def fence(tokens, idx, options, env):
        token = tokens[idx]
        info = (token.info or "").strip().split()
        lang = info[0] if info else ""
        try:
            lexer = get_lexer_by_name(lang) if lang else TextLexer()
        except Exception:
            lexer = TextLexer()
        body = highlight(token.content, lexer, HtmlFormatter(nowrap=True))
        cls = f' class="language-{lang}"' if lang else ""
        return f'<pre class="code"><code{cls}>{body}</code></pre>\n'

    md.renderer.rules["fence"] = fence
    return md


def as_date(value) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return date.min


def date_text(value) -> str:
    return "" if value is None else as_date(value).strftime("%Y-%m-%d")


def collect_posts(md: MarkdownIt, base: str) -> list[dict]:
    posts = []
    folder = CONTENT / "blog"
    if not folder.exists():
        return posts
    for path in sorted(folder.glob("*.md")):
        meta, body = read_doc(path)
        slug = path.stem
        posts.append(
            {
                "slug": slug,
                "title": meta.get("title", slug),
                "date": as_date(meta.get("date")),
                "date_text": date_text(meta.get("date")),
                "tags": meta.get("tags") or [],
                "summary": meta.get("summary", ""),
                "math": bool(meta.get("math", False)),
                "html": render_md(md, body),
                "url": f"{base}blog/{slug}/",
                "kind": "blog",
            }
        )
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def collect_past(md: MarkdownIt, base: str) -> list[dict]:
    """洛谷旧文。隐藏的文章不进入公开输出。"""
    posts = []
    folder = CONTENT / "past"
    if not folder.exists():
        return posts
    for path in sorted(folder.glob("*.md")):
        meta, body = read_doc(path)
        slug = str(meta.get("slug") or path.stem)
        category = meta.get("category", "题解")
        posts.append(
            {
                "slug": slug,
                "title": meta.get("title", slug),
                "date": as_date(meta.get("date")),
                "date_text": date_text(meta.get("date")),
                "category": category,
                "category_key": CATEGORY_KEYS.get(category, "other"),
                "tags": meta.get("tags") or [],
                "summary": meta.get("summary", ""),
                "math": bool(meta.get("math", False)),
                "hidden": bool(meta.get("hidden", False)),
                "top": int(meta.get("top") or 0),
                "source": meta.get("source", ""),
                "html": render_md(md, body),
                "url": f"{base}{'hidden' if meta.get('hidden') else 'past'}/{slug}/",
                "kind": "past",
            }
        )
    posts.sort(key=lambda p: (-p["top"], -p["date"].toordinal()))
    return posts


def paginate(items: list[dict], size: int = PAGE_SIZE) -> list[list[dict]]:
    return [items[i:i + size] for i in range(0, len(items), size)] or [[]]


def past_page_url(base: str, category_key: str | None, page: int) -> str:
    stem = (
        f"{base}past/category/{category_key}/" if category_key else f"{base}past/"
    )
    return stem if page == 1 else f"{stem}page/{page}/"


def build_pager(base: str, category_key: str | None, page: int, total: int) -> dict:
    return {
        "n": page,
        "total": total,
        "pages": [
            {
                "n": i,
                "href": past_page_url(base, category_key, i),
                "current": i == page,
            }
            for i in range(1, total + 1)
        ],
        "prev": past_page_url(base, category_key, page - 1) if page > 1 else "",
        "next": past_page_url(base, category_key, page + 1) if page < total else "",
    }


def _size_text(pdf: str | None) -> str:
    if not pdf:
        return ""
    path = STATIC / pdf
    if not path.exists():
        return ""
    size = path.stat().st_size
    if size > 1048576:
        return f"{size / 1048576:.1f} MB"
    return f"{size / 1024:.0f} KB"


def _office_src(pdf: str | None, cfg: dict) -> str:
    """PPTX 交给微软 Office 网页查看器渲染，需要公网可访问的绝对地址。"""
    if not pdf or pdf.lower().endswith(".pdf"):
        return ""
    url = str(cfg.get("url") or "").rstrip("/")
    if not url.startswith("http"):
        return ""
    target = f"{url}/{pdf.lstrip('/')}"
    return f"https://view.officeapps.live.com/op/embed.aspx?src={quote(target, safe='')}"


def collect_subjects(md: MarkdownIt, cfg: dict) -> list[dict]:
    subjects = []
    root = CONTENT / "notes"
    if not root.exists():
        return subjects
    for folder in sorted(p for p in root.iterdir() if p.is_dir()):
        meta_path = folder / "_subject.yaml"
        meta = {}
        if meta_path.exists():
            meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
        items = []
        for path in sorted(folder.glob("*.md")):
            imeta, ibody = read_doc(path)
            kind = imeta.get("kind", "note")
            pdf = imeta.get("pdf")
            body_html = render_md(md, ibody).strip()
            slug = path.stem
            hidden = bool(imeta.get("hidden", False))
            if body_html or (pdf and not hidden):
                href = f"{cfg['base']}notes/{folder.name}/{slug}/"
            else:
                href = ""
            items.append(
                {
                    "slug": slug,
                    "title": imeta.get("title", slug),
                    "date": as_date(imeta.get("date")),
                    "date_text": date_text(imeta.get("date")),
                    "kind": kind,
                    "order": int(imeta.get("order") or 0),
                    "seq": int(imeta.get("seq") or 0),
                    "short": imeta.get("short")
                    or (
                        imeta.get("title", slug).replace("课堂记录", "").strip()
                        if kind == "record"
                        else imeta.get("title", slug)
                    ),
                    "kind_label": cfg["kinds"].get(kind, cfg["kinds"].get("other", "其他")),
                    "pdf": pdf,
                    "pdf_href": (cfg["base"] + pdf) if pdf else "",
                    "file_name": Path(pdf).name if pdf else "",
                    "size_text": _size_text(pdf),
                    "office_src": _office_src(pdf, cfg),
                    "tags": imeta.get("tags") or [],
                    "math": bool(imeta.get("math", False)),
                    "html": body_html,
                    "href": href,
                    "hidden": hidden,
                    "has_page": bool(body_html),
                    "url": f"{cfg['base']}notes/{folder.name}/{slug}/",
                }
            )
        items.sort(key=lambda i: (i["order"], i["seq"], -i["date"].toordinal()))
        public = [i for i in items if not i["hidden"]]
        secret = [i for i in items if i["hidden"]]

        records = [i for i in items if i["kind"] == "record" and i["date"] != date.min]
        if records:
            first = min(i["date"] for i in records)
            for i in records:
                if not i["order"]:
                    i["order"] = 1 + (i["date"] - first).days // 7

        syllabus_path = folder / "_syllabus.yaml"
        syllabus = {}
        if syllabus_path.exists():
            syllabus = yaml.safe_load(syllabus_path.read_text(encoding="utf-8")) or {}

        lecture_keys = meta.get("lecture_columns") or []
        main_items = (
            [i for i in items if i["kind"] not in ("slide", "note")]
            if lecture_keys
            else items
        )
        lecture_items = (
            [i for i in items if i["kind"] in ("slide", "note")] if lecture_keys else []
        )

        numbers = sorted({i["order"] for i in main_items if i["order"]})
        rows = []
        for n in numbers:
            cells = {}
            for i in main_items:
                if i["order"] != n:
                    continue
                if i["slug"].endswith("-solution"):
                    key = "tutorial_solution" if i["kind"] == "tutorial" else "solution"
                else:
                    key = i["kind"]
                cells.setdefault(key, []).append(i)
            for key, group in cells.items():
                if key == "record":
                    group.sort(key=lambda e: e["date"])
            rows.append(
                {
                    "n": n,
                    "text": str(syllabus.get(n, "") or ""),
                    "cells": cells,
                    "lect": str((meta.get("homework_lectures") or {}).get(n, "") or ""),
                }
            )

        # 解答、答案默认并进「作业 / 习题课」格：作业 · 解答 · 答案
        inline_solutions = meta.get("inline_solutions", True)
        if inline_solutions:
            for r in rows:
                for extra_key, base_key, label in (
                    ("solution", "homework", "解答"),
                    ("tutorial_solution", "tutorial", "解答"),
                    ("answer", "homework", "答案"),
                ):
                    group = r["cells"].pop(extra_key, None)
                    if not group:
                        continue
                    if base_key not in r["cells"]:
                        r["cells"][base_key] = []
                    for e in group:
                        item = dict(e)
                        item["short"] = label
                        r["cells"][base_key].append(item)

        drop = ("solution", "tutorial_solution", "answer")
        column_keys = [
            k
            for k in (meta.get("columns") or [])
            if not (inline_solutions and k in drop)
        ]
        if not column_keys:
            present = {k for r in rows for k in r["cells"]}
            column_keys = [k for k in cfg["kinds"] if k in present]
        columns = [
            {"key": k, "label": COLUMN_LABEL.get(k, cfg["kinds"].get(k, k))}
            for k in column_keys
        ]
        if column_keys:
            rows = [
                r
                for r in rows
                if any(k in r["cells"] for k in column_keys) or r.get("lect")
            ]
        used = {
            e["slug"]
            for r in rows
            for k, group in r["cells"].items()
            if k in column_keys
            for e in group
        }

        lecture_rows = []
        if lecture_keys:
            for n in sorted({i["order"] for i in lecture_items if i["order"]}):
                cells = {}
                for i in lecture_items:
                    if i["order"] == n:
                        cells.setdefault(i["kind"], []).append(i)
                        used.add(i["slug"])
                lecture_rows.append({"n": n, "cells": cells})

        # 作业表与讲次表合并：行 = 讲次，作业挂在它覆盖的第一讲上
        merge = bool(meta.get("merge_tables", False))
        merged_rows: list[dict] = []
        merged_columns: list[dict] = []
        if merge and lecture_keys:
            hw_ranges = meta.get("homework_lectures") or {}

            def start_of(n: int) -> int:
                text = str(hw_ranges.get(n, "") or "")
                digits = re.findall(r"\d+", text)
                return int(digits[0]) if digits else n

            by_n: dict[int, dict] = {}
            for r in lecture_rows:
                by_n[r["n"]] = {
                    "n": r["n"],
                    "cells": dict(r["cells"]),
                    "hw": [],
                    "span": {},
                    "skip": set(),
                }
            for r in rows:
                start = start_of(r["n"])
                target = by_n.setdefault(
                    start, {"n": start, "cells": {}, "hw": [], "span": {}, "skip": set()}
                )
                for key, group in r["cells"].items():
                    target["cells"].setdefault(key, []).extend(group)
                target["hw"].append(r["n"])

                # 作业覆盖若干讲：起始行用 rowspan 合并，跨过的行不再画这个格子
                digits = re.findall(r"\d+", str(hw_ranges.get(r["n"], "") or ""))
                end = int(digits[-1]) if len(digits) > 1 else start
                if end > start:
                    target["span"]["homework"] = end - start + 1
                    for n in range(start + 1, end + 1):
                        row = by_n.setdefault(
                            n, {"n": n, "cells": {}, "hw": [], "span": {}, "skip": set()}
                        )
                        row["skip"].add("homework")
            for n, r in by_n.items():
                r["text"] = str(syllabus.get(n, "") or "")
            merged_rows = [by_n[n] for n in sorted(by_n)]
            seen = set()
            merged_columns = []
            for c in lecture_keys + [
                c["key"] for c in columns if c["key"] != "lectures"
            ]:
                if c in seen:
                    continue
                seen.add(c)
                merged_columns.append(
                    {"key": c, "label": COLUMN_LABEL.get(c, cfg["kinds"].get(c, c))}
                )

        loose = [e for e in public if e["slug"] not in used]

        groups = []
        for key, label in cfg["kinds"].items():
            bucket = [i for i in public if i["kind"] == key]
            if bucket:
                groups.append((label, bucket))
        subjects.append(
            {
                "slug": folder.name,
                "name": meta.get("name", folder.name),
                "name_en": meta.get("name_en", ""),
                "term": meta.get("term", ""),
                "description": meta.get("description", ""),
                "order": meta.get("order", 999),
                "entries": public,
                "hidden_entries": secret,
                "groups": groups,
                "rows": rows,
                "loose": loose,
                "columns": columns,
                "lecture_rows": lecture_rows,
                "merge": merge,
                "merged_rows": merged_rows,
                "merged_columns": merged_columns,
                "lecture_columns": [
                    {"key": k, "label": COLUMN_LABEL.get(k, cfg["kinds"].get(k, k))}
                    for k in lecture_keys
                ],
                "lecture_unit": meta.get("lecture_unit", "讲"),
                "unit": meta.get("unit", "周"),
                "show_text": bool(meta.get("show_text", True)),
                "resources": meta.get("resources") or [],
                "links": meta.get("links") or [],
                "links_title": meta.get("links_title", "实验与代码"),
                "count": len(public),
                "hidden_count": len(secret),
            }
        )
    subjects.sort(key=lambda s: (s["order"], s["slug"]))
    return subjects


def load_secret() -> tuple[str, bytes] | None:
    """secret.key 第一行是口令，第二行是十六进制盐值。"""
    path = ROOT / "secret.key"
    if not path.exists():
        return None
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if len(lines) < 2:
        return None
    return lines[0], bytes.fromhex(lines[1])


def seal(obj: dict, password: str, salt: bytes, iterations: int = 150_000) -> str:
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations, 32)
    nonce = os.urandom(12)
    data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    cipher = AESGCM(key).encrypt(nonce, data, None)
    enc = lambda b: base64.b64encode(b).decode("ascii")  # noqa: E731
    return json.dumps(
        {"v": 1, "i": iterations, "s": enc(salt), "n": enc(nonce), "c": enc(cipher)},
        ensure_ascii=False,
    )


def seal_bytes(data: bytes, password: str, salt: bytes, iterations: int = 150_000) -> str:
    """把二进制文件加密成「nonce 一行 + 密文一行」的文本。"""
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations, 32)
    nonce = os.urandom(12)
    cipher = AESGCM(key).encrypt(nonce, data, None)
    return (
        base64.b64encode(nonce).decode("ascii")
        + "\n"
        + base64.b64encode(cipher).decode("ascii")
    )


def write(rel: str, html: str) -> None:
    target = OUT / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")


def main() -> None:
    cfg = load_config()
    site = {
        "title": cfg["title"],
        "tagline": cfg["tagline"],
        "description": cfg["description"],
        "footer": cfg["footer"],
    }
    base = cfg["base"]
    site["v"] = str(int(datetime.now().timestamp()))

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    md = make_markdown()
    secret = load_secret()
    pending_enc: list[tuple[str, str]] = []
    posts = collect_posts(md, base)
    past_all = collect_past(md, base)
    past = [p for p in past_all if not p["hidden"]]
    hidden_count = len(past_all) - len(past)
    subjects = collect_subjects(md, cfg)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    def render(name: str, rel: str, **ctx) -> None:
        tpl = env.get_template(name)
        write(rel, tpl.render(site=site, base=base, **ctx))

    years: list[tuple[int, list[dict]]] = []
    for post in posts:
        year = post["date"].year if post["date"] != date.min else 0
        if years and years[-1][0] == year:
            years[-1][1].append(post)
        else:
            years.append((year, [post]))

    recent = sorted(posts + past, key=lambda p: p["date"], reverse=True)[:6]
    current_term = cfg.get("current_term", "")
    home_subjects = [s for s in subjects if not current_term or s["term"] == current_term]
    render(
        "home.html",
        "index.html",
        section="home",
        posts=recent,
        subjects=home_subjects,
        past_total=len(past),
    )

    hidden = [p for p in past_all if p["hidden"]]
    if hidden and not secret:
        print(f"警告：{len(hidden)} 篇隐藏文章未生成，因为缺少 secret.key")
        hidden = []

    counts: dict[str, int] = {}
    for item in past:
        counts[item["category"]] = counts.get(item["category"], 0) + 1
    cats = [
        {"name": name, "key": CATEGORY_KEYS.get(name, "other"), "count": count}
        for name, count in sorted(counts.items(), key=lambda x: -x[1])
    ]

    hidden_counts: dict[str, int] = {}
    for item in hidden:
        hidden_counts[item["category"]] = hidden_counts.get(item["category"], 0) + 1

    all_hidden_link = (
        {"count": len(hidden), "href": f"{base}hidden/", "label": "全部隐藏文章"}
        if hidden
        else None
    )

    def cat_hidden_link(cat_name: str) -> dict | None:
        n = hidden_counts.get(cat_name, 0)
        if not n:
            return None
        key = CATEGORY_KEYS.get(cat_name, "other")
        return {
            "count": n,
            "href": f"{base}hidden/category/{key}/",
            "label": "本类隐藏文章",
        }

    pages = paginate(past)
    for i, chunk in enumerate(pages, 1):
        rel = "past/index.html" if i == 1 else f"past/page/{i}/index.html"
        render(
            "past_list.html",
            rel,
            section="past",
            posts=chunk,
            pager=build_pager(base, None, i, len(pages)),
            cats=cats,
            active_cat=None,
            heading="过往",
            total=len(past),
            hidden_link=all_hidden_link,
        )

    for cat in cats:
        items = [p for p in past if p["category"] == cat["name"]]
        cat_pages = paginate(items)
        for i, chunk in enumerate(cat_pages, 1):
            rel = f"past/category/{cat['key']}/" + (
                "" if i == 1 else f"page/{i}/"
            ) + "index.html"
            render(
                "past_list.html",
                rel,
                section="past",
                posts=chunk,
                pager=build_pager(base, cat["key"], i, len(cat_pages)),
                cats=cats,
                active_cat=cat["name"],
                heading=cat["name"],
                total=len(items),
                hidden_link=cat_hidden_link(cat["name"]),
            )

    for item in past:
        body, toc = build_toc(item["html"])
        render(
            "past_post.html",
            f"past/{item['slug']}/index.html",
            section="past",
            post={**item, "html": body},
            toc=toc,
            wide=True,
            math=item["math"],
        )

    if hidden:
        for item in hidden:
            body, toc = build_toc(item["html"])
            payload = seal(
                {"title": item["title"], "html": body, "toc": toc}, *secret
            )
            render(
                "hidden_post.html",
                f"hidden/{item['slug']}/index.html",
                section="past",
                post=item,
                payload=payload,
                wide=True,
                math=True,
            )

        listing = [
            {"t": p["title"], "u": p["url"], "d": p["date_text"]} for p in hidden
        ]
        hidden_cats = [
            {"name": name, "key": CATEGORY_KEYS.get(name, "other"), "count": n}
            for name, n in sorted(hidden_counts.items(), key=lambda x: -x[1])
        ]
        payload = seal({"title": "隐藏文章", "items": listing}, *secret)
        render(
            "hidden_index.html",
            "hidden/index.html",
            section="past",
            payload=payload,
            math=True,
            count=len(hidden),
            heading="隐藏文章",
            chips=hidden_cats,
        )

        for name, n in hidden_counts.items():
            key = CATEGORY_KEYS.get(name, "other")
            subset = [p for p in hidden if p["category"] == name]
            listing = [
                {"t": p["title"], "u": p["url"], "d": p["date_text"]} for p in subset
            ]
            payload = seal({"title": name, "items": listing}, *secret)
            render(
                "hidden_index.html",
                f"hidden/category/{key}/index.html",
                section="past",
                payload=payload,
                math=True,
                count=n,
                heading=name,
                chips=hidden_cats,
                active_cat=name,
                back_href=f"{base}hidden/",
                public_href=f"{base}past/category/{key}/",
            )
    by_term: dict[str, list[dict]] = {}
    for subject in subjects:
        by_term.setdefault(subject["term"] or "未分类", []).append(subject)
    terms = [
        {"name": name, "subjects": sorted(items, key=lambda s: s["order"])}
        for name, items in sorted(by_term.items())
    ]
    render(
        "notes_list.html",
        "notes/index.html",
        section="notes",
        subjects=subjects,
        terms=terms,
    )
    for subject in subjects:
        render(
            "subject.html",
            f"notes/{subject['slug']}/index.html",
            section="notes",
            subject=subject,
            wider=True,
        )
        for item in subject["entries"]:
            if item["has_page"]:
                render(
                    "item.html",
                    f"notes/{subject['slug']}/{item['slug']}/index.html",
                    section="notes",
                    subject=subject,
                    item=item,
                    math=item["math"],
                )
            elif item["pdf"]:
                pdf_only = item["pdf"].lower().endswith(".pdf")
                render(
                    "item_pdf.html" if pdf_only else "item_file.html",
                    f"notes/{subject['slug']}/{item['slug']}/index.html",
                    section="notes",
                    subject=subject,
                    item=item,
                    wider=True,
                )

        secret_entries = subject["hidden_entries"]
        if secret_entries and secret:
            for entry in secret_entries:
                src = STATIC / entry["pdf"] if entry["pdf"] else None
                if not src or not src.exists():
                    continue
                enc_rel = entry["pdf"].replace("private/", "files/", 1) + ".enc"
                pending_enc.append((enc_rel, seal_bytes(src.read_bytes(), *secret)))
                payload = seal(
                    {"title": entry["title"], "file": f"{base}{enc_rel}"}, *secret
                )
                render(
                    "hidden_file.html",
                    f"notes/{subject['slug']}/{entry['slug']}/index.html",
                    section="notes",
                    subject=subject,
                    item=entry,
                    payload=payload,
                    wider=True,
                )


    shutil.copy2(STATIC / "style.css", OUT / "assets" / "style.css")
    shutil.copy2(STATIC / "lock.js", OUT / "assets" / "lock.js")
    shutil.copy2(STATIC / "math.js", OUT / "assets" / "math.js")
    light_css = HtmlFormatter(style="friendly").get_style_defs("pre.code")
    dark_css = HtmlFormatter(style="native").get_style_defs("pre.code")
    (OUT / "assets" / "pygments.css").write_text(
        light_css + "\n@media (prefers-color-scheme: dark) {\n" + dark_css + "\n}\n",
        encoding="utf-8",
    )
    files_src = STATIC / "files"
    if files_src.exists():
        shutil.copytree(files_src, OUT / "files")
    for rel, text in pending_enc:
        target = OUT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    print(
        f"生成完成：文章 {len(posts)}，过往 {len(past)}，隐藏 {len(hidden)}，科目 {len(subjects)} -> {OUT}"
    )


if __name__ == "__main__":
    main()
