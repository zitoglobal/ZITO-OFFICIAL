# ZITO-OFFICIAL

## 语言要求
- 除非用户明确要求，否则所有回复一律使用简体中文。
- 面向海外访客的页面正文可用英文；解释、总结、建议用中文。

## 项目定位
- ZITO Global 集团官网。
- **正式规范地址（canonical）**：`https://www.zitoglobal.com/`
- 服务器：`47.82.99.116`，目录 `/var/www/zito-official`
- 真实目录：`D:\ZITO-OFFICIAL`；本工作区 `ZITO-OFFICIAL/` 为 junction。
- GitHub：`https://github.com/zitoglobal/ZITO-OFFICIAL`

## 域名与 HTTPS
- NS：DNSPod（`cow.dnspod.net` / `cormorant.dnspod.net`）
- **正式规范地址**：`https://www.zitoglobal.com/`
- 根域 / www 的 A 均指向 `47.82.99.116`
- 证书：`www.zitoglobal.com`（SAN 含 `zitoglobal.com`），有效至约 2027-01-14
- 跳转：`http(s)://zitoglobal.com/*` 与 `http://www/*` → **301** → `https://www.zitoglobal.com/*`
- 变更 nginx/证书：`python deploy/fix-dns-and-cert.py`

## 本地
- 静态站点：`npx --yes serve -l 3320 .` → `http://localhost:3320`

## 部署
- `python deploy/deploy.py`（站点文件）
- `python deploy/fix-dns-and-cert.py`（nginx + 证书，DNS 干净时才扩根域）

## 约束
- 禁止建议对接已下线的 `crm.zitoglobal.com`。
- 部署主机/密钥只写本机 `deploy/deploy.local.env`（勿提交）。
- 勿与 `ZIESHINE-OFFICIAL` / 各品牌站混改同一文件后两边硬推。
