from pathlib import Path
from PIL import Image

dst = Path(r"D:/ZITO-OFFICIAL/assets/brand")
prev = Path(r"D:/ZITO-OFFICIAL/_preview")
prev.mkdir(exist_ok=True)

for name in ["zieshine-wordmark.png", "elevia-wordmark.png", "manlor-wordmark.png"]:
    im = Image.open(dst / name).convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    out = Image.alpha_composite(bg, im)
    out.convert("RGB").save(prev / f"check-{name}", quality=95)
    ink = sum(1 for r, g, b, a in im.getdata() if a > 20 and (r + g + b) < 600)
    print(name, "ink", ink, "size", im.size)
