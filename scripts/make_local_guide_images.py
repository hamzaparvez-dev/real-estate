#!/usr/bin/env python3
"""Blog cover images for the November 2026 local guides: centre-cropped 1400x933 JPEGs
made from the project's own photos and renders (no stock images).

    python3 scripts/make_local_guide_images.py
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {
    'prestige-flats-in-kalyan-west': 'prestige-tower-day.jpg',
    'prestige-gold-kalyan-west': 'prestige-gold-night.jpg',
    'prestige-one-kalyan-godrej-hill': 'prestige-one/gallery/tower-daylight.jpg',
    'prestige-enterprises-kalyan': 'prestige-tower-night.jpg',
    '5-bhk-flats-in-kalyan-west': 'prestige-one/who-we-are-interior.jpg',
    '3-bhk-flats-in-kalyan-west': 'prestige-gold/gallery/bedroom.jpg',
    '1-bhk-2-bhk-flats-near-kala-talao-kalyan-west': 'hero-iso-2bhk.jpg',
    'flats-in-khadakpada-kalyan-west': 'prestige-one/gallery/rooftop-garden.webp',
    'new-projects-in-kalyan-west': 'prestige-gold/gallery/main-lobby.jpg',
    'ready-reckoner-rate-in-kalyan': 'hero-plan-1bhk.jpg',
    'how-to-check-maharera-registration-number': 'prestige-gold/gallery/entrance-gate.jpg',
    'upcoming-infrastructure-kalyan-metro-line-5': 'hero-corridor.webp',
    'total-cost-of-buying-a-flat-in-kalyan-west': 'prestige-gold/gallery/kitchen.jpg',
}
W, H = 1400, 933


def cover(src, dst):
    im = Image.open(src).convert('RGB')
    r = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    im.crop((x, y, x + W, y + H)).save(dst, 'JPEG', quality=82, optimize=True, progressive=True)


if __name__ == '__main__':
    for slug, rel in SRC.items():
        dst = os.path.join(ROOT, 'img', 'blog', slug + '.jpg')
        cover(os.path.join(ROOT, 'img', rel), dst)
        print('wrote', os.path.relpath(dst, ROOT), os.path.getsize(dst))
