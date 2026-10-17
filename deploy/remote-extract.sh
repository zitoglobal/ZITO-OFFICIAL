#!/bin/bash
set -euo pipefail
python3 -c 'import zipfile; zipfile.ZipFile("/tmp/zito-official.zip").extractall("/var/www/zito-official")'
# Drop factory/product photo assets — site is wordmark-only
rm -rf /var/www/zito-official/assets/photos
test -f /var/www/zito-official/index.html
test -f /var/www/zito-official/assets/css/site.css
! grep -RIn 'assets/photos/' /var/www/zito-official --include='*.html' --include='*.css'
curl -skI --resolve www.zitoglobal.com:443:127.0.0.1 https://www.zitoglobal.com/ | head -n 8
curl -sk --resolve www.zitoglobal.com:443:127.0.0.1 https://www.zitoglobal.com/ | grep -o '<title>[^<]*</title>'
ls -la /var/www/zito-official/assets/brand/logo-nav.png

