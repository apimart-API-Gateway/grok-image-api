#!/usr/bin/env python3
"""Generate one image with Grok Image (grok-imagine-1.5-apimart) and download the result."""

import argparse, os, pathlib, time
import requests

BASE = os.environ.get("APIMART_BASE_URL", "https://api.apimart.ai/v1")
HEADERS = {"Authorization": f"Bearer {os.environ['APIMART_API_KEY']}", "Content-Type": "application/json"}


def generate(prompt: str, size: str = "1:1", resolution: str = "1K",
             references: list[str] | None = None) -> dict:
    body = {"model": "grok-imagine-1.5-apimart", "prompt": prompt, "size": size, "resolution": resolution, "n": 1}
    if references:
        body["image_urls"] = references
    created = requests.post(f"{BASE}/images/generations", headers=HEADERS, json=body, timeout=60)
    created.raise_for_status()
    task_id = created.json()["data"]["id"]
    delay = 3
    for _ in range(60):
        task = requests.get(f"{BASE}/tasks/{task_id}", headers=HEADERS, timeout=60).json()["data"]
        if task["status"] in ("completed", "failed"):
            return task
        time.sleep(delay)
        delay = min(delay * 2, 10)
    raise TimeoutError(task_id)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Grok Image image generation")
    ap.add_argument("--prompt", default="A bamboo forest path under moonlight")
    ap.add_argument("--size", default="1:1", help="`1:1`, `16:9`, `9:16`, `3:2`, `2:3`")
    ap.add_argument("--resolution", default="1K", choices=["1K", "2K", "4K"])
    ap.add_argument("--reference", action="append", help="reference image URL or data URL (repeatable)")
    ap.add_argument("--out", default="out")
    args = ap.parse_args()

    task = generate(args.prompt, args.size, args.resolution, args.reference)
    print(f"status={task['status']} cost={task.get('cost')} credits={task.get('credits_cost')}")
    pathlib.Path(args.out).mkdir(parents=True, exist_ok=True)
    for url in (task.get("result", {}).get("images", [{}])[0].get("url") or []):
        dest = pathlib.Path(args.out) / url.rsplit("/", 1)[-1]
        dest.write_bytes(requests.get(url, timeout=120).content)
        print("saved", dest)
