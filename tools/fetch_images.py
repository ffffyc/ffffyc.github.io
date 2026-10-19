"""把 content/past 里引用的外链图片下载到 static/files/luogu/，并把正文改成站内路径。"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
PAST = ROOT / "content" / "past"
DEST = ROOT / "static" / "files" / "luogu"
IMG = re.compile(r"!\[([^\]]*)\]\((https?://[^)\s]+)\)")
HEAD = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.luogu.com.cn/"}


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    total = 0
    for path in sorted(PAST.glob("*.md")):
        lid = path.stem
        text = path.read_text(encoding="utf-8")

        def repl(m: re.Match) -> str:
            nonlocal total
            alt, url = m.group(1), m.group(2)
            if not url.startswith("http"):
                return m.group(0)
            ext = url.split("?")[0].rsplit(".", 1)[-1].lower()
            if ext not in ("png", "jpg", "jpeg", "gif", "webp", "svg"):
                ext = "png"
            name = hashlib.md5(url.encode()).hexdigest()[:10] + "." + ext
            target = DEST / lid / name
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                try:
                    r = requests.get(url, headers=HEAD, timeout=30)
                    r.raise_for_status()
                    target.write_bytes(r.content)
                except Exception as exc:  # noqa: BLE001
                    print("下载失败", url, exc)
                    return m.group(0)
            total += 1
            return f"![{alt}](/files/luogu/{lid}/{name})"

        new = IMG.sub(repl, text)
        if new != text:
            path.write_text(new, encoding="utf-8")
    print("处理图片", total)


if __name__ == "__main__":
    main()
