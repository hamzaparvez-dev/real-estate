#!/usr/bin/env python3
"""Generate every illustration used on the site (original artwork, no stock photos).

    python3 scripts/make_images.py

Scenes are drawn as SVG from small primitives (skyline, hills, fort, temple, train,
viaduct ...) in the brand palette taken from the logo (navy, gold, coral), rendered
with headless Chromium and saved to img/. Images contain NO text so they work for
English, Hindi and Marathi alike. Replace any of them with real photos of your
projects later: just keep the same file name.
"""
import math
import os
import random
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, 'img')

NAVY, NAVY2, GOLD, GOLD2 = '#0A1525', '#0D1A30', '#C9A84C', '#E0C968'
CORAL, COPPER, CREAM = '#D4706F', '#D2693E', '#F7F4EF'

_uid = [0]


def uid():
    _uid[0] += 1
    return f'g{_uid[0]}'


def grad(stops, vertical=True):
    """Return (defs, url) for a linear gradient. stops = [(offset, color[, opacity])]."""
    i = uid()
    xy = 'x1="0" y1="0" x2="0" y2="1"' if vertical else 'x1="0" y1="0" x2="1" y2="0"'
    s = ''.join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a[0]}"' if a else '') + '/>'
                for o, c, *a in stops)
    return f'<linearGradient id="{i}" {xy}>{s}</linearGradient>', f'url(#{i})'


