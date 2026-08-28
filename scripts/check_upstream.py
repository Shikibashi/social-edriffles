#!/usr/bin/env python3
"""Read-only pinned upstream status check; never fetches or mutates trees."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(
        args,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    ).stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fast", action="store_true")
    args = parser.parse_args()

    data: dict[str, Any] = json.loads(
        (ROOT / "artifacts/upstream-baseline.json").read_text()
    )
    rows: list[dict[str, object]] = []
    for name, item in data["upstreams"].items():
        path = ROOT / item["path"]
        current = run("git", "rev-parse", "HEAD", cwd=path)
        remote = run("git", "remote", "get-url", "origin", cwd=path)
        expected = item["forkSha"]
        status = "CURRENT" if current == expected else "LOCAL-DIVERGED"
        if not current:
            status = "INVALID-BASELINE"
        rows.append(
            {
                "name": name,
                "path": item["path"],
                "expectedForkSha": expected,
                "currentSha": current,
                "remote": remote or item["remote"],
                "status": status,
            }
        )

    result: dict[str, Any] = {
        "kind": "upstream-status",
        "readOnly": True,
        "networkFetch": False,
        "classification": "LOCAL-HISTORY",
        "upstreams": rows,
        "fast": args.fast,
        "ok": all(row["status"] == "CURRENT" for row in rows),
    }
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
