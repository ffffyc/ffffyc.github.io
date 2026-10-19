"""通过 GitHub API 建仓库、开 Pages，并用临时凭据推送 docs。

token 从环境变量 GITHUB_TOKEN 读取，不落盘。
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
OWNER = "ffffyc"
REPO = "ffffyc.github.io"
PROXY = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEAD = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def api(method: str, path: str, **kwargs):
    r = requests.request(
        method, f"https://api.github.com{path}", headers=HEAD, proxies=PROXY, timeout=60, **kwargs
    )
    return r


def ensure_repo() -> None:
    r = api("GET", f"/repos/{OWNER}/{REPO}")
    if r.status_code == 200:
        print("仓库已存在")
        return
    r = api(
        "POST",
        "/user/repos",
        json={
            "name": REPO,
            "description": "ffffyc 的个人站点：过往文章与课程资料",
            "homepage": f"https://{REPO}",
            "private": False,
            "has_wiki": False,
        },
    )
    print("创建仓库", r.status_code, r.json().get("full_name") or r.text[:200])


def ensure_pages() -> None:
    r = api("GET", f"/repos/{OWNER}/{REPO}/pages")
    if r.status_code == 200:
        print("Pages 已开启", r.json().get("source"))
        return
    r = api(
        "POST",
        f"/repos/{OWNER}/{REPO}/pages",
        json={"source": {"branch": "main", "path": "/docs"}},
    )
    print("开启 Pages", r.status_code, r.text[:200] if r.status_code >= 300 else "")


def push() -> None:
    git = str(Path(os.environ["LOCALAPPDATA"]) / "PortableGit" / "bin" / "git.exe")
    url = f"https://{OWNER}:{TOKEN}@github.com/{OWNER}/{REPO}.git"
    env = dict(os.environ, HTTPS_PROXY=PROXY["https"], HTTP_PROXY=PROXY["http"])
    subprocess.run([git, "remote", "remove", "origin"], cwd=ROOT, capture_output=True)
    subprocess.run([git, "remote", "add", "origin", url], cwd=ROOT, check=True, env=env)
    code = subprocess.run(
        [git, "push", "-u", "origin", "main", "--progress"], cwd=ROOT, env=env
    ).returncode
    subprocess.run(
        [git, "remote", "set-url", "origin", f"https://github.com/{OWNER}/{REPO}.git"],
        cwd=ROOT,
        env=env,
    )
    print("推送返回码", code)
    sys.exit(code)


if __name__ == "__main__":
    if not TOKEN:
        sys.exit("缺少 GITHUB_TOKEN")
    ensure_repo()
    if len(sys.argv) > 1 and sys.argv[1] == "pages":
        ensure_pages()
    push()