def svg(w, h, body, defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<defs>{defs}</defs>{body}</svg>')


# ------------------------------------------------------------------ primitives

def sky(w, h, stops):
    d, u = grad(stops)
    return d, f'<rect width="{w}" height="{h}" fill="{u}"/>'


def sun(cx, cy, r, color, glow=None):
    out = ''
    if glow:
        i = uid()
        out += (f'<radialGradient id="{i}"><stop offset="0" stop-color="{glow}" stop-opacity=".55"/>'
                f'<stop offset="1" stop-color="{glow}" stop-opacity="0"/></radialGradient>'
                f'<circle cx="{cx}" cy="{cy}" r="{r * 3.2}" fill="url(#{i})"/>')
    return out + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>'


def stars(w, h, n, seed, maxy=0.5):
    r = random.Random(seed)
    return ''.join(f'<circle cx="{r.uniform(0, w):.0f}" cy="{r.uniform(0, h * maxy):.0f}" r="{r.choice([.8, 1.2, 1.6]):.1f}" '
                   f'fill="#fff" opacity="{r.uniform(.25, .9):.2f}"/>' for _ in range(n))


def clouds(w, h, n, seed, color='#fff', op=.18, ymax=0.4):
    r = random.Random(seed)
    out = ''
    for _ in range(n):
        x, y, s = r.uniform(0, w), r.uniform(h * .05, h * ymax), r.uniform(.6, 1.6)
        for dx, dy, rx in [(0, 0, 90), (70, -14, 70), (-70, 8, 60), (130, 10, 50)]:
            out += (f'<ellipse cx="{x + dx * s:.0f}" cy="{y + dy * s:.0f}" rx="{rx * s:.0f}" ry="{22 * s:.0f}" '
                    f'fill="{color}" opacity="{op}"/>')
    return out


def hills(w, base, amp, color, seed, step=24, opacity=1, bottom=None):
    r = random.Random(seed)
    f = [(r.uniform(.003, .009), r.uniform(0, 6.28), r.uniform(.4, 1)) for _ in range(3)]
    pts = []
    x = 0
    while x <= w + step:
        y = base - sum(a * math.sin(k * x + p) for k, p, a in f) * amp / 2
        pts.append(f'{x:.0f},{y:.0f}')
        x += step
    bottom = bottom if bottom is not None else base + amp * 3 + 2000
    return f'<polygon points="0,{bottom} {" ".join(pts)} {w + step},{bottom}" fill="{color}" opacity="{opacity}"/>'


def buildings(x0, x1, base, hmin, hmax, wmin, wmax, fill, seed, win=None, win_p=.45,
              ww=6, wh=9, gx=11, gy=17, tops=True, shade=None):
    r = random.Random(seed)
    out, x = '', x0
    while x < x1:
        bw = r.uniform(wmin, wmax)
        bh = r.uniform(hmin, hmax)
        out += f'<rect x="{x:.0f}" y="{base - bh:.0f}" width="{bw:.0f}" height="{bh + 3:.0f}" fill="{fill}"/>'
        if shade:
            out += f'<rect x="{x + bw * .62:.0f}" y="{base - bh:.0f}" width="{bw * .38:.0f}" height="{bh + 3:.0f}" fill="{shade}"/>'
        if tops:
            t = r.random()
            if t < .22:
                out += f'<rect x="{x + bw / 2 - 1:.0f}" y="{base - bh - r.uniform(14, 40):.0f}" width="2" height="{r.uniform(14, 40):.0f}" fill="{fill}"/>'
            elif t < .42:
                out += f'<rect x="{x + bw * .2:.0f}" y="{base - bh - 8:.0f}" width="{bw * .6:.0f}" height="9" fill="{fill}"/>'
        if win:
            cols = max(1, int((bw - 8) // gx))
            rows = max(1, int((bh - 14) // gy))
            for ry in range(rows):
                for cx in range(cols):
                    if r.random() < win_p:
                        out += (f'<rect x="{x + 6 + cx * gx:.0f}" y="{base - bh + 9 + ry * gy:.0f}" '
                                f'width="{ww}" height="{wh}" fill="{r.choice(win) if isinstance(win, (list, tuple)) else win}"/>')
        x += bw + r.uniform(0, 4)
    return out


def tower(x, base, w, h, fill, win, seed, win_p=.5, ww=7, wh=10, gx=14, gy=20, taper=True):
    """A single detailed residential tower with balconies."""
    r = random.Random(seed)
    out = f'<rect x="{x}" y="{base - h}" width="{w}" height="{h + 2}" fill="{fill}"/>'
    if taper:
        out += f'<rect x="{x + w * .12}" y="{base - h - 18}" width="{w * .76}" height="20" fill="{fill}"/>'
        out += f'<rect x="{x + w / 2 - 1.5}" y="{base - h - 46}" width="3" height="30" fill="{fill}"/>'
    cols, rows = int((w - 10) // gx), int((h - 16) // gy)
    for ry in range(rows):
        out += f'<rect x="{x}" y="{base - h + 14 + ry * gy + wh + 3}" width="{w}" height="2" fill="#000" opacity=".16"/>'
        for cx in range(cols):
            if r.random() < win_p:
                out += f'<rect x="{x + 7 + cx * gx}" y="{base - h + 14 + ry * gy}" width="{ww}" height="{wh}" fill="{win}"/>'
    return out


def water(y, w, h, c1, c2, seed, streak='#fff', n=60):
    d, u = grad([(0, c1), (1, c2)])
    r = random.Random(seed)
    out = f'<rect y="{y}" width="{w}" height="{h - y}" fill="{u}"/>'
    for _ in range(n):
        yy = r.uniform(y + 6, h)
        ln = r.uniform(30, 200) * (1 + (yy - y) / (h - y))
        out += f'<rect x="{r.uniform(-20, w):.0f}" y="{yy:.0f}" width="{ln:.0f}" height="2" rx="1" fill="{streak}" opacity="{r.uniform(.05, .22):.2f}"/>'
    return d, out


def cable_bridge(cx, deck_y, span, pylon_h, color, cable=None):
    cable = cable or color
    out = f'<rect x="{cx - span / 2}" y="{deck_y}" width="{span}" height="9" fill="{color}"/>'
    for px in (cx - span * .22, cx + span * .22):
        out += f'<polygon points="{px - 10},{deck_y + 9} {px - 4},{deck_y - pylon_h} {px + 4},{deck_y - pylon_h} {px + 10},{deck_y + 9}" fill="{color}"/>'
        top = deck_y - pylon_h + 18
        for i in range(1, 15):
            d = i * span * .0155
            for s in (-1, 1):
                out += f'<line x1="{px}" y1="{top + i * 3.4}" x2="{px + s * d:.0f}" y2="{deck_y}" stroke="{cable}" stroke-width="1.3" opacity=".75"/>'
    for k in range(0, int(span), 70):
        out += f'<rect x="{cx - span / 2 + k}" y="{deck_y + 9}" width="6" height="40" fill="{color}"/>'
    return out


def fort(x, base, s, color, light=None):
    """Hill-fort wall with crenellations, two round towers and an arched gate."""
    W = 420 * s
    out = f'<rect x="{x}" y="{base - 120 * s}" width="{W}" height="{120 * s + 3}" fill="{color}"/>'
    n = int(W // (22 * s))
    for i in range(0, n, 2):
        out += f'<rect x="{x + i * 22 * s}" y="{base - 138 * s}" width="{14 * s}" height="{20 * s}" fill="{color}"/>'
    for tx in (x - 20 * s, x + W - 40 * s):
        out += (f'<rect x="{tx}" y="{base - 210 * s}" width="{60 * s}" height="{213 * s}" fill="{color}"/>'
                f'<polygon points="{tx - 6 * s},{base - 210 * s} {tx + 30 * s},{base - 262 * s} {tx + 66 * s},{base - 210 * s}" fill="{color}"/>')
    out += f'<path d="M{x + W / 2 - 34 * s},{base} V{base - 60 * s} a{34 * s},{34 * s} 0 0 1 {68 * s},0 V{base} Z" fill="{light or "#000"}" opacity=".55"/>'
    return out


def temple(x, base, s, color, accent=None):
    """Stone shikhara temple: plinth, mandapa, stepped tower, kalash and flag."""
    out = ''
    for i in range(4):
        out += f'<rect x="{x - (110 - i * 10) * s}" y="{base - (i + 1) * 10 * s}" width="{(220 - i * 20) * s}" height="{10 * s + 1}" fill="{color}"/>'
    bx, by = x - 70 * s, base - 40 * s
    out += f'<rect x="{bx}" y="{by - 70 * s}" width="{140 * s}" height="{70 * s}" fill="{color}"/>'
    out += f'<polygon points="{bx - 10 * s},{by - 70 * s} {x},{by - 112 * s} {bx + 150 * s},{by - 70 * s}" fill="{color}"/>'
    tiers = 9
    for i in range(tiers):
        tw = (96 - i * 9) * s
        th = 20 * s
        out += f'<rect x="{x - tw / 2}" y="{by - 112 * s - th - i * th * .86}" width="{tw}" height="{th + 1}" fill="{color}"/>'
    topy = by - 112 * s - 20 * s - (tiers - 1) * 20 * s * .86 - 6 * s
    out += f'<ellipse cx="{x}" cy="{topy}" rx="{10 * s}" ry="{8 * s}" fill="{color}"/><rect x="{x - 1.5 * s}" y="{topy - 34 * s}" width="{3 * s}" height="{30 * s}" fill="{color}"/>'
    out += f'<polygon points="{x + 1.5 * s},{topy - 34 * s} {x + 24 * s},{topy - 27 * s} {x + 1.5 * s},{topy - 20 * s}" fill="{accent or CORAL}"/>'
    out += f'<path d="M{x - 18 * s},{by} V{by - 28 * s} a{18 * s},{18 * s} 0 0 1 {36 * s},0 V{by} Z" fill="#000" opacity=".5"/>'
    return out


def train(x, y, n, s, body, stripe, win='#FFE9A8', dir=1):
    out = ''
    cw = 150 * s
    for i in range(n):
        cx = x + i * (cw + 5 * s) * dir
        out += f'<rect x="{cx}" y="{y - 46 * s}" width="{cw}" height="{46 * s}" rx="{5 * s}" fill="{body}"/>'
        out += f'<rect x="{cx}" y="{y - 16 * s}" width="{cw}" height="{5 * s}" fill="{stripe}"/>'
        for k in range(5):
            out += f'<rect x="{cx + 10 * s + k * 28 * s}" y="{y - 38 * s}" width="{18 * s}" height="{14 * s}" rx="2" fill="{win}" opacity=".92"/>'
    return out


def viaduct(w, y, color, pier_h, step=260, deck=14):
    out = f'<rect y="{y}" width="{w}" height="{deck}" fill="{color}"/>'
    for px in range(120, w, step):
        out += f'<rect x="{px}" y="{y + deck}" width="26" height="{pier_h}" fill="{color}"/><polygon points="{px - 34},{y + deck} {px + 60},{y + deck} {px + 26},{y + deck + 22} {px},{y + deck + 22}" fill="{color}"/>'
    return out


def tree(x, base, h, color, color2=None):
    out = f'<rect x="{x - 2}" y="{base - h * .45}" width="4" height="{h * .45}" fill="#2a1a12"/>'
    for dx, dy, r in [(0, -.62, .34), (-.2, -.5, .26), (.2, -.5, .26), (0, -.8, .24)]:
        out += f'<circle cx="{x + dx * h:.0f}" cy="{base + dy * h:.0f}" r="{r * h:.0f}" fill="{color}"/>'
    if color2:
        out += f'<circle cx="{x + h * .1:.0f}" cy="{base - h * .7:.0f}" r="{h * .16:.0f}" fill="{color2}" opacity=".5"/>'
    return out


def palm(x, base, h, color):
    out = f'<path d="M{x},{base} Q{x + h * .08},{base - h * .5} {x + h * .03},{base - h}" stroke="#3a2a1a" stroke-width="5" fill="none"/>'
    for a in range(-70, 90, 28):
        rad = math.radians(a)
        out += f'<path d="M{x + h * .03},{base - h} q{math.sin(rad) * h * .3:.0f},{-h * .12:.0f} {math.sin(rad) * h * .42:.0f},{h * .1 + abs(a) * .3:.0f}" stroke="{color}" stroke-width="5" fill="none" stroke-linecap="round"/>'
    return out


def crane(x, base, h, color):
    out = f'<rect x="{x}" y="{base - h}" width="8" height="{h}" fill="{color}"/>'
    for i in range(0, int(h), 20):
        out += f'<line x1="{x}" y1="{base - i}" x2="{x + 8}" y2="{base - i - 20}" stroke="{color}" stroke-width="2"/>'
    out += f'<rect x="{x - 130}" y="{base - h}" width="270" height="7" fill="{color}"/><rect x="{x - 150}" y="{base - h - 4}" width="20" height="16" fill="{color}"/>'
    out += f'<line x1="{x + 4}" y1="{base - h - 26}" x2="{x + 120}" y2="{base - h}" stroke="{color}" stroke-width="1.5"/><line x1="{x + 100}" y1="{base - h + 7}" x2="{x + 100}" y2="{base - h + 70}" stroke="{color}" stroke-width="1.5"/>'
    out += f'<rect x="{x + 90}" y="{base - h + 70}" width="22" height="12" fill="{CORAL}"/>'
    return out


def warehouse(x, base, w, h, color, door, seed):
    out = f'<rect x="{x}" y="{base - h}" width="{w}" height="{h + 2}" fill="{color}"/>'
    out += f'<polygon points="{x - 6},{base - h} {x + w / 2},{base - h - 16} {x + w + 6},{base - h}" fill="{color}"/>'
    for i in range(int(w // 60)):
        out += f'<rect x="{x + 14 + i * 60}" y="{base - h * .62}" width="40" height="{h * .62}" fill="{door}"/>'
        for k in range(5):
            out += f'<rect x="{x + 14 + i * 60}" y="{base - h * .62 + k * h * .12}" width="40" height="1.5" fill="#000" opacity=".25"/>'
    return out


def truck(x, base, s, cab, box):
    return (f'<rect x="{x}" y="{base - 52 * s}" width="{96 * s}" height="{44 * s}" fill="{box}"/>'
            f'<path d="M{x + 98 * s},{base - 8 * s} V{base - 40 * s} h{20 * s} l{14 * s},{14 * s} V{base - 8 * s} Z" fill="{cab}"/>'
            f'<circle cx="{x + 22 * s}" cy="{base - 6 * s}" r="{9 * s}" fill="#111"/><circle cx="{x + 74 * s}" cy="{base - 6 * s}" r="{9 * s}" fill="#111"/><circle cx="{x + 120 * s}" cy="{base - 6 * s}" r="{9 * s}" fill="#111"/>')


def birds(w, h, n, seed, color='#fff', op=.6):
    r = random.Random(seed)
    out = ''
    for _ in range(n):
        x, y, s = r.uniform(w * .3, w * .95), r.uniform(h * .08, h * .32), r.uniform(.7, 1.4)
        out += f'<path d="M{x:.0f},{y:.0f} q{8 * s:.0f},{-9 * s:.0f} {16 * s:.0f},0 q{8 * s:.0f},{-9 * s:.0f} {16 * s:.0f},0" stroke="{color}" stroke-width="2" fill="none" opacity="{op}"/>'
    return out


def mist(w, y, color, seed, n=5, op=.16):
    r = random.Random(seed)
    return ''.join(f'<ellipse cx="{r.uniform(0, w):.0f}" cy="{y + r.uniform(-30, 40):.0f}" rx="{r.uniform(220, 520):.0f}" ry="{r.uniform(16, 34):.0f}" fill="{color}" opacity="{op}"/>' for _ in range(n))


# ------------------------------------------------------------------ icons (for blog covers)
# every icon is drawn in a 200x200 box, stroke style, centre (100,100)

def icon(name, c=GOLD2, a=CORAL):
    s = f'stroke="{c}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    fa = f'fill="{a}"'
    shapes = {
        'key': f'<circle cx="62" cy="100" r="34" {s}/><circle cx="62" cy="100" r="10" {fa}/><path d="M96 100 H178 M150 100 v26 M168 100 v18" {s}/>',
        'doc': f'<path d="M50 20 H120 L156 56 V180 H50 Z" {s}/><path d="M120 20 V56 H156" {s}/><path d="M70 90 H136 M70 116 H136 M70 142 H110" {s}/><circle cx="132" cy="150" r="22" {fa} opacity=".9"/><path d="M122 150 l8 8 14 -16" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
        'shield': f'<path d="M100 18 L168 44 V100 C168 142 138 168 100 184 C62 168 32 142 32 100 V44 Z" {s}/><path d="M68 100 l24 24 42 -50" stroke="{a}" stroke-width="11" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
        'rupee': f'<circle cx="100" cy="100" r="76" {s}/><path d="M68 66 H132 M68 90 H132 M84 66 C130 66 130 118 84 118 L132 160" {s}/>',
        'calc': f'<rect x="46" y="22" width="108" height="156" rx="14" {s}/><rect x="62" y="38" width="76" height="34" rx="4" {fa} opacity=".85"/><g fill="{c}"><circle cx="70" cy="100" r="7"/><circle cx="100" cy="100" r="7"/><circle cx="130" cy="100" r="7"/><circle cx="70" cy="130" r="7"/><circle cx="100" cy="130" r="7"/><circle cx="130" cy="130" r="7"/><circle cx="70" cy="158" r="7"/><circle cx="100" cy="158" r="7"/><circle cx="130" cy="158" r="7"/></g>',
        'house': f'<path d="M24 98 L100 30 L176 98" {s}/><path d="M46 84 V172 H154 V84" {s}/><rect x="84" y="118" width="32" height="54" {fa} opacity=".9"/><rect x="58" y="100" width="20" height="20" {s}/>',
        'chart': f'<path d="M30 30 V168 H178" {s}/><path d="M50 140 L84 104 L112 124 L168 56" stroke="{a}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M142 56 H168 V82" stroke="{a}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
        'globe': f'<circle cx="100" cy="100" r="76" {s}/><ellipse cx="100" cy="100" rx="32" ry="76" {s}/><path d="M26 100 H174 M38 66 H162 M38 134 H162" {s}/>',
        'scale': f'<path d="M100 28 V168 M60 168 H140 M40 62 H160" {s}/><path d="M40 62 L18 118 H62 Z M160 62 L138 118 H182 Z" {s}/><path d="M18 118 a22 14 0 0 0 44 0 M138 118 a22 14 0 0 0 44 0" {s}/>',
        'crane': f'<path d="M60 176 V40 M60 40 H176 M60 40 L30 60 M60 70 L90 40 M60 100 L120 40" {s}/><path d="M150 40 V108" {s}/><rect x="132" y="108" width="36" height="22" {fa}/>',
        'percent': f'<path d="M152 40 L48 160" {s}/><circle cx="62" cy="60" r="22" {s}/><circle cx="138" cy="140" r="22" {s}/>',
        'pin': f'<path d="M100 184 C60 136 44 112 44 80 a56 56 0 0 1 112 0 C156 112 140 136 100 184 Z" {s}/><circle cx="100" cy="80" r="20" {fa}/>',
        'hand': f'<path d="M24 110 L62 72 L100 90 L140 62 L178 100" {s}/><path d="M62 72 V150 M100 90 V160 M140 62 V150 M24 110 V150 H178 V100" {s}/>',
        'train': f'<rect x="48" y="30" width="104" height="116" rx="18" {s}/><rect x="64" y="50" width="72" height="40" rx="6" {fa} opacity=".85"/><circle cx="76" cy="120" r="8" fill="{c}"/><circle cx="124" cy="120" r="8" fill="{c}"/><path d="M70 146 L52 178 M130 146 L148 178 M60 178 H140" {s}/>',
    }
    return f'<g>{shapes[name]}</g>'


# ------------------------------------------------------------------ scenes

def scene_hero_mumbai(w=1920, h=1080):
    d1, bg = sky(w, h, [(0, '#0E1B3A'), (.45, '#5B4A7A'), (.72, '#E08A5E'), (1, '#F6C27A')])
    d2, wat = water(int(h * .72), w, h, '#3A3A66', '#0B1428', 3, '#FFD9A0', 90)
    b = stars(w, h, 70, 1, .35) + sun(int(w * .72), int(h * .66), 70, '#FFE2A8', '#FFB36B')
    b += clouds(w, h, 4, 2, '#FFD7B0', .13)
    b += hills(w, int(h * .72), 30, '#2A2F55', 5, opacity=.8)
    b += buildings(int(w * .38), w, int(h * .72), 120, 420, 30, 70, '#1A2147', 11, ['#FFD98E', '#FFC46B'], .34, shade='#141A3A')
    b += buildings(int(w * .45), w, int(h * .72), 60, 210, 26, 56, '#222B56', 12, ['#FFD98E'], .25)
    b += cable_bridge(int(w * .26), int(h * .715), int(w * .5), 230, '#141A3A', '#2a2f5a')
    b += birds(w, h, 5, 4, '#fff', .5)
    return svg(w, h, bg + wat + b, d1 + d2)


def scene_hero_kalyan(w=1920, h=1080):
    d1, bg = sky(w, h, [(0, '#2B3A67'), (.5, '#C98C8C'), (.8, '#F4C98F'), (1, '#FBE3B4')])
    d2, wat = water(int(h * .8), w, h, '#E3A98B', '#4A4F7A', 7, '#fff', 60)
    b = sun(int(w * .62), int(h * .6), 60, '#FFF2C8', '#FFD08A') + clouds(w, h, 5, 3, '#fff', .2)
    b += hills(w, int(h * .62), 120, '#6C6A91', 1, opacity=.75) + hills(w, int(h * .7), 90, '#4B4C76', 2)
    b += fort(int(w * .5), int(h * .63), 1.35 * (h / 1080) * (1.25 if h < 800 else 1), '#34385F', '#F4C98F')
    b += hills(w, int(h * .8), 40, '#2A2D52', 4)
    b += buildings(int(w * .34), w, int(h * .8), 80, 300, 28, 62, '#202549', 21, ['#FFE3A2'], .22, shade='#1A1E3F')
    b += f'<rect y="{h * .765}" width="{w}" height="10" fill="#1B1F40"/>' + train(int(w * .12), int(h * .765), 6, 1.2, '#E9E3F5', CORAL)
    b += ''.join(tree(x, int(h * .8), r, '#1F4A3C') for x, r in [(60, 120), (190, 90), (1730, 110), (1850, 140)])
    b += birds(w, h, 6, 8, '#2A2D52', .7)
    return svg(w, h, bg + wat + b, d1 + d2)


def scene_hero_towers(w=1920, h=1080):
    d1, bg = sky(w, h, [(0, '#050B18'), (.6, '#10224A'), (1, '#2B4678')])
    b = stars(w, h, 140, 9, .55) + sun(int(w * .84), int(h * .16), 44, '#F4F1E4', '#9FB6E8')
    b += buildings(0, w, int(h * .86), 140, 420, 40, 90, '#0B1530', 31, ['#FFD98E', '#E9C46A'], .22)
    for i, (x, hh, ww) in enumerate([(w * .52, 560, 130), (w * .66, 700, 150), (w * .8, 520, 120), (w * .92, 640, 110)]):
        b += tower(int(x), int(h * .9), ww, hh, '#122046', '#FFD98E', 40 + i, .5, taper=True)
    b += crane(int(w * .6), int(h * .9) - 700, 150, '#0A1226')
    b += f'<rect y="{h * .9}" width="{w}" height="{h * .1}" fill="#050B18"/>'
    b += ''.join(tree(x, int(h * .9), 80, '#0F3A32') for x in range(40, w, 190))
    return svg(w, h, bg + b, d1)


def scene_hero_township(w=1920, h=1080):
    d1, bg = sky(w, h, [(0, '#7FB2E5'), (.55, '#D5E9F5'), (1, '#FCEBC9')])
    b = sun(int(w * .8), int(h * .22), 56, '#FFF6D8', '#FFE7A8') + clouds(w, h, 6, 4, '#fff', .55, .35)
    b += hills(w, int(h * .55), 150, '#8EB1C9', 1, opacity=.8) + hills(w, int(h * .62), 120, '#6C9A8A', 2) + hills(w, int(h * .72), 80, '#3F7A5F', 3)
    d2, lake = water(int(h * .8), w, h, '#7FB6D4', '#3A7C9C', 5, '#fff', 40)
    b += lake
    base = int(h * .8)
    for i, (x, hh, ww) in enumerate([(w * .46, 420, 120), (w * .58, 560, 140), (w * .7, 360, 110), (w * .82, 500, 130)]):
        b += tower(int(x), base, ww, hh, '#F1E9DA' if i % 2 else '#E6D6BC', '#6FA0C8', 50 + i, .55)
    b += buildings(int(w * .4), w, base, 50, 120, 50, 90, '#CDB690', 15, '#6FA0C8', .3)
    b += ''.join(tree(x, base + 6, r, '#2E7D4F', '#9AD08A') for x, r in [(30, 190), (150, 150), (290, 220), (420, 140), (1680, 160), (1810, 210)])
    b += ''.join(palm(x, base + 14, 200, '#2E7D4F') for x in (610, 1560))
    b += birds(w, h, 7, 9, '#37506B', .7)
    return svg(w, h, bg + b, d1 + d2)


def scene_hero_corridor(w=1920, h=1080):
    d1, bg = sky(w, h, [(0, '#25305E'), (.5, '#B3597A'), (.78, '#F39A63'), (1, '#FFD08A')])
    b = sun(int(w * .66), int(h * .55), 90, '#FFE9B0', '#FFAE6B') + clouds(w, h, 5, 6, '#FFD1A0', .2)
    b += hills(w, int(h * .62), 80, '#5A4577', 1, opacity=.8)
    b += buildings(0, w, int(h * .84), 150, 520, 40, 90, '#2A2150', 61, ['#FFE3A2'], .2, shade='#221A44')
    b += f'<rect y="{h * .84}" width="{w}" height="{h * .16}" fill="#171233"/>'
    y = int(h * .66)
    b += viaduct(w, y, '#120E2B', int(h * .84) - y - 14, 300, 16)
    b += train(int(w * .28), y, 5, 1.5, '#F6E9D2', CORAL, '#FFE3A2')
    b += ''.join(tree(x, int(h * .86), 90, '#15402F') for x in range(30, w, 230))
    b += birds(w, h, 5, 2, '#fff', .45)
    return svg(w, h, bg + b, d1)


# ---- city covers (1200x630)

def city_scene(slug, w=1200, h=630):
    S = {
        'kalyan': lambda: scene_hero_kalyan(w, h),
        'mumbai': lambda: scene_hero_mumbai(w, h),
        'dombivli': lambda: _dombivli(w, h),
        'thane': lambda: _thane(w, h),
        'ulhasnagar': lambda: _ulhasnagar(w, h),
        'ambernath': lambda: _ambernath(w, h),
        'badlapur': lambda: _badlapur(w, h),
        'bhiwandi': lambda: _bhiwandi(w, h),
        'navi-mumbai': lambda: _navi(w, h),
        'panvel': lambda: _panvel(w, h),
    }
    return S[slug]()


def _dombivli(w, h):
    d1, bg = sky(w, h, [(0, '#1F4E79'), (.5, '#E58F65'), (1, '#FFD9A0')])
    b = sun(int(w * .18), int(h * .6), 52, '#FFF0C8', '#FFC48A') + clouds(w, h, 4, 5, '#FFD9B0', .25) + birds(w, h, 5, 6, '#2B2A55', .6)
    b += hills(w, int(h * .6), 60, '#6B5C8E', 2, opacity=.7)
    base = int(h * .74)
    b += buildings(0, w, base, 60, 170, 40, 80, '#2B2A55', 17, ['#FFE3A2'], .25)
    for i, (x, hh, ww) in enumerate([(.36, 340, 88), (.48, 420, 98), (.6, 300, 82), (.72, 380, 92), (.84, 270, 76)]):
        b += tower(int(w * x), base, ww, hh, '#3A3563' if i % 2 else '#2F2B58', '#FFE3A2', 120 + i, .42, ww=5, wh=8, gx=11, gy=16)
    b += temple(int(w * .17), base, .62, '#241F4A', CORAL)
    b += f'<rect y="{base}" width="{w}" height="{h - base}" fill="#1A1636"/>'
    b += f'<rect y="{base + 66}" width="{w}" height="4" fill="#8F86B5"/><rect y="{base + 96}" width="{w}" height="4" fill="#8F86B5"/>'
    b += train(int(w * .08), base + 64, 5, 1.2, '#F6E9D2', CORAL)
    b += ''.join(f'<rect x="{x}" y="{base - 150}" width="5" height="{h - base + 150}" fill="#120F2B"/><rect x="{x - 24}" y="{base - 150}" width="53" height="4" fill="#120F2B"/>' for x in range(60, w, 240))
    b += f'<path d="M0,{base - 130} Q{w / 2},{base - 96} {w},{base - 130}" stroke="#120F2B" stroke-width="2" fill="none"/>'
    return svg(w, h, bg + b, d1)


def _thane(w, h):
    d1, bg = sky(w, h, [(0, '#5E96D3'), (.6, '#BFDDF2'), (1, '#FDEBC8')])
    b = sun(int(w * .2), int(h * .2), 38, '#FFF6D8', '#FFE7A8') + clouds(w, h, 5, 9, '#fff', .6, .35)
    b += hills(w, int(h * .52), 100, '#7FA6C4', 2, opacity=.85) + hills(w, int(h * .6), 70, '#4E8A74', 3)
    d2, lake = water(int(h * .74), w, h, '#6EB0D2', '#2F6F92', 6, '#fff', 40)
    b += lake
    base = int(h * .74)
    for i, (x, hh, ww) in enumerate([(.5, 260, 80), (.6, 340, 92), (.7, 230, 74), (.8, 300, 86), (.9, 210, 70)]):
        b += tower(int(w * x), base, ww, hh, '#F1E9DA' if i % 2 else '#E3D2B6', '#5F93BF', 70 + i, .5, ww=5, wh=8, gx=11, gy=16)
    b += ''.join(tree(x, base + 4, r, '#2E7D4F', '#9AD08A') for x, r in [(30, 130), (110, 100), (230, 140), (400, 90)])
    b += ''.join(f'<path d="M{x},{h * .82} h60 l-10 14 h-40 z" fill="#C9A84C" opacity=".9"/><line x1="{x + 30}" y1="{h * .82}" x2="{x + 30}" y2="{h * .82 - 40}" stroke="#7A5C20" stroke-width="2"/><path d="M{x + 30},{h * .82 - 40} l26 18 h-26 z" fill="{CORAL}"/>' for x in (180, 330))
    return svg(w, h, bg + b, d1 + d2)


def _ulhasnagar(w, h):
    d1, bg = sky(w, h, [(0, '#F2B66B'), (.6, '#F8D79E'), (1, '#FDEED0')])
    b = sun(int(w * .8), int(h * .22), 50, '#FFF3CF', '#FFD58A') + clouds(w, h, 3, 4, '#fff', .5, .3)
    base = int(h * .84)
    cols = ['#E98E6B', '#D4706F', '#F0C06B', '#C9A84C', '#B9573E', '#E6A37B']
    r = random.Random(5)
    x = -20
    while x < w:
        bw, bh = r.uniform(80, 130), r.uniform(150, 330)
        c = r.choice(cols)
        b += f'<rect x="{x:.0f}" y="{base - bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{c}"/><rect x="{x:.0f}" y="{base - bh:.0f}" width="{bw:.0f}" height="8" fill="#000" opacity=".18"/>'
        for ry in range(int((bh - 40) // 44)):
            for cx in range(int((bw - 14) // 26)):
                b += f'<rect x="{x + 10 + cx * 26:.0f}" y="{base - bh + 24 + ry * 44:.0f}" width="16" height="22" fill="#6A3C2E" opacity=".75"/><rect x="{x + 6 + cx * 26:.0f}" y="{base - bh + 48 + ry * 44:.0f}" width="24" height="3" fill="#000" opacity=".2"/>'
        x += bw + r.uniform(2, 10)
    b += f'<rect y="{base}" width="{w}" height="{h - base}" fill="#5A4A52"/>'
    for i, xx in enumerate(range(0, w, 110)):  # market awnings
        b += f'<path d="M{xx},{base - 36} h100 l-8 -22 h-84 z" fill="{[CORAL, GOLD, "#fff", "#5FA37E"][i % 4]}"/>'
    b += f'<path d="M0,{h * .3} Q{w / 2},{h * .42} {w},{h * .3}" stroke="#7A4B2A" stroke-width="2" fill="none"/>'
    b += ''.join(f'<polygon points="{x},{h * .33 + math.sin(x / 80) * 8:.0f} {x + 18},{h * .33 + math.sin(x / 80) * 8:.0f} {x + 9},{h * .33 + 26 + math.sin(x / 80) * 8:.0f}" fill="{[CORAL, GOLD, "#fff"][i % 3]}"/>' for i, x in enumerate(range(30, w, 46)))
    return svg(w, h, bg + b, d1)


def _ambernath(w, h):
    d1, bg = sky(w, h, [(0, '#2D3B6B'), (.5, '#E9A88B'), (1, '#FCE3B0')])
    b = sun(int(w * .3), int(h * .55), 62, '#FFF1C6', '#FFC987') + clouds(w, h, 4, 3, '#fff', .22) + birds(w, h, 6, 4, '#2A2D52', .7)
    b += hills(w, int(h * .56), 90, '#7A6C96', 1, opacity=.8) + hills(w, int(h * .68), 70, '#4E4A78', 2)
    base = int(h * .84)
    b += hills(w, base - 10, 22, '#2A2D52', 9)
    b += temple(int(w * .62), base, 1.12, '#2B2E55', '#F4C98F')
    b += ''.join(tree(x, base, r, '#1B3A33') for x, r in [(60, 150), (180, 110), (320, 160), (980, 130), (1090, 170), (1160, 120)])
    b += f'<rect y="{base}" width="{w}" height="{h - base}" fill="#1D2046"/>'
    return svg(w, h, bg + b, d1)


def _badlapur(w, h):
    d1, bg = sky(w, h, [(0, '#8FB8C8'), (.6, '#CFE3DA'), (1, '#EFF3DC')])
    b = clouds(w, h, 6, 8, '#fff', .55, .3)
    b += hills(w, int(h * .42), 120, '#8DB2A0', 1, opacity=.8) + mist(w, int(h * .5), '#fff', 2, 5, .35)
    b += hills(w, int(h * .55), 100, '#5D9279', 2) + mist(w, int(h * .62), '#fff', 3, 4, .28)
    b += hills(w, int(h * .68), 70, '#3C7A5C', 4)
    d2, rv = water(int(h * .8), w, h, '#6FA7B3', '#376F7F', 7, '#fff', 40)
    b += rv
    base = int(h * .8)
    b += ''.join(f'<rect x="{x}" y="{base - 46}" width="54" height="46" fill="#F1E9DA"/><polygon points="{x - 6},{base - 46} {x + 27},{base - 76} {x + 60},{base - 46}" fill="{CORAL}"/><rect x="{x + 20}" y="{base - 24}" width="14" height="24" fill="#7A5C3A"/>' for x in (120, 260, 880, 1010))
    b += ''.join(tree(x, base + 4, r, '#2A6B4A', '#8CC78A') for x, r in [(60, 130), (200, 100), (350, 120), (800, 110), (950, 140), (1100, 120), (1160, 170)])
    b += f'<path d="M{w * .55},{h * .62} L{w * .72},{h * .62} L{w * .7},{h * .8} L{w * .57},{h * .8} Z" fill="#C9D8D2" opacity=".45"/>'
    return svg(w, h, bg + b, d1 + d2)


def _bhiwandi(w, h):
    d1, bg = sky(w, h, [(0, '#3B3F73'), (.55, '#D9728A'), (.85, '#F6B26B'), (1, '#FFD98E')])
    b = sun(int(w * .78), int(h * .6), 70, '#FFE9B0', '#FFAE6B') + clouds(w, h, 4, 2, '#FFD1A0', .2)
    b += hills(w, int(h * .66), 50, '#5A4577', 2, opacity=.85)
    base = int(h * .8)
    for i, (x, ww, hh) in enumerate([(30, 300, 130), (360, 360, 150), (760, 300, 120), (1090, 200, 140)]):
        b += warehouse(x, base, ww, hh, '#2A2150' if i % 2 else '#352A63', '#4B3C85', 5 + i)
    b += f'<rect y="{base}" width="{w}" height="{h - base}" fill="#171233"/>'
    b += ''.join(f'<rect x="{x}" y="{base + 34}" width="60" height="4" fill="{GOLD}" opacity=".7"/>' for x in range(0, w, 130))
    b += truck(120, base + 28, 1.2, CORAL, '#E9E3F5') + truck(640, base + 28, 1.0, GOLD, '#F6E9D2') + truck(980, base + 28, 1.3, '#5FA3C9', '#E9E3F5')
    b += ''.join(f'<line x1="{x}" y1="{base + 4}" x2="{x}" y2="{base - 120}" stroke="#171233" stroke-width="4"/><circle cx="{x}" cy="{base - 124}" r="6" fill="#FFE3A2"/>' for x in (330, 740, 1060))
    return svg(w, h, bg + b, d1)


def _navi(w, h):
    d1, bg = sky(w, h, [(0, '#07112A'), (.55, '#1D3C7A'), (1, '#6E8FCB')])
    b = stars(w, h, 80, 3, .5) + sun(int(w * .84), int(h * .18), 34, '#F4F1E4', '#9FB6E8')
    base = int(h * .8)
    d2, wat = water(base, w, h, '#2A4C86', '#0B1B3C', 6, '#FFE3A2', 50)
    b += hills(w, int(h * .6), 50, '#16295A', 1, opacity=.8)
    for i in range(14):  # planned grid of towers
        x = 30 + i * 84
        hh = 120 + ((i * 53) % 7) * 36
        b += tower(x, base, 62, hh, '#0F2150', '#FFD98E', 90 + i, .45, ww=5, wh=7, gx=10, gy=15, taper=False)
    b += f'<path d="M{w * .05},{base - 6} Q{w * .3},{base - 130} {w * .55},{base - 6}" stroke="{GOLD2}" stroke-width="6" fill="none"/><path d="M{w * .08},{base - 6} Q{w * .3},{base - 100} {w * .5},{base - 6}" stroke="{CORAL}" stroke-width="3" fill="none"/>'
    b += f'<rect y="{base}" width="{w}" height="4" fill="#3C5FA8"/>'
    return svg(w, h, bg + wat + b, d1 + d2)


def _panvel(w, h):
    d1, bg = sky(w, h, [(0, '#1B2A4A'), (.5, '#8E5B7A'), (.8, '#F2A65A'), (1, '#FBD08A')])
    b = sun(int(w * .25), int(h * .62), 58, '#FFE6B0', '#FFB36B') + clouds(w, h, 4, 7, '#FFD7B0', .16)
    b += hills(w, int(h * .55), 110, '#6A4D78', 1, opacity=.85) + hills(w, int(h * .65), 70, '#43366A', 2)
    d2, cr = water(int(h * .78), w, h, '#C98A7A', '#2E2A55', 4, '#FFE3A2', 50)
    b += cr
    base = int(h * .78)
    b += buildings(int(w * .5), w, base, 100, 280, 28, 60, '#221C4A', 22, ['#FFE3A2'], .22)
    y = int(h * .64)
    b += viaduct(int(w * .62), y, '#171233', base - y - 14, 220, 12) + train(int(w * .06), y, 4, 1.05, '#F6E9D2', CORAL)
    b += ''.join(tree(x, base + 6, r, '#1B3A33') for x, r in [(30, 110), (120, 90), (240, 120)])
    b += birds(w, h, 4, 3, '#2A2D52', .6)
    return svg(w, h, bg + b, d1 + d2)


# ---- blog covers (1200x630): gradient + skyline + big icon

BLOG_STYLES = {
    # slug: (icon, gradient stops, accent)
    'how-to-buy-a-flat-in-kalyan-dombivli': ('key', ['#0A1525', '#1E3A66'], CORAL),
    'stamp-duty-registration-charges-maharashtra': ('doc', ['#2A1B3D', '#6B3A5C'], GOLD2),
    'check-rera-registration-before-you-buy': ('shield', ['#0B2A2E', '#1F5B5B'], GOLD2),
    'home-loan-eligibility-emi-guide': ('calc', ['#12203F', '#35508C'], GOLD2),
    'under-construction-vs-ready-to-move': ('crane', ['#3A1F15', '#A4512D'], GOLD2),
    'documents-to-check-before-buying-property': ('doc', ['#0A1525', '#2B3F66'], CORAL),
    'buying-a-resale-flat-checklist': ('house', ['#2C1B2F', '#7B3F57'], GOLD2),
    'ready-reckoner-rate-explained': ('percent', ['#0F2A3A', '#1F6177'], GOLD2),
    'rent-or-buy-in-mumbai-metropolitan-region': ('scale', ['#1B1E3F', '#4C4A8C'], GOLD2),
    'capital-gains-tax-on-property-sale': ('rupee', ['#31200F', '#8B5A1E'], '#FFF3C4'),
    'property-investment-kalyan-corridor': ('train', ['#0A1525', '#254A7A'], CORAL),
    'nri-buying-property-in-maharashtra': ('globe', ['#10283A', '#2F6A8E'], GOLD2),
}


def blog_scene(slug, w=1200, h=630):
    ic, (c1, c2), acc = BLOG_STYLES[slug]
    seed = sum(map(ord, slug))
    d1, bg = sky(w, h, [(0, c1), (1, c2)])
    b = stars(w, h, 30, seed, .6)
    b += f'<circle cx="{w * .76}" cy="{h * .42}" r="205" fill="#fff" opacity=".05"/><circle cx="{w * .76}" cy="{h * .42}" r="150" fill="#fff" opacity=".06"/>'
    b += f'<circle cx="{w * .76}" cy="{h * .42}" r="132" fill="none" stroke="{GOLD}" stroke-width="2" stroke-dasharray="3 9" opacity=".8"/>'
    b += f'<g transform="translate({w * .76 - 120},{h * .42 - 120}) scale(1.2)">{icon(ic, "#FAF6F0", acc)}</g>'
    b += buildings(0, w, h, 70, 230, 34, 80, '#000', seed, None, tops=True)
    b = b.replace('fill="#000"', 'fill="#000" fill-opacity=".30"')
    b += tower(70, h, 110, 330, '#000', GOLD2, seed, .4, taper=True).replace('fill="#000"', 'fill="#000" fill-opacity=".34"')
    b += f'<rect y="{h - 6}" width="{w}" height="6" fill="{GOLD}"/>'
    return svg(w, h, bg + b, d1)


# ---- property-type cards (900x1200) + about

def prop_scene(kind, w=900, h=1200):
    S = {
        'apartments': (['#0A1525', '#2B4678'], lambda: ''.join(tower(40 + i * 215, h - 60, 190, 700 - ((i * 37) % 4) * 90, '#F1E9DA' if i % 2 else '#E6D6BC', '#4C7CB0', 200 + i, .6, ww=11, wh=14, gx=22, gy=30) for i in range(4))),
        'villas': (['#7FB2E5', '#FCEBC9'], lambda: _villas(w, h)),
        'plots': (['#F2B66B', '#FDEED0'], lambda: _plots(w, h)),
        'commercial': (['#12203F', '#4C6AA0'], lambda: _commercial(w, h)),
        'rentals': (['#2C1B2F', '#C9715F'], lambda: _rentals(w, h)),
        'redevelopment': (['#3A1F15', '#E39A5E'], lambda: _redev(w, h)),
    }
    c, fn = S[kind]
    d1, bg = sky(w, h, [(0, c[0]), (1, c[1])])
    b = stars(w, h, 40, 5, .4) if kind in ('apartments', 'commercial', 'rentals') else clouds(w, h, 3, 4, '#fff', .45, .3)
    b += fn()
    return svg(w, h, bg + b, d1)


def _villas(w, h):
    base = h - 150
    b = hills(w, int(h * .55), 120, '#8EB1C9', 1, opacity=.8) + hills(w, int(h * .66), 80, '#4E8A74', 2)
    b += f'<rect y="{base}" width="{w}" height="{h - base}" fill="#5C9A62"/><rect y="{base + 60}" width="{w}" height="46" fill="#C9B79A"/>'
    for i, x in enumerate((70, 360, 640)):
        c = ['#F1E9DA', '#E8CBA8', '#F4D9D0'][i]
        b += f'<rect x="{x}" y="{base - 190}" width="200" height="190" fill="{c}"/><polygon points="{x - 18},{base - 190} {x + 100},{base - 290} {x + 218},{base - 190}" fill="{[CORAL, COPPER, "#8A5A44"][i]}"/>'
        b += f'<rect x="{x + 78}" y="{base - 110}" width="44" height="110" fill="#7A5C3A"/><rect x="{x + 22}" y="{base - 150}" width="40" height="46" fill="#6FA0C8"/><rect x="{x + 138}" y="{base - 150}" width="40" height="46" fill="#6FA0C8"/>'
    b += ''.join(tree(x, base + 20, r, '#2E7D4F', '#9AD08A') for x, r in [(20, 200), (300, 150), (580, 160), (860, 210)])
    return b


def _plots(w, h):
    base = int(h * .52)
    b = hills(w, base - 40, 90, '#B58E5A', 1, opacity=.55) + hills(w, base + 20, 60, '#7BA05B', 2)
    b += f'<polygon points="0,{h} {w},{h} {w},{base + 90} 0,{base + 90}" fill="#8DB66A"/>'
    for i in range(6):  # survey grid lines in perspective
        x = -300 + i * 300
        b += f'<line x1="{x}" y1="{h}" x2="{w / 2 + (x - w / 2) * .25}" y2="{base + 90}" stroke="#fff" stroke-width="3" opacity=".6"/>'
    for i in range(5):
        y = base + 90 + (i ** 1.7) * 62
        b += f'<line x1="0" y1="{y:.0f}" x2="{w}" y2="{y:.0f}" stroke="#fff" stroke-width="3" opacity=".55"/>'
    b += ''.join(f'<rect x="{x}" y="{y}" width="8" height="{hh}" fill="#fff"/><polygon points="{x + 8},{y} {x + 8 + hh * .6},{y + hh * .18} {x + 8},{y + hh * .36}" fill="{CORAL}"/>' for x, y, hh in [(180, 700, 150), (520, 860, 190), (760, 640, 120)])
    b += f'<circle cx="{w * .78}" cy="{h * .12}" r="48" fill="#FFF3CF"/>' + ''.join(tree(x, base + 70, 90, '#2E7D4F') for x in (80, 300, 840))
    return b


def _commercial(w, h):
    base = h - 70
    b = ''
    for i, (x, ww, hh) in enumerate([(30, 260, 780), (330, 220, 940), (580, 290, 700)]):
        b += f'<rect x="{x}" y="{base - hh}" width="{ww}" height="{hh}" fill="#0D1A30"/><rect x="{x}" y="{base - hh}" width="{ww}" height="{hh}" fill="#6FA0C8" opacity=".18"/>'
        for ry in range(hh // 40):
            b += f'<rect x="{x + 8}" y="{base - hh + 12 + ry * 40}" width="{ww - 16}" height="26" fill="#9FC4E6" opacity="{.18 + .12 * ((ry * 7 + i) % 3)}"/>'
    b += f'<rect y="{base}" width="{w}" height="70" fill="#0A1020"/>'
    b += ''.join(f'<path d="M{x},{base - 4} h104 l-10 -26 h-84 z" fill="{[CORAL, GOLD, "#E9E3F5"][i % 3]}"/><rect x="{x + 6}" y="{base - 4}" width="92" height="4" fill="#000" opacity=".3"/>' for i, x in enumerate(range(24, w, 130)))
    return b


def _rentals(w, h):
    base = h - 90
    b = hills(w, int(h * .6), 70, '#6A3B5E', 1, opacity=.6)
    b += buildings(0, w, base, 200, 520, 70, 140, '#2A1A33', 8, '#FFD98E', .35)
    b += f'<rect y="{base}" width="{w}" height="90" fill="#1A1020"/>'
    b += f'<g transform="translate({w / 2 - 170},{h * .28}) scale(1.7)">{icon("key", "#FAF6F0", GOLD2)}</g>'
    return b


def _redev(w, h):
    base = h - 90
    b = hills(w, int(h * .6), 60, '#B2653F', 1, opacity=.55)
    b += f'<rect x="60" y="{base - 330}" width="320" height="330" fill="#7A4A38"/>' + ''.join(f'<rect x="{80 + c * 54}" y="{base - 300 + r * 70}" width="30" height="40" fill="#2A1710" opacity=".7"/>' for r in range(4) for c in range(5))
    b += tower(470, base, 190, 760, '#F1E9DA', '#4C7CB0', 77, .55, ww=11, wh=14, gx=22, gy=30)
    b += tower(700, base, 150, 560, '#E6D6BC', '#4C7CB0', 78, .5, ww=10, wh=13, gx=20, gy=28)
    b += crane(430, base, 800, '#1A0F0A')
    b += f'<rect y="{base}" width="{w}" height="90" fill="#2A1710"/>'
    return b


def about_scene(w=900, h=1125):
    d1, bg = sky(w, h, [(0, '#0A1525'), (.62, '#254A7A'), (1, '#E9B27A')])
    b = stars(w, h, 70, 11, .5) + sun(int(w * .7), int(h * .3), 46, '#FFF3CF', '#FFD58A')
    base = int(h * .9)
    b += buildings(0, w, base, 120, 420, 40, 90, '#0C1830', 41, '#FFD98E', .25)
    # big heart-house emblem, echoing the logo
    cx, cy = w / 2, h * .54
    b += (f'<path d="M{cx},{cy + 190} C{cx - 330},{cy - 40} {cx - 150},{cy - 250} {cx},{cy - 90} C{cx + 150},{cy - 250} {cx + 330},{cy - 40} {cx},{cy + 190} Z" fill="{CORAL}"/>'
          f'<path d="M{cx - 120},{cy + 40} V{cy - 40} L{cx},{cy - 140} L{cx + 120},{cy - 40} V{cy + 40} Z" fill="#FAF6F0"/>'
          f'<rect x="{cx - 64}" y="{cy - 50}" width="42" height="42" fill="{CORAL}"/><rect x="{cx + 22}" y="{cy - 50}" width="42" height="42" fill="{CORAL}"/>'
          f'<rect x="{cx - 30}" y="{cy + 4}" width="60" height="36" fill="{GOLD}"/>')
    b += f'<rect y="{base}" width="{w}" height="{h - base}" fill="#07101F"/><rect y="{base}" width="{w}" height="5" fill="{GOLD}"/>'
    return svg(w, h, bg + b, d1)


# ------------------------------------------------------------------ render

HEROES = {'hero-mumbai': scene_hero_mumbai, 'hero-kalyan': scene_hero_kalyan, 'hero-towers': scene_hero_towers,
          'hero-township': scene_hero_township, 'hero-corridor': scene_hero_corridor}
CITY_SLUGS = ['kalyan', 'mumbai', 'thane', 'dombivli', 'ulhasnagar', 'ambernath', 'badlapur', 'bhiwandi', 'navi-mumbai', 'panvel']
PROPS = ['apartments', 'villas', 'plots', 'commercial', 'rentals', 'redevelopment']


def jobs():
    j = []
    for k, fn in HEROES.items():
        j.append((f'img/{k}.webp', fn(), 'webp', 80))
    for s in CITY_SLUGS:
        j.append((f'img/areas/{s}.jpg', city_scene(s), 'jpg', 86))
    for s in BLOG_STYLES:
        j.append((f'img/blog/{s}.jpg', blog_scene(s), 'jpg', 86))
    for p in PROPS:
        j.append((f'img/types/{p}.jpg', prop_scene(p), 'jpg', 84))
    j.append(('img/about.jpg', about_scene(), 'jpg', 86))
    return j


def render(only=None):
    from playwright.sync_api import sync_playwright
    import re
    tmp = os.path.join(ROOT, '.imgtmp')
    os.makedirs(tmp, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch()
        for rel, s, fmt, q in jobs():
            if only and not any(o in rel for o in only):
                continue
            w, h = map(int, re.search(r'width="(\d+)" height="(\d+)"', s).groups())
            pg = br.new_page(viewport={'width': w, 'height': h})
            pg.set_content(f'<html><body style="margin:0;background:#000">{s}</body></html>')
            png = os.path.join(tmp, 'x.png')
            pg.screenshot(path=png)
            pg.close()
            out = os.path.join(ROOT, rel)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            im = Image.open(png).convert('RGB')
            if fmt == 'webp':
                im.save(out, 'WEBP', quality=q, method=6)
            else:
                im.save(out, 'JPEG', quality=q, optimize=True, progressive=True, subsampling=0)
            print('wrote', rel, f'{os.path.getsize(out) // 1024} KB')
        br.close()
    os.remove(os.path.join(tmp, 'x.png'))
    os.rmdir(tmp)


def brand_assets():
    """Optimised logo, favicons, touch icons and the default social image, all from the supplied logo."""
    src = Image.open(os.path.join(IMG, 'prestige_enterprises.in.png')).convert('RGB')
    W, H = src.size
    logo = src.copy()
    logo.thumbnail((1200, 1200))
    logo.save(os.path.join(IMG, 'logo.webp'), 'WEBP', quality=88, method=6)
    logo.save(os.path.join(IMG, 'logo.png'), 'PNG', optimize=True)
    # emblem = the heart-house on the left of the logo card
    em = src.crop((int(W * .035), int(H * .09), int(W * .335), int(H * .91)))
    side = max(em.size)
    sq = Image.new('RGB', (side, side), (247, 244, 239))
    sq.paste(em, ((side - em.width) // 2, (side - em.height) // 2))
    for name, px in [('icon-192.png', 192), ('apple-touch-icon.png', 180), ('icon-512.png', 512)]:
        sq.resize((px, px), Image.LANCZOS).save(os.path.join(ROOT, name) if name != 'icon-512.png' else os.path.join(IMG, name), 'PNG', optimize=True)
    sq.resize((64, 64), Image.LANCZOS).save(os.path.join(ROOT, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    # default social card: logo on cream, skyline silhouettes in gold
    og = Image.new('RGB', (1200, 630), (247, 244, 239))
    lg = src.copy()
    lg.thumbnail((920, 420))
    og.paste(lg, ((1200 - lg.width) // 2, 70))
    ov = svg(1200, 630, buildings(0, 1200, 630, 40, 150, 30, 70, GOLD, 5, None) + f'<rect y="620" width="1200" height="10" fill="{CORAL}"/>')
    return og, ov


def render_og():
    from playwright.sync_api import sync_playwright
    og, ov = brand_assets()
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={'width': 1200, 'height': 630})
        pg.set_content(f'<html><body style="margin:0;background:transparent">{ov}</body></html>')
        tmp = os.path.join(ROOT, 'og_overlay.png')
        pg.screenshot(path=tmp, omit_background=True)
        br.close()
    over = Image.open(tmp).convert('RGBA')
    base = og.convert('RGBA')
    base.alpha_composite(over)
    # keep the logo on top of any silhouette that overlaps it
    lg = Image.open(os.path.join(IMG, 'prestige_enterprises.in.png')).convert('RGB')
    lg.thumbnail((920, 420))
    base.paste(lg, ((1200 - lg.width) // 2, 70))
    base.convert('RGB').save(os.path.join(IMG, 'og-default.jpg'), 'JPEG', quality=88, optimize=True)
    os.remove(tmp)
    print('wrote img/og-default.jpg + logo/icons')


if __name__ == '__main__':
    only = sys.argv[1:] or None
    render(only)
    if not only:
        render_og()
