"""诊断 GitHub Pages 构建失败：列出工作流步骤与错误注解。"""

from __future__ import annotations

import os

import requests

P = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
H = {
    "Authorization": "Bearer " + os.environ["GITHUB_TOKEN"],
    "Accept": "application/vnd.github+json",
}
API = "https://api.github.com/repos/ffffyc/ffffyc.github.io"


def main() -> None:
    runs = requests.get(f"{API}/actions/runs?per_page=3", headers=H, proxies=P, timeout=40).json()
    for run in runs.get("workflow_runs", []):
        print("RUN", run["id"], run["status"], run["conclusion"], run["created_at"])
        jobs = requests.get(
            f"{API}/actions/runs/{run['id']}/jobs", headers=H, proxies=P, timeout=40
        ).json()
        for job in jobs.get("jobs", []):
            print("  JOB", job["name"], job["conclusion"])
            for step in job.get("steps", []):
                print("    -", step["name"], step["conclusion"])
            for ann in requests.get(
                f"{API}/check-runs/{job['id']}/annotations", headers=H, proxies=P, timeout=40
            ).json():
                print("    ANN", ann.get("annotation_level"), ann.get("message", "")[:300])


if __name__ == "__main__":
    main()
