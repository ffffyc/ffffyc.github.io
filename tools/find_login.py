"""找出哪个浏览器配置里存有洛谷的登录 Cookie。"""

import glob
import os
import shutil
import sqlite3
import tempfile

roots = [
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data"),
    os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data"),
]

for root in roots:
    if not os.path.isdir(root):
        continue
    print("==", root)
    for prof in sorted(glob.glob(os.path.join(root, "*"))):
        if not os.path.isdir(prof):
            continue
        name = os.path.basename(prof)
        for cand in ("Network/Cookies", "Cookies"):
            db = os.path.join(prof, cand)
            if os.path.isfile(db):
                tmp = os.path.join(tempfile.gettempdir(), "ck.db")
                try:
                    shutil.copy2(db, tmp)
                    con = sqlite3.connect(tmp)
                    rows = con.execute(
                        "select name, host_key from cookies where host_key like '%luogu%'"
                    ).fetchall()
                    con.close()
                    if rows:
                        print(f"  {name}: {len(rows)} 条", [r[0] for r in rows][:8])
                except Exception as exc:
                    print(f"  {name}: 读取失败 {exc}")
                break
