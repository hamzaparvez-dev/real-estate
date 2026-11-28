"""November 2026 local-keyword guides (EN/HI/MR). One module per guide; see ORDER.

Each module defines SLUG, CAT, READ, KEYWORDS and EN / HI / MR dicts with
title, desc, answer, sections [(heading, [paragraphs], [bullets])], faq [(q, a)].
Inline links use [label](/path/) and are rendered only for these guides.
Facts about Prestige Gold / Prestige One must match the project pages.
"""
import importlib

MODULES = [
    'g01_prestige_flats_kalyan_west',
    'g02_prestige_gold_kalyan_west',
    'g03_prestige_one_godrej_hill',
    'g04_prestige_enterprises_kalyan',
    'g05_5bhk_flats_kalyan_west',
    'g06_3bhk_flats_kalyan_west',
    'g07_1bhk_2bhk_kala_talao',
    'g08_flats_khadakpada',
    'g10_new_projects_kalyan_west',
    'g11_ready_reckoner_kalyan',
    'g13_maharera_check_steps',
    'g14_metro_line_5_kalyan',
    'g16_total_cost_flat_kalyan',
]

_mods = []
for _m in MODULES:
    try:
        _mods.append(importlib.import_module('local_guides.' + _m))
    except ModuleNotFoundError as _e:
        if _e.name != 'local_guides.' + _m:
            raise

ORDER = [m.SLUG for m in _mods]


def posts(lang):
    out = {}
    for m in _mods:
        d = dict(getattr(m, lang.upper()))
        if lang == 'en':
            d.update({'cat': m.CAT, 'read': m.READ, 'keywords': m.KEYWORDS})
        out[m.SLUG] = d
    return out
