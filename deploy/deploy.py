# -*- coding: utf-8 -*-
"""Pack and deploy ZITO-OFFICIAL to www.zitoglobal.com."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEPLOY = Path(__file__).resolve().parent
HOST = "root@47.82.99.116"
REMOTE = "/var/www/zito-official"
KEYS = [
    Path.home() / ".ssh" / "zito-mail-new",
    Path(r"c:\temp\hk.pem"),
    Path(r"c:\temp\zito-sg.pem"),
]


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.check_call(cmd)


def ssh_base(key: Path) -> list[str]:
    return [
        "ssh",
        "-i",
        str(key),
        "-o",
        "BatchMode=yes",
        "-o",
        "IdentitiesOnly=yes",
        "-o",
        "ConnectTimeout=15",
        "-o",
        "StrictHostKeyChecking=no",
    ]


def pick_key() -> Path:
    for k in KEYS:
        if not k.exists():
            continue
        try:
            subprocess.check_call(
                ssh_base(k)
                + [
                    HOST,
                    "test -d /var/www/zito-official || mkdir -p /var/www/zito-official",
                ]
            )
            print("using key", k)
            return k
        except subprocess.CalledProcessError:
            continue
    raise SystemExit("No SSH key can reach " + HOST)


def main() -> None:
    key = pick_key()
    run([sys.executable, str(DEPLOY / "pack.py")])
    zpath = Path(r"c:\temp\zito-official.zip")
    # TEMP may vary
    import os
    import glob

    candidates = [
        Path(os.environ.get("TEMP", r"c:\temp")) / "zito-official.zip",
        Path(r"c:\temp\zito-official.zip"),
    ]
    zpath = next((p for p in candidates if p.exists()), None)
    if not zpath:
        raise SystemExit("zip missing after pack.py")
    scp = [
        "scp",
        "-i",
        str(key),
        "-o",
        "IdentitiesOnly=yes",
        "-o",
        "StrictHostKeyChecking=no",
    ]
    run(scp + [str(zpath), f"{HOST}:/tmp/zito-official.zip"])
    run(scp + [str(DEPLOY / "remote-extract.sh"), f"{HOST}:/tmp/remote-extract.sh"])
    run(ssh_base(key) + [HOST, "bash /tmp/remote-extract.sh"])
    print("deployed", REMOTE)


if __name__ == "__main__":
    main()
