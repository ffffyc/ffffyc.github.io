"""公式手册是自制材料，从「参考资料」挪到页脚式的小字条目。"""

from pathlib import Path

import yaml

FOLDER = Path(__file__).resolve().parent.parent / "content" / "notes" / "advanced-calculus-1"
meta_path = FOLDER / "_subject.yaml"
meta = yaml.safe_load(meta_path.read_text(encoding="utf-8"))

resources = meta.get("resources") or []
handbook = None
keep = []
for item in resources:
    if "formula-handbook" in str(item.get("file", "")):
        handbook = item
    else:
        keep.append(item)

meta["resources"] = keep
if handbook:
    meta["extras"] = [
        {
            "title": "公式手册",
            "note": "展开、等价无穷小、三角恒等式、常用求和",
            "file": "files/notes/advanced-calculus-1/formula-handbook.pdf",
        }
    ]
meta_path.write_text(yaml.safe_dump(meta, allow_unicode=True, sort_keys=False), encoding="utf-8")
print("resources", len(keep), "extras", meta.get("extras"))
