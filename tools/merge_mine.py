"""把后台清单里的隐藏文章并入 list.json，供后续抓正文使用。"""

import json
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"
old = json.loads((DATA / "list.json").read_text(encoding="utf-8"))
mine = json.loads((DATA / "mine.json").read_text(encoding="utf-8"))

have = {it["lid"] for it in old}
merged = list(old)
added = 0
for it in mine:
    if it["lid"] in have:
        continue
    merged.append(it)
    added += 1

merged.sort(key=lambda x: -int(x["time"]))
(DATA / "list.json").write_text(json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8")
print("原有", len(old), "新增", added, "合计", len(merged))

hidden = [it for it in mine if str(it.get("status")) != "2"]
print("隐藏文章分类:", {})
from collections import Counter

print(Counter(str(it.get("category")) for it in hidden))
