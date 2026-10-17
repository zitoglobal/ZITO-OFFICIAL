#!/bin/bash
set -euo pipefail
sed -i 's/\r$//' /tmp/zito-official.conf
cp /tmp/zito-official.conf /etc/nginx/sites-available/zito-official
ln -sf /etc/nginx/sites-available/zito-official /etc/nginx/sites-enabled/zito-official
nginx -t
systemctl reload nginx
curl -sI https://www.zitoglobal.com/ | head -n 12
