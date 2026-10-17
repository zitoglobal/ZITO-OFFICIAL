# -*- coding: utf-8 -*-
"""Rewrite official pages with real photos, pack, deploy to SG host."""
from __future__ import annotations

import os
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(r"D:\ZITO-OFFICIAL")
KEY = Path(r"c:\temp\zito-sg.pem")
HOST = "root@47.84.47.222"
PHOTOS = ROOT / "assets" / "photos"


def w(rel: str, text: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("wrote", rel, path.stat().st_size)


def patch_css() -> None:
    css_path = ROOT / "assets" / "css" / "site.css"
    css = css_path.read_text(encoding="utf-8")
    if "hero-media" in css and "proof-strip" in css:
        print("css already patched")
        return
    old = """/* —— Hero —— */
.hero {
  position: relative;
  overflow: hidden;
  min-height: 100vh;
  min-height: 100dvh;
  display: flex;
  align-items: center;
  background: var(--navy);
  color: var(--white);
  padding: 5.75rem 0 3.75rem;
}

.hero-wash {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 48% 58% at 86% 46%, rgba(10, 102, 255, 0.28), transparent 68%),
    radial-gradient(ellipse 30% 40% at 8% 88%, rgba(0, 194, 255, 0.1), transparent 70%),
    linear-gradient(165deg, var(--navy) 0%, #0e2748 48%, var(--navy-deep) 100%);
  pointer-events: none;
}

.hero-grid {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(0, 0.92fr);
  align-items: center;
  gap: 2rem;
  width: min(100% - 3rem, var(--max));
  margin-inline: auto;
}"""
    new = """/* —— Hero —— */
.hero {
  position: relative;
  overflow: hidden;
  min-height: 100vh;
  min-height: 100dvh;
  display: flex;
  align-items: flex-end;
  background: var(--navy);
  color: var(--white);
  padding: 5.75rem 0 3.75rem;
}
.hero-media { position: absolute; inset: 0; z-index: 0; }
.hero-media img {
  width: 100%; height: 100%; object-fit: cover; object-position: center 42%;
  filter: saturate(0.92) contrast(1.05) brightness(0.72);
  transform: scale(1.03);
}
.hero-wash {
  position: absolute; inset: 0; z-index: 1; pointer-events: none;
  background:
    linear-gradient(180deg, rgba(7,21,37,.35) 0%, rgba(7,21,37,.2) 40%, rgba(7,21,37,.82) 100%),
    linear-gradient(90deg, rgba(7,21,37,.55) 0%, transparent 62%);
}
.hero-grid {
  position: relative; z-index: 2; display: grid; grid-template-columns: 1fr;
  align-items: end; gap: 2rem; width: min(100% - 3rem, var(--max)); margin-inline: auto;
}
.hero-kicker {
  margin: 0 0 .85rem; font-size: .72rem; font-weight: 600;
  letter-spacing: .16em; text-transform: uppercase; color: var(--cyan-on-dark);
}
.proof-strip {
  display: grid; grid-template-columns: repeat(4,1fr); gap: 10px;
  margin-top: -2.5rem; position: relative; z-index: 3;
}
@media (max-width:820px){ .proof-strip{ grid-template-columns:repeat(2,1fr); margin-top:1.25rem; } }
.proof-strip figure{ margin:0; position:relative; aspect-ratio:4/3; overflow:hidden; border-radius:12px; background:var(--navy); box-shadow:0 16px 36px rgba(7,21,37,.18); }
.proof-strip img{ width:100%; height:100%; object-fit:cover; filter:saturate(.94) contrast(1.03); transition:transform .5s var(--ease); }
.proof-strip figure:hover img{ transform:scale(1.04); }
.proof-strip figcaption{ position:absolute; left:10px; bottom:10px; font-size:.68rem; letter-spacing:.12em; text-transform:uppercase; color:#fff; text-shadow:0 1px 10px rgba(0,0,0,.45); }
.product-rail{ padding:4.5rem 0 1rem; }
.product-grid{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; }
@media (max-width:820px){ .product-grid{ grid-template-columns:repeat(2,1fr); } }
.product-grid figure{ margin:0; aspect-ratio:3/4; overflow:hidden; background:#101820; border-radius:2px; position:relative; }
.product-grid img{ width:100%; height:100%; object-fit:cover; object-position:center 22%; transition:transform .5s var(--ease); }
.product-grid figure:hover img{ transform:scale(1.03); }
.product-grid figcaption{ position:absolute; left:10px; bottom:10px; font-size:.66rem; letter-spacing:.12em; text-transform:uppercase; color:#fff; text-shadow:0 1px 8px rgba(0,0,0,.5); }
.brand-card{ display:grid; grid-template-columns:minmax(0,1.1fr) minmax(0,1fr); gap:1.4rem 1.8rem; align-items:center; padding:1.5rem 0; border-top:1px solid var(--line); text-decoration:none; }
.brand-card:last-of-type{ border-bottom:1px solid var(--line); }
.brand-card img{ width:100%; aspect-ratio:16/10; object-fit:cover; border-radius:10px; filter:saturate(.94) contrast(1.03); }
.brand-card strong{ display:block; font-size:1.35rem; font-weight:560; letter-spacing:-.02em; margin-bottom:.35rem; }
.brand-card span{ display:block; color:var(--muted); font-size:.95rem; margin-bottom:.65rem; }
.brand-card i{ font-style:normal; font-weight:560; font-size:.88rem; color:var(--blue); }
@media (max-width:720px){ .brand-card{ grid-template-columns:1fr; } }
.page-hero.photo{ position:relative; overflow:hidden; color:#fff; border-bottom:0; padding:0; background:var(--navy); min-height:min(52vh,420px); display:flex; align-items:flex-end; }
.page-hero.photo .page-hero-media{ position:absolute; inset:0; }
.page-hero.photo .page-hero-media img{ width:100%; height:100%; object-fit:cover; object-position:center 40%; filter:saturate(.92) contrast(1.04) brightness(.68); }
.page-hero.photo .page-hero-veil{ position:absolute; inset:0; background:linear-gradient(180deg,rgba(7,21,37,.25),rgba(7,21,37,.78)); }
.page-hero.photo .wrap{ position:relative; z-index:1; padding:5.5rem 0 2.5rem; }
.page-hero.photo h1{ color:#fff; }
.page-hero.photo p{ color:rgba(255,255,255,.72); }
.cap-photo{ display:grid; grid-template-columns:minmax(0,.95fr) minmax(0,1.2fr); gap:1.5rem 2rem; align-items:center; padding:2rem 0; border-top:1px solid var(--line); }
.cap-photo:last-child{ border-bottom:1px solid var(--line); }
.cap-photo img{ width:100%; aspect-ratio:4/3; object-fit:cover; border-radius:10px; }
@media (max-width:720px){ .cap-photo{ grid-template-columns:1fr; } }
.about-strip{ display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-top:1.5rem; }
@media (max-width:720px){ .about-strip{ grid-template-columns:1fr; } }
.about-strip img{ width:100%; aspect-ratio:4/3; object-fit:cover; border-radius:10px; }"""
    if old not in css:
        # append photo styles before ledger if hero block already changed
        marker = "/* —— Ledger —— */"
        if "proof-strip" not in css and marker in css:
            css = css.replace(marker, new.split("/* —— Ledger —— */")[0] + "\n" + marker if False else new + "\n\n" + marker)
            # simpler: append before footer styles
        if "proof-strip" not in css:
            css = css.replace(marker, new + "\n\n" + marker)
        css_path.write_text(css, encoding="utf-8")
        print("css appended photo blocks")
        return
    css = css.replace(old, new, 1)
    # also inject extra blocks after hero-grid section if not present
    if "proof-strip" not in css:
        css += "\n" + new[new.find(".proof-strip"):]
    css_path.write_text(css, encoding="utf-8")
    print("css hero replaced")


INDEX = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ZITO | Design, Fabric and Manufacturing</title>
  <meta name="description" content="ZITO is an integrated apparel group: style design, fabric development and manufacturing. Brands: ZIESHINE, ELEVIA and MANLOR.">
  <link rel="canonical" href="https://www.zitoglobal.com/">
  <meta property="og:image" content="https://www.zitoglobal.com/assets/photos/hero-floor.webp">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/brand/favicon-32.png">
  <link rel="apple-touch-icon" href="/assets/brand/favicon-180.png">
  <link rel="preload" as="image" href="/assets/photos/hero-floor.webp" fetchpriority="high">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/site.css">
</head>
<body class="home">
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="nav">
      <a class="brand-logo" href="/" aria-label="ZITO home">
        <img class="logo-on-light" src="/assets/brand/logo-nav.png" alt="ZITO 志拓" width="460" height="128">
        <img class="logo-on-dark" src="/assets/brand/logo-hero.png" alt="" width="1151" height="320">
      </a>
      <ul class="menu" id="menu">
        <li><a href="/about.html">About</a></li>
        <li><a href="/capabilities.html">Capabilities</a></li>
        <li><a href="/brands.html">Brands</a></li>
      </ul>
      <a class="nav-cta" href="/contact.html">Contact</a>
      <button class="burger" id="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
    </div>
  </header>
  <main id="main">
    <section class="hero">
      <div class="hero-media" aria-hidden="true">
        <img src="/assets/photos/hero-floor.webp" alt="" width="1800" height="1200" fetchpriority="high">
      </div>
      <div class="hero-wash" aria-hidden="true"></div>
      <div class="hero-grid">
        <div class="hero-copy">
          <p class="hero-kicker">Real floors · Real product</p>
          <h1>Design<span class="dot">.</span> Fabric<span class="dot">.</span><br>Manufacturing<span class="dot">.</span></h1>
          <p class="hero-lead">One path for style, cloth and production — three brand lanes for the category that fits. Shot in our factories, not generated.</p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="/capabilities.html">Capabilities</a>
            <a class="btn btn-ghost" href="/brands.html">Brands</a>
          </div>
        </div>
      </div>
    </section>
    <section class="proof-strip wrap" aria-label="Factory evidence">
      <figure class="reveal"><img src="/assets/photos/strip-cut.webp" alt="CNC cutting" width="1200" height="800" loading="lazy"><figcaption>Cutting</figcaption></figure>
      <figure class="reveal d2"><img src="/assets/photos/hero-sewing.webp" alt="Sewing floor" width="1200" height="800" loading="lazy"><figcaption>Sewing</figcaption></figure>
      <figure class="reveal d3"><img src="/assets/photos/strip-press.webp" alt="Pressing" width="1200" height="800" loading="lazy"><figcaption>Pressing</figcaption></figure>
      <figure class="reveal d3"><img src="/assets/photos/strip-qc.webp" alt="QC" width="1200" height="800" loading="lazy"><figcaption>QC</figcaption></figure>
    </section>
    <section class="ledger">
      <div class="wrap">
        <a class="ledger-row reveal" href="/capabilities.html#design"><em>01</em><h2>Style design</h2><p>Silhouette, pattern and fit locked to the brief before a sample is cut.</p></a>
        <a class="ledger-row reveal d2" href="/capabilities.html#fabric"><em>02</em><h2>Fabric development</h2><p>Cloth engineered with the mills — performance knits, swim and fashion hand-feels.</p></a>
        <a class="ledger-row reveal d3" href="/capabilities.html#manufacturing"><em>03</em><h2>Manufacturing</h2><p>Sample, fit, then sealed bulk — run by the brand that owns the lane.</p></a>
      </div>
    </section>
    <section class="product-rail wrap" aria-label="Product photography">
      <div class="directory-head reveal"><h2>Product on the floor</h2><span>Real samples — activewear, fashion, menswear</span></div>
      <div class="product-grid">
        <figure class="reveal"><img src="/assets/photos/prod-yoga.webp" alt="ZIESHINE yoga set" width="720" height="960" loading="lazy"><figcaption>ZIESHINE</figcaption></figure>
        <figure class="reveal d2"><img src="/assets/photos/prod-tennis.webp" alt="ZIESHINE tennis dress" width="720" height="960" loading="lazy"><figcaption>ZIESHINE</figcaption></figure>
        <figure class="reveal d3"><img src="/assets/photos/prod-women.jpg" alt="Fashion sample" width="720" height="960" loading="lazy"><figcaption>MANLOR lane</figcaption></figure>
        <figure class="reveal d3"><img src="/assets/photos/prod-men.jpg" alt="Menswear sample" width="720" height="960" loading="lazy"><figcaption>ELEVIA / fashion</figcaption></figure>
      </div>
    </section>
    <section class="bridge">
      <div class="wrap bridge-inner reveal">
        <div><h2>One group. Three lanes.</h2><p>The brief stays with the brand built for that category.</p></div>
        <a class="btn btn-ghost" href="/contact.html">Contact</a>
      </div>
    </section>
    <section class="directory">
      <div class="wrap">
        <div class="directory-head reveal"><h2>Brands</h2><span>Each site is the desk for that lane</span></div>
        <a class="brand-card reveal" href="https://www.zieshine.com/" rel="noopener">
          <img src="/assets/photos/brand-zieshine.webp" alt="ZIESHINE sewing floor" width="1400" height="900" loading="lazy">
          <div><strong>ZIESHINE</strong><span>Activewear and swimwear · Dongguan</span><i>zieshine.com →</i></div>
        </a>
        <a class="brand-card reveal d2" href="https://eleviaapparel.com/" rel="noopener">
          <img src="/assets/photos/brand-elevia.webp" alt="ELEVIA production" width="1400" height="900" loading="lazy">
          <div><strong>ELEVIA</strong><span>Men’s performance apparel · Guangzhou</span><i>eleviaapparel.com →</i></div>
        </a>
        <a class="brand-card reveal d3" href="https://manlorapparel.com/" rel="noopener">
          <img src="/assets/photos/brand-manlor.webp" alt="MANLOR hanging line" width="1400" height="900" loading="lazy">
          <div><strong>MANLOR</strong><span>Contemporary fashion · Guangzhou</span><i>manlorapparel.com →</i></div>
        </a>
      </div>
    </section>
    <section class="sign wrap">
      <img src="/assets/brand/logo-vertical.png" alt="ZITO 志拓" width="578" height="400">
      <p>Guangzhou Zito Global Co., Ltd. · Factory photography only — no AI workshop images.</p>
    </section>
  </main>
  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div class="footer-meta">© <span id="y"></span> Guangzhou Zito Global Co., Ltd.</div>
      <div class="footer-links">
        <a href="/about.html">About</a><a href="/capabilities.html">Capabilities</a>
        <a href="/brands.html">Brands</a><a href="/contact.html">Contact</a><a href="/privacy.html">Privacy</a>
      </div>
    </div>
  </footer>
  <script>document.getElementById("y").textContent = new Date().getFullYear();</script>
  <script src="/assets/js/site.js"></script>
</body>
</html>
'''


def pack() -> Path:
    out = Path(os.environ.get("TEMP", r"c:\temp")) / "zito-official.zip"
    skip = {".git", "_preview", "node_modules", "deploy"}
    n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for dirpath, dirs, files in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in skip and not d.startswith(".")]
            for name in files:
                if name.endswith((".pem", ".pyc")):
                    continue
                path = Path(dirpath) / name
                rel = path.relative_to(ROOT).as_posix()
                z.write(path, rel)
                n += 1
    print("packed", out, "files", n, "KB", round(out.stat().st_size / 1024, 1))
    # sanity
    with zipfile.ZipFile(out) as z:
        names = z.namelist()
        assert "assets/photos/hero-floor.webp" in names, "photos missing from zip"
        assert b"Real floors" in z.read("index.html")
    return out


def deploy(zpath: Path) -> None:
    subprocess.check_call(
        ["scp", "-i", str(KEY), "-o", "StrictHostKeyChecking=no", str(zpath), f"{HOST}:/tmp/zito-official.zip"]
    )
    remote = """
set -e
mkdir -p /var/www/zito-official
python3 - <<'PY'
import zipfile
zipfile.ZipFile('/tmp/zito-official.zip').extractall('/var/www/zito-official')
print('extracted ok')
PY
test -f /var/www/zito-official/assets/photos/hero-floor.webp
grep -q 'Real floors' /var/www/zito-official/index.html
# Serve on this host if we can issue/ use cert; otherwise leave files ready
if [ -d /etc/letsencrypt/live/www.zitoglobal.com ]; then
  echo HAS_CERT
else
  echo NO_CERT — files ready at /var/www/zito-official
fi
ls /var/www/zito-official/assets/photos | wc -l
"""
    subprocess.check_call(["ssh", "-i", str(KEY), "-o", "StrictHostKeyChecking=no", HOST, remote])
    print("remote files OK on", HOST)


def main() -> None:
    if not PHOTOS.exists() or not list(PHOTOS.glob("*.webp")):
        subprocess.check_call([sys.executable, str(ROOT / "tools" / "pull_real_photos.py")])
    patch_css()
    w("index.html", INDEX)
    # minimal inner pages with photo heroes
    for name, img, h1, lead in [
        (
            "about.html",
            "about-floor.webp",
            "An apparel group, not a catalogue",
            "ZITO holds the group path: design, fabric and manufacturing. Photography is from our floors — not generated.",
        ),
        (
            "capabilities.html",
            "cap-manufacturing.webp",
            "From sketch to sealed bulk",
            "Style, fabric and manufacturing stay in one group. Real production photography throughout.",
        ),
        (
            "brands.html",
            "hero-sewing.webp",
            "Three directions",
            "Same group capabilities. A different product lane on each brand site.",
        ),
        (
            "contact.html",
            "contact-side.webp",
            "Start with the lane",
            "Category briefs are fastest on the brand site.",
        ),
    ]:
        # keep existing form body for contact by only replacing page-hero — write full short pages
        pass
    # write about/capabilities/brands/contact from templates already prepared in this script's companion files if present
    about = (ROOT / "about.html").read_text(encoding="utf-8")
    if "page-hero photo" not in about:
        w(
            "about.html",
            about.replace(
                '<section class="page-hero">',
                '<section class="page-hero photo"><div class="page-hero-media" aria-hidden="true"><img src="/assets/photos/about-floor.webp" alt="" width="1600" height="1000"></div><div class="page-hero-veil" aria-hidden="true"></div><!--',
                1,
            ).replace("</section>", "-->", 1)
            if False
            else _inner("about", "about-floor.webp", "An apparel group, not a catalogue", "ZITO holds design, fabric and manufacturing. Floor photography only."),
        )
    w("about.html", _inner("about", "about-floor.webp", "An apparel group, not a catalogue", "ZITO holds design, fabric and manufacturing. Floor photography from Dongguan and Guangzhou — not generated sets.") + _about_body())
    w("capabilities.html", _inner("capabilities", "cap-manufacturing.webp", "From sketch to sealed bulk", "Style, fabric and manufacturing stay in one group.") + _cap_body())
    w("brands.html", _inner("brands", "hero-sewing.webp", "Three directions", "Same group. Different product lanes.") + _brands_body())
    w("contact.html", _inner("contact", "contact-side.webp", "Start with the lane", "Category briefs are fastest on the brand site.") + _contact_body())
    z = pack()
    deploy(z)


def _nav(cur: str) -> str:
    items = [("about.html", "About"), ("capabilities.html", "Capabilities"), ("brands.html", "Brands")]
    lis = []
    for href, label in items:
        cur_attr = ' aria-current="page"' if cur in href else ""
        lis.append(f'<li><a href="/{href}"{cur_attr}>{label}</a></li>')
    return "\n".join(lis)


def _inner(cur: str, img: str, h1: str, lead: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{h1.split(',')[0]} — ZITO</title>
  <link rel="canonical" href="https://www.zitoglobal.com/{cur}.html">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/brand/favicon-32.png">
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/site.css">
</head>
<body>
  <header class="site-header"><div class="nav">
    <a class="brand-logo" href="/"><img src="/assets/brand/logo-nav.png" alt="ZITO" width="460" height="128"></a>
    <ul class="menu" id="menu">{_nav(cur)}</ul>
    <a class="nav-cta" href="/contact.html">Contact</a>
    <button class="burger" id="burger" type="button" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div></header>
  <main id="main">
    <section class="page-hero photo">
      <div class="page-hero-media" aria-hidden="true"><img src="/assets/photos/{img}" alt="" width="1600" height="1000"></div>
      <div class="page-hero-veil" aria-hidden="true"></div>
      <div class="wrap"><h1>{h1}</h1><p>{lead}</p></div>
    </section>
"""


def _about_body() -> str:
    return """
    <section class="section"><div class="wrap">
      <div class="about-strip reveal">
        <img src="/assets/photos/about-sewing.webp" alt="Sewing" width="900" height="675" loading="lazy">
        <img src="/assets/photos/about-qc.webp" alt="QC" width="900" height="675" loading="lazy">
        <img src="/assets/photos/cap-manufacturing.webp" alt="Production" width="900" height="675" loading="lazy">
      </div>
      <p class="lede reveal" style="margin-top:1.5rem;max-width:56ch">Guangzhou Zito Global Co., Ltd. keeps ZIESHINE, ELEVIA and MANLOR as separate lanes. ZITO is the front door.</p>
    </div></section>
  </main>
  <footer class="site-footer"><div class="wrap footer-grid">
    <div class="footer-meta">© <span id="y"></span> Guangzhou Zito Global Co., Ltd.</div>
    <div class="footer-links"><a href="/capabilities.html">Capabilities</a><a href="/brands.html">Brands</a><a href="/contact.html">Contact</a></div>
  </div></footer>
  <script>document.getElementById("y").textContent=new Date().getFullYear()</script>
  <script src="/assets/js/site.js"></script>
</body></html>
"""


def _cap_body() -> str:
    return """
    <section class="section"><div class="wrap">
      <article class="cap-photo reveal" id="design">
        <img src="/assets/photos/cap-design.webp" alt="Pattern room" width="1200" height="900" loading="lazy">
        <div><h2>Style design</h2><p>Silhouette, block, pattern and fit developed from a brief or a reference.</p></div>
      </article>
      <article class="cap-photo reveal d2" id="fabric">
        <img src="/assets/photos/cap-fabric.webp" alt="Fabric inspection" width="1200" height="900" loading="lazy">
        <div><h2>Fabric development</h2><p>Hand-feel, stretch, recovery and colour matched to the garment.</p></div>
      </article>
      <article class="cap-photo reveal d3" id="manufacturing">
        <img src="/assets/photos/cap-manufacturing.webp" alt="Sewing line" width="1200" height="900" loading="lazy">
        <div><h2>Manufacturing</h2><p>Sampling and fit first. Bulk follows once the seal is agreed.</p></div>
      </article>
    </div></section>
  </main>
  <footer class="site-footer"><div class="wrap footer-grid">
    <div class="footer-meta">© <span id="y"></span> Guangzhou Zito Global Co., Ltd.</div>
    <div class="footer-links"><a href="/about.html">About</a><a href="/brands.html">Brands</a><a href="/contact.html">Contact</a></div>
  </div></footer>
  <script>document.getElementById("y").textContent=new Date().getFullYear()</script>
  <script src="/assets/js/site.js"></script>
</body></html>
"""


def _brands_body() -> str:
    return """
    <section class="section"><div class="wrap">
      <a class="brand-card reveal" href="https://www.zieshine.com/" rel="noopener">
        <img src="/assets/photos/brand-zieshine.webp" alt="ZIESHINE" width="1400" height="900" loading="lazy">
        <div><strong>ZIESHINE</strong><span>Activewear and swimwear · Dongguan</span><i>zieshine.com →</i></div>
      </a>
      <a class="brand-card reveal d2" href="https://eleviaapparel.com/" rel="noopener">
        <img src="/assets/photos/brand-elevia.webp" alt="ELEVIA" width="1400" height="900" loading="lazy">
        <div><strong>ELEVIA</strong><span>Men’s performance apparel · Guangzhou</span><i>eleviaapparel.com →</i></div>
      </a>
      <a class="brand-card reveal d3" href="https://manlorapparel.com/" rel="noopener">
        <img src="/assets/photos/brand-manlor.webp" alt="MANLOR" width="1400" height="900" loading="lazy">
        <div><strong>MANLOR</strong><span>Contemporary fashion · Guangzhou</span><i>manlorapparel.com →</i></div>
      </a>
    </div></section>
  </main>
  <footer class="site-footer"><div class="wrap footer-grid">
    <div class="footer-meta">© <span id="y"></span> Guangzhou Zito Global Co., Ltd.</div>
    <div class="footer-links"><a href="/capabilities.html">Capabilities</a><a href="/contact.html">Contact</a></div>
  </div></footer>
  <script>document.getElementById("y").textContent=new Date().getFullYear()</script>
  <script src="/assets/js/site.js"></script>
</body></html>
"""


def _contact_body() -> str:
    return """
    <section class="section"><div class="wrap split">
      <form class="form reveal" action="mailto:hello@zitoglobal.com" method="get" enctype="text/plain">
        <label>Name<input name="name" required autocomplete="name"></label>
        <label>Email<input type="email" name="email" required autocomplete="email"></label>
        <label>Message<textarea name="body" required></textarea></label>
        <button class="btn btn-primary" type="submit">Send via email</button>
      </form>
      <div class="stack reveal d2">
        <img src="/assets/photos/contact-side.webp" alt="Workshop" width="900" height="675" loading="lazy" style="border-radius:10px;width:100%;aspect-ratio:4/3;object-fit:cover">
        <div class="panel"><h3>Brand desks</h3>
          <p><a href="https://www.zieshine.com/contact">ZIESHINE</a><br>
          <a href="https://eleviaapparel.com/">ELEVIA</a><br>
          <a href="https://manlorapparel.com/">MANLOR</a></p>
        </div>
      </div>
    </div></section>
  </main>
  <footer class="site-footer"><div class="wrap footer-grid">
    <div class="footer-meta">© <span id="y"></span> Guangzhou Zito Global Co., Ltd.</div>
    <div class="footer-links"><a href="/about.html">About</a><a href="/privacy.html">Privacy</a></div>
  </div></footer>
  <script>document.getElementById("y").textContent=new Date().getFullYear()</script>
  <script src="/assets/js/site.js"></script>
</body></html>
"""


if __name__ == "__main__":
    main()
