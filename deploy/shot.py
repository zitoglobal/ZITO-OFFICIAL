from pathlib import Path
from playwright.sync_api import sync_playwright

out = Path(r"D:\ZITO-OFFICIAL\_preview")
out.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge")
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:3320/", wait_until="networkidle")
    page.wait_for_timeout(900)
    page.screenshot(path=str(out / "v3-fold.png"))
    page.evaluate("window.scrollTo(0, 950)")
    page.wait_for_timeout(500)
    page.screenshot(path=str(out / "v3-ledger.png"))
    page.evaluate("window.scrollTo(0, 1750)")
    page.wait_for_timeout(500)
    page.screenshot(path=str(out / "v3-brands.png"))
    browser.close()

print("shots ok")
