# -*- coding: utf-8 -*-
"""Deploy ZITO-OFFICIAL files to the Singapore host (working key)."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEPLOY = Path(__file__).resolve().parent
KEY = Path(r"c:\temp\zito-sg.pem")
HOST = "root@47.84.47.222"


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.check_call(cmd)


def main() -> None:
    if not KEY.exists():
        raise SystemExit(f"missing key {KEY}")
    run([sys.executable, str(DEPLOY / "pack.py")])
    zpath = Path(os.environ.get("TEMP", r"c:\temp")) / "zito-official.zip"
    if not zpath.exists():
        raise SystemExit(f"zip missing: {zpath}")
    run(["scp", "-i", str(KEY), "-o", "StrictHostKeyChecking=no", str(zpath), f"{HOST}:/tmp/zito-official.zip"])
    run(
        [
            "scp",
            "-i",
            str(KEY),
            "-o",
            "StrictHostKeyChecking=no",
            str(DEPLOY / "nginx-zito-official.conf"),
            f"{HOST}:/tmp/nginx-zito-official.conf",
        ]
    )
    remote = r"""
set -e
mkdir -p /var/www/zito-official
python3 - <<'PY'
import zipfile
zipfile.ZipFile('/tmp/zito-official.zip').extractall('/var/www/zito-official')
print('extracted')
PY
test -f /var/www/zito-official/index.html
test -f /var/www/zito-official/assets/photos/hero-floor.webp
if [ -f /etc/letsencrypt/live/www.zitoglobal.com/fullchain.pem ]; then
  sed -i 's/\r$//' /tmp/nginx-zito-official.conf
  cp /tmp/nginx-zito-official.conf /etc/nginx/sites-enabled/zito-official
  nginx -t && systemctl reload nginx && echo NGINX_ENABLED
else
  echo NO_CERT_ON_SG
  ls /etc/letsencrypt/live 2>/dev/null || true
fi
grep -o 'Real floors' /var/www/zito-official/index.html | head -1
ls /var/www/zito-official/assets/photos | wc -l
"""
    run(["ssh", "-i", str(KEY), "-o", "StrictHostKeyChecking=no", HOST, remote])
    print("deployed files to", HOST, "/var/www/zito-official")


if __name__ == "__main__":
    main()
