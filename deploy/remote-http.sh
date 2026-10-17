#!/bin/bash
set -euo pipefail
mkdir -p /var/www/zito-official /var/www/html
find /var/www/zito-official -mindepth 1 -delete
python3 -c 'import zipfile; zipfile.ZipFile("/tmp/zito-official.zip").extractall("/var/www/zito-official")'
test -f /var/www/zito-official/index.html
sed -i 's/\r$//' /tmp/zito-official-http.conf
cp /tmp/zito-official-http.conf /etc/nginx/sites-available/zito-official
ln -sf /etc/nginx/sites-available/zito-official /etc/nginx/sites-enabled/zito-official
nginx -t
systemctl reload nginx
curl -sI -H "Host: zitoglobal.com" http://127.0.0.1/ | head -n 8
