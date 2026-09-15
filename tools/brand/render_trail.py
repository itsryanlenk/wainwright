"""Render the trail-themed pixel brand assets for the README.

Usage: python tools/brand/render_trail.py "Wainwright" "One job per bot. Checked before it ships." assets
Needs Pillow and a local Chrome or Chromium (set CHROME_PATH if it is not found on PATH).
Fonts (Press Start 2P, VT323) load from Google Fonts, so rendering needs network access.
"""
import html
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

import pixel

HERE = Path(__file__).resolve().parent
CHROME = (os.environ.get("CHROME_PATH") or shutil.which("chrome") or shutil.which("chromium")
          or shutil.which("google-chrome") or r"C:\Program Files\Google\Chrome\Application\chrome.exe")
NAME, TAGLINE, OUTDIR = sys.argv[1], sys.argv[2], Path(sys.argv[3])
OUTDIR.mkdir(parents=True, exist_ok=True)
BUILD = HERE / ".build"
if BUILD.exists():
    shutil.rmtree(BUILD)
BUILD.mkdir()
shutil.copy(HERE / "trail.css", BUILD / "trail.css")
pixel.build_all(BUILD / "pix")


def fill(tpl, **extra):
    t = (HERE / tpl).read_text(encoding="utf-8")
    name, tagline = html.escape(NAME), html.escape(TAGLINE)
    t = t.replace("__UPPER__", name.upper()).replace("__NAME__", name).replace("__TAGLINE__", tagline)
    for k, v in extra.items():
        t = t.replace(f"__{k}__", v)
    return t


def shoot(html, out_png, w, h, scale=2):
    page = BUILD / (Path(out_png).stem + ".html")
    page.write_text(html, encoding="utf-8")
    subprocess.run([
        CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        f"--force-device-scale-factor={scale}", f"--window-size={w},{h}",
        "--virtual-time-budget=10000", f"--screenshot={out_png}", page.as_uri(),
    ], check=True, capture_output=True)


for tpl, out, w, h, scale in [
    ("t-logo.html", "logo.png", 256, 256, 2),
    ("t-banner.html", "banner.png", 1500, 500, 2),
    ("t-social.html", "social-preview.png", 1280, 640, 1),
    ("t-how.html", "how-it-works.png", 1500, 720, 2),
    ("t-anatomy.html", "persona-anatomy.png", 1500, 860, 2),
    ("t-memory.html", "memory-tiers.png", 1500, 700, 2),
]:
    shoot(fill(tpl), OUTDIR / out, w, h, scale)
    print("rendered", out)

frames, durations = [], []
plan = [(1, "strip-0", 2600), (2, "strip-0", 450), (3, "strip-1", 450), (2, "strip-0", 450), (3, "strip-1", 450),
        (4, "strip-0", 3000), (5, "strip-0", 2600), (6, "strip-arrive-0", 450), (6, "strip-arrive-1", 450),
        (6, "strip-arrive-0", 450), (6, "strip-arrive-1", 2200)]
for i, (show, strip, ms) in enumerate(plan):
    png = BUILD / f"lint-{i}.png"
    step = {1: "1", 2: "2", 3: "2", 4: "3", 5: "4", 6: "5"}[show]
    shoot(fill("t-lint.html", FRAME=str(show), STRIP=strip, STEP=step).replace("__STEP__", step), png, 1200, 600, scale=1)
    frames.append(Image.open(png).convert("RGB").quantize(colors=32, method=Image.Quantize.MEDIANCUT))
    durations.append(ms)
frames[0].save(OUTDIR / "lint-demo.gif", save_all=True, append_images=frames[1:], duration=durations, loop=0, optimize=True)
print("rendered lint-demo.gif")
