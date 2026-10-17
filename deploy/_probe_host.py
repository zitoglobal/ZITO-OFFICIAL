# -*- coding: utf-8 -*-
import subprocess
from pathlib import Path

checks = [
    ("c:\\temp\\zito-sg.pem", "root@47.84.47.222"),
    ("c:\\temp\\hk.pem", "root@47.76.184.126"),
    ("c:\\temp\\hk.pem", "root@47.82.99.116"),
    ("c:\\temp\\zito-sg.pem", "root@47.82.99.116"),
]
for key, host in checks:
    if not Path(key).exists():
        print("NOKEY", key)
        continue
    cmd = [
        "ssh", "-i", key, "-o", "BatchMode=yes", "-o", "ConnectTimeout=10",
        "-o", "StrictHostKeyChecking=no", host,
        "hostname; ls /var/www; grep -l zitoglobal /etc/nginx/sites-enabled/* 2>/dev/null || true",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print("====", host, key, "code", r.returncode)
    print((r.stdout or "")[:800])
    if r.returncode != 0:
        print((r.stderr or "")[:300])
