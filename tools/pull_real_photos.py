# -*- coding: utf-8 -*-
"""Copy real factory + product photos into ZITO-OFFICIAL assets (no AI)."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(r"D:\ZITO-OFFICIAL")
OUT = ROOT / "assets" / "photos"
FAC = Path(r"D:\ZITO-CORE-Sync\repo") / "VAOSE 沃斯" / "工厂实拍"
ZS_PROD = Path(r"D:\ZITO.AI项目\ZIESHINE智能企业官网\assets\products")
LOOK_W = Path(r"D:\ZITO-CORE-Sync\repo") / "VAOSE 沃斯" / "lookbook" / "women" / "media"
LOOK_M = Path(r"D:\ZITO-CORE-Sync\repo") / "VAOSE 沃斯" / "lookbook" / "men" / "media"

MAP = {
    # hero / floors
    "hero-floor.webp": FAC / "zieshine" / "zs-floor-tegote.webp",
    "hero-sewing.webp": FAC / "manlor" / "ml-hero-floor.webp",
    "cap-design.webp": FAC / "zieshine" / "zs-p14.webp",
    "cap-fabric.webp": FAC / "manlor" / "ml-fabric-insp.webp",
    "cap-manufacturing.webp": FAC / "elevia" / "el-sewing-line.webp",
    "about-floor.webp": FAC / "manlor" / "ml-workshop-wide.webp",
    "about-sewing.webp": FAC / "manlor" / "ml-sewing-coat.webp",
    "about-qc.webp": FAC / "zieshine" / "zs-p05.webp",
    "brand-zieshine.webp": FAC / "zieshine" / "zs-p07.webp",
    "brand-elevia.webp": FAC / "elevia" / "el-sewing-prod.webp",
    "brand-manlor.webp": FAC / "manlor" / "ml-hanging-line.webp",
    "strip-cut.webp": FAC / "zieshine" / "zs-cut-cnc.webp",
    "strip-press.webp": FAC / "manlor" / "ml-pressing.webp",
    "strip-qc.webp": FAC / "elevia" / "el-qc.webp",
    "contact-side.webp": FAC / "elevia" / "el-workshop.webp",
}

# product covers (real lookbook / ZIESHINE catalog)
PRODUCTS = {
    "prod-yoga.webp": ZS_PROD / "brushed-anti-shock-yoga-set-7028__oat-apricot__md.webp",
    "prod-tennis.webp": ZS_PROD / "mock-collar-tennis-dress__linen__md.webp",
    "prod-swim.webp": ZS_PROD / "black-arched-neck-onepiece__dark-choco__md.webp",
}


def first_cover(folder: Path) -> Path | None:
    if not folder.exists():
        return None
    for sku in sorted(folder.iterdir()):
        if not sku.is_dir():
            continue
        jpgs = sorted(sku.glob("*.jpg"))
        if jpgs:
            return jpgs[0]
    return None


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    n = 0
    for name, src in {**MAP, **PRODUCTS}.items():
        if not src.exists():
            print("MISSING", src)
            continue
        dest = OUT / name
        shutil.copy2(src, dest)
        n += 1
        print("ok", name)

    # fashion lookbook covers as jpg→ keep as jpg
    for label, root in (("prod-women.jpg", LOOK_W), ("prod-men.jpg", LOOK_M)):
        cover = first_cover(root)
        if cover:
            shutil.copy2(cover, OUT / label)
            n += 1
            print("ok", label, "<-", cover)
    print("copied", n, "->", OUT)


if __name__ == "__main__":
    main()
