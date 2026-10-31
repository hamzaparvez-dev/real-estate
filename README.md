# Prestige Enterprises website

Static site (no framework). English at `/`, Hindi at `/hi/`, Marathi at `/mr/`. Hosted on Vercel.

## Rebuild after any edit
    python3 scripts/build.py          # regenerates every page, sitemap, feeds, llms.txt, vercel.json
    python3 scripts/make_images.py    # only to regenerate the illustrated artwork (needs Playwright + Pillow)

Never edit the generated `index.html` files by hand: they are overwritten. Edit the sources instead:

| What | Where |
|---|---|
| Phone, email, address, RERA no., Meta Pixel ID, social links | `scripts/config.py` |
| Home page copy + menu/button text (EN/HI/MR) | `scripts/ui.py` |
| City pages | `scripts/cities_en.py`, `cities_hi.py`, `cities_mr.py` |
| Blog guides | `scripts/posts_en.py`, `posts_hi.py`, `posts_mr.py` |
| Design / behaviour | `assets/site.css`, `assets/site.js` |
| Images | `img/` (replace any file with a real photo, same file name) |

The build refuses to run if Hindi/Marathi don't match the English structure (same cities, same number of sections, FAQs, etc.).

## Before launch (needs the client)
1. `RERA_NO` in `config.py`: the agent's MahaRERA registration number (shown in footer/contact once filled).
2. `META_PIXEL_ID` in `config.py`: the previous client's Meta Pixel was removed. Add Prestige's own.
3. `SAME_AS` in `config.py`: Facebook Page / Instagram URLs.
4. Replace illustrated artwork with real project or office photos where available.
5. Re-check stamp duty, GST and tax figures in the guides (`posts_*.py`) every year; they are marked "at the time of writing".
6. The git `origin` still points at the previous client's repository. Create a new repo for Prestige and update the remote.
# real-estate
