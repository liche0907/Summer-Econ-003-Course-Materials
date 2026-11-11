#!/usr/bin/env python3
"""ECON 003 — T4 spot-icon library. Flat vector, 3 colours, transparent ground.
100x100 viewBox, 8px uniform stroke where stroked. Palette locked to the deck."""

import os

NAVY = "#003DA5"
GOLD = "#FFB81D"
GREY = "#4A4A4A"
SW   = 7          # uniform stroke weight

HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">'
        '<g fill="none" stroke-width="%d" stroke-linecap="round" stroke-linejoin="round">' % SW)
TAIL = '</g></svg>'

ICONS = {

"coffee-cup": f'''
<path d="M18 38 h50 v22 a25 25 0 0 1 -50 0 z" stroke="{NAVY}"/>
<path d="M68 44 h9 a10 10 0 0 1 0 20 h-9" stroke="{NAVY}"/>
<path d="M16 84 h58" stroke="{NAVY}"/>
<path d="M34 26 q5 -7 0 -14" stroke="{GOLD}"/>
<path d="M50 26 q5 -7 0 -14" stroke="{GOLD}"/>
''',

"factory": f'''
<path d="M14 86 v-38 l22 14 v-14 l22 14 v-14 l22 14 v24 z" stroke="{NAVY}"/>
<path d="M74 48 v-30 h12 v30" stroke="{GOLD}"/>
<path d="M28 72 h10 M52 72 h10" stroke="{GOLD}"/>
''',

"house": f'''
<path d="M14 48 L50 18 L86 48" stroke="{GOLD}"/>
<path d="M24 44 v42 h52 v-42" stroke="{NAVY}"/>
<path d="M42 86 v-24 h16 v24" stroke="{GOLD}"/>
''',

"truck": f'''
<path d="M8 26 h46 v40 h-46 z" stroke="{NAVY}"/>
<path d="M54 40 h18 l14 14 v12 h-32 z" stroke="{NAVY}"/>
<circle cx="30" cy="76" r="9" stroke="{GOLD}"/>
<circle cx="70" cy="76" r="9" stroke="{GOLD}"/>
''',

"ballot-box": f'''
<path d="M16 44 h68 v42 h-68 z" stroke="{NAVY}"/>
<path d="M36 44 h28" stroke="{GOLD}" stroke-width="9"/>
<path d="M40 38 v-24 h24 v24" stroke="{GOLD}"/>
<path d="M48 24 l5 6 l10 -12" stroke="{NAVY}"/>
''',

"wheat": f'''
<path d="M50 92 v-50" stroke="{NAVY}"/>
<path d="M50 34 q-9 -15 0 -26 q9 11 0 26 z" stroke="{GOLD}"/>
<path d="M50 50 q-20 -5 -23 -23 q20 3 23 23 z" stroke="{GOLD}"/>
<path d="M50 50 q20 -5 23 -23 q-20 3 -23 23 z" stroke="{GOLD}"/>
<path d="M50 70 q-20 -5 -23 -23 q20 3 23 23 z" stroke="{GOLD}"/>
<path d="M50 70 q20 -5 23 -23 q-20 3 -23 23 z" stroke="{GOLD}"/>
''',

"phone": f'''
<rect x="30" y="10" width="40" height="80" rx="7" stroke="{NAVY}"/>
<path d="M30 26 h40 M30 74 h40" stroke="{GOLD}"/>
<path d="M44 82 h12" stroke="{GOLD}"/>
''',

"shopping-cart": f'''
<path d="M10 18 h12 l12 44 h38 l10 -30 h-54" stroke="{NAVY}"/>
<circle cx="40" cy="80" r="7" stroke="{GOLD}"/>
<circle cx="70" cy="80" r="7" stroke="{GOLD}"/>
''',

"gas-pump": f'''
<path d="M18 88 v-70 a6 6 0 0 1 6 -6 h26 a6 6 0 0 1 6 6 v70 z" stroke="{NAVY}"/>
<path d="M10 88 h64" stroke="{NAVY}"/>
<path d="M28 30 h18 v16 h-18 z" stroke="{GOLD}"/>
<path d="M56 40 h14 a6 6 0 0 1 6 6 v26 a7 7 0 0 0 12 5" stroke="{GOLD}"/>
''',

"clock": f'''
<circle cx="50" cy="52" r="34" stroke="{NAVY}"/>
<path d="M50 32 v22 h16" stroke="{GOLD}"/>
<path d="M50 12 v6" stroke="{NAVY}"/>
''',

"exchange": f'''
<path d="M16 36 h60" stroke="{GOLD}"/>
<path d="M62 22 l14 14 l-14 14" stroke="{GOLD}"/>
<path d="M84 66 h-60" stroke="{NAVY}"/>
<path d="M38 52 l-14 14 l14 14" stroke="{NAVY}"/>
''',

"shipping-container": f'''
<rect x="10" y="32" width="80" height="42" rx="3" stroke="{NAVY}"/>
<path d="M24 32 v42 M76 32 v42" stroke="{GOLD}"/>
<path d="M38 42 v22 M50 42 v22 M62 42 v22" stroke="{NAVY}"/>
''',

"apartment": f'''
<path d="M22 88 v-70 h56 v70 z" stroke="{NAVY}"/>
<path d="M34 32 h12 M54 32 h12 M34 50 h12 M54 50 h12" stroke="{GOLD}"/>
<path d="M42 88 v-20 h16 v20" stroke="{GOLD}"/>
''',

"hard-hat": f'''
<path d="M22 64 a28 28 0 0 1 56 0 z" stroke="{GOLD}"/>
<path d="M10 64 h80" stroke="{NAVY}"/>
<path d="M37 48 a17 17 0 0 1 26 0" stroke="{NAVY}"/>
''',

"receipt": f'''
<path d="M24 12 h52 v76 l-9 -7 l-8 7 l-9 -7 l-8 7 l-9 -7 l-9 7 z" stroke="{NAVY}"/>
<path d="M36 32 h28 M36 46 h28 M36 60 h16" stroke="{GOLD}"/>
''',

"price-tag": f'''
<path d="M52 10 h34 v34 l-42 42 a6 6 0 0 1 -9 0 l-25 -25 a6 6 0 0 1 0 -9 z" stroke="{GOLD}"/>
<circle cx="71" cy="25" r="7" stroke="{NAVY}"/>
''',

"balance-scale": f'''
<path d="M50 14 v70 M30 86 h40" stroke="{NAVY}"/>
<path d="M14 30 h72" stroke="{NAVY}"/>
<path d="M14 30 v8 M86 30 v8" stroke="{NAVY}"/>
<path d="M2 40 h24 l-6 13 h-12 z" stroke="{GOLD}"/>
<path d="M74 40 h24 l-6 13 h-12 z" stroke="{GOLD}"/>
''',

"coin-stack": f'''
<ellipse cx="50" cy="30" rx="30" ry="11" stroke="{GOLD}"/>
<path d="M20 30 v14 a30 11 0 0 0 60 0 v-14" stroke="{NAVY}"/>
<path d="M20 48 v14 a30 11 0 0 0 60 0 v-14" stroke="{NAVY}"/>
<path d="M20 66 v14 a30 11 0 0 0 60 0 v-14" stroke="{NAVY}"/>
''',

"lightbulb": f'''
<path d="M50 10 a26 26 0 0 1 16 46 v10 h-32 v-10 a26 26 0 0 1 16 -46 z" stroke="{GOLD}"/>
<path d="M36 76 h28 M42 88 h16" stroke="{NAVY}"/>
''',

"up-down": f'''
<path d="M32 84 v-58 M18 40 l14 -14 l14 14" stroke="{GOLD}"/>
<path d="M68 16 v58 M54 60 l14 14 l14 -14" stroke="{NAVY}"/>
''',

"burger": f'''
<path d="M24 48 a26 20 0 0 1 52 0 z" stroke="{GOLD}"/>
<path d="M22 56 h56" stroke="{NAVY}"/>
<path d="M22 64 q7 -6 14 0 q7 6 14 0 q7 -6 14 0 q7 6 14 0" stroke="{GOLD}"/>
<path d="M26 72 h48 a10 8 0 0 1 -10 8 h-28 a10 8 0 0 1 -10 -8 z" stroke="{NAVY}"/>
''',

"manager": f'''
<circle cx="50" cy="42" r="11" stroke="{NAVY}"/>
<path d="M24 92 Q24 70 46 66" stroke="{NAVY}"/>
<path d="M76 92 Q76 70 54 66" stroke="{NAVY}"/>
<path d="M45 69 h10" stroke="{GOLD}"/>
<path d="M50 69 v20" stroke="{GOLD}"/>
''',

"cook": f'''
<circle cx="50" cy="42" r="11" stroke="{NAVY}"/>
<path d="M26 92 a24 24 0 0 1 48 0" stroke="{NAVY}"/>
<circle cx="40" cy="17" r="8" stroke="{GOLD}"/>
<circle cx="50" cy="12" r="9" stroke="{GOLD}"/>
<circle cx="60" cy="17" r="8" stroke="{GOLD}"/>
<path d="M34 28 h32 M34 28 v-8 M66 28 v-8" stroke="{GOLD}"/>
''',

"waiter": f'''
<circle cx="38" cy="42" r="11" stroke="{NAVY}"/>
<path d="M14 92 a24 24 0 0 1 48 0" stroke="{NAVY}"/>
<path d="M54 74 L70 52" stroke="{NAVY}"/>
<path d="M58 48 h36" stroke="{GOLD}"/>
<path d="M68 48 a8 6 0 0 1 16 0" stroke="{GOLD}"/>
''',

"owner": f'''
<circle cx="40" cy="42" r="11" stroke="{NAVY}"/>
<path d="M16 92 a24 24 0 0 1 48 0" stroke="{NAVY}"/>
<circle cx="78" cy="52" r="8" stroke="{GOLD}"/>
<path d="M78 60 v24" stroke="{GOLD}"/>
<path d="M78 68 h8 M78 76 h8" stroke="{GOLD}"/>
''',

"register": f'''
<path d="M14 84 h72 v-18 h-72 z" stroke="{NAVY}"/>
<path d="M32 66 v-30 h36 v30" stroke="{NAVY}"/>
<path d="M40 46 h20" stroke="{GOLD}"/>
<path d="M24 75 h10 M45 75 h10 M66 75 h10" stroke="{GOLD}"/>
''',

"ledger": f'''
<path d="M18 16 h64 v68 h-64 z" stroke="{NAVY}"/>
<path d="M18 34 h64" stroke="{NAVY}"/>
<path d="M56 34 v50" stroke="{GOLD}"/>
<path d="M28 48 h20 M28 62 h20 M64 48 h10 M64 62 h10" stroke="{GOLD}"/>
''',

"research": f'''
<circle cx="46" cy="44" r="27" stroke="{NAVY}"/>
<path d="M66 64 l18 18" stroke="{NAVY}"/>
<path d="M36 56 v-8 M46 56 v-16 M56 56 v-24" stroke="{GOLD}"/>
''',

"jeans": f'''
<path d="M28 18 h44 v10 h-44 z" stroke="{NAVY}"/>
<path d="M28 28 V88 H42 L50 50 L58 88 H72 V28" stroke="{NAVY}"/>
<path d="M32 36 h9 M68 36 h-9" stroke="{GOLD}"/>
<path d="M28 23 h44" stroke="{GOLD}"/>
''',

"sweater": f'''
<path d="M22 40 L36 28 H64 L78 40 L70 58 L64 54 V84 H36 V54 L30 58 Z" stroke="{NAVY}"/>
<path d="M40 28 a11 8 0 0 0 20 0" stroke="{GOLD}"/>
<path d="M36 79 h28" stroke="{GOLD}"/>
''',
}

if __name__ == "__main__":
    out = "/home/claude/art/icons"
    os.makedirs(out, exist_ok=True)
    for name, body in ICONS.items():
        with open(f"{out}/{name}.svg", "w") as f:
            f.write(HEAD + body.strip() + TAIL)
    print("wrote", len(ICONS), "icons")
