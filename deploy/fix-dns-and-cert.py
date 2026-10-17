# -*- coding: utf-8 -*-
"""Apply nginx, reload, and try to expand TLS to cover zitoglobal.com + www."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HOST = "root@47.82.99.116"
KEY = Path.home() / ".ssh" / "zito-mail-new"
ROOT = Path(__file__).resolve().parents[1]
CONF = Path(__file__).resolve().parent / "nginx-zito-official.conf"


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.check_call(cmd)


def ssh(remote: str) -> None:
    run(
        [
            "ssh",
            "-i",
            str(KEY),
            "-o",
            "IdentitiesOnly=yes",
            "-o",
            "StrictHostKeyChecking=no",
            "-o",
            "BatchMode=yes",
            HOST,
            remote,
        ]
    )


def main() -> None:
    if not KEY.exists():
        raise SystemExit(f"missing key {KEY}")

    run(
        [
            "scp",
            "-i",
            str(KEY),
            "-o",
            "IdentitiesOnly=yes",
            "-o",
            "StrictHostKeyChecking=no",
            str(CONF),
            f"{HOST}:/etc/nginx/sites-available/zito-official",
        ]
    )
    ssh("nginx -t && systemctl reload nginx && echo NGINX_OK")

    # Probe whether apex still has the dead A record
    ssh(
        "set -e; "
        "echo 'DNS apex:'; dig +short zitoglobal.com A; "
        "if dig +short zitoglobal.com A | grep -q '43.166.233.211'; then "
        "echo 'BLOCKED: delete A 43.166.233.211 on DNSPod (NS: cow/cormorant.dnspod.net), keep only 47.82.99.116'; "
        "exit 0; "
        "fi; "
        "echo 'DNS clean — expanding certificate'; "
        "certbot certonly --nginx --non-interactive --agree-tos "
        "--cert-name www.zitoglobal.com "
        "-d www.zitoglobal.com -d zitoglobal.com "
        "--expand || certbot certonly --nginx --non-interactive --agree-tos "
        "-d www.zitoglobal.com -d zitoglobal.com; "
        "echo CERT_DONE"
    )


if __name__ == "__main__":
    main()
