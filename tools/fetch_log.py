"""下载失败的 Pages 构建作业日志并打印关键行。"""

from __future__ import annotations

import io
import os
import zipfile

import requests

P = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
H = {"Authorization": "Bearer " + os.environ["GITHUB_TOKEN"], "Accept": "application/vnd.github+json"}
API = "https://api.github.com/repos/ffffyc/ffffyc.github.io"

runs = requests.get(f"{API}/actions/runs?per_page=1", headers=H, proxies=P, timeout=40).json()
run = runs["workflow_runs"][0]
print("run", run["id"], run["conclusion"])
jobs = requests.get(f"{API}/actions/runs/{run['id']}/jobs", headers=H, proxies=P, timeout=40).json()
for job in jobs["jobs"]:
    if job["conclusion"] != "failure":
        continue
    resp = requests.get(f"{API}/actions/jobs/{job['id']}/logs", headers=H, proxies=P, timeout=120)
    print("log status", resp.status_code, len(resp.content))
    if resp.status_code != 200:
        continue
    if not resp.content.startswith(b"PK"):
        keys = ("Error", "error", "Liquid", "Invalid", "fatal", "Exception", "jekyll")
        for line in resp.text.splitlines():
            if any(k in line for k in keys):
                print(line[:400])
        continue
    zf = zipfile.ZipFile(io.BytesIO(resp.content))
    for name in zf.namelist():
        text = zf.read(name).decode("utf-8", "ignore")
        if "Build with Jekyll" in name:
            print("=== ", name)
            print(text[-4000:])
