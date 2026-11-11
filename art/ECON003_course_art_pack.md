# ECON 003 — course art pack

The system (Part A), the prompts as they get written (Part B), and what is already built (Part C).

**Palette note.** UCR's published gold is `#FFB81C`; the decks as built use `#FFB81D`. The difference is
invisible on screen, and everything here is normalised to `#FFB81D` so new art matches the decks rather
than the brand sheet.

**Scope note.** The deck's visual identity is already fixed by the UCR template and the finished Ch01 and
Ch03 decks. Nothing here restyles it. New chapter decks are built by copying an existing deck; the only
art a chapter strictly requires is its title-slide triangle.

---

# Part A — the system

# ECON 003 — slide image system

Keep this open in a second window. Workflow: pick a template → pick a style → paste
`[TEMPLATE BLOCK] + [STYLE BLOCK] + [your subject]` into the tool. No thinking required mid-session.

Global constants, appended to every prompt:

```
16:9 aspect ratio. No text, letters, numbers, or signage anywhere in the image.
No watermark, no border, no frame.
```

---

## Part 1 — Templates (the format)

### T1. Story panel
Carries a worked example. One clear action, readable in two seconds from the back row.

```
A single narrative moment: [SUBJECT DOING ACTION].
Exactly [N] figures, no bystanders. One clear focal point, centered slightly left.
Plain uncluttered background, no scenery beyond what the action requires.
Medium shot, eye level. Right third left empty for caption text.
```
**Tool:** Midjourney (painterly styles) or Recraft (flat styles)
**Volume:** 1–2 per lecture. Highest effort, highest payoff.

---

### T2. Eye-catcher
Section opener / attention reset. Nearly empty. The image is a punctuation mark, not content.

```
One single object: [OBJECT], isolated, centered.
Nothing else in frame. Solid flat background, no gradient, no shadow, no floor.
Generous empty space on all sides. Bold silhouette readable at thumbnail size.
```
**Tool:** Recraft (vector output — recolor to deck palette)
**Volume:** 1 per section, ~4 per lecture.
**Rule:** if you can describe it in more than six words, it's a T1, not a T2.

---

### T3. Filler / breather
Sits behind or beside text during a dense stretch. Must lose the fight for attention.

```
Low-contrast [SCENE/TEXTURE], muted, desaturated, soft.
No focal point, no figures, no detail that rewards looking closely.
Even tonal value across the whole frame. Bottom two-thirds visually quiet.
```
**Tool:** Recraft
**Volume:** 2–4 per lecture.
**Rule:** if a student's eye stops on it, it failed. Generate, then squint — anything that pops, regenerate flatter.

---

### T4. Spot icon
Small repeatable object next to a bullet. Highest volume, lowest cost.

```
Single [OBJECT] icon, flat, front-facing, no perspective.
Uniform stroke weight. Maximum 3 colors. Transparent background.
Simplified to essential shapes only.
```
**Tool:** Recraft vector — generate 10–15 in one locked-style session, export SVG, build a library.
**Volume:** as many as you want, once the set exists.

---

### T5. Concept metaphor
One visual analogy for an abstract idea. No narrative, no characters. The hardest to write and the most memorable.

```
A visual metaphor for [CONCEPT]: [CONCRETE PHYSICAL SITUATION].
Single image, no panels, no sequence. One idea only.
Symbolic and clean rather than literal or busy.
```
**Tool:** either. **Volume:** 1 per chapter at most.
**Note:** ask Claude for three metaphor options before generating. The concept is the work; the render is trivial.

---

## Part 2 — Styles (the look)

Never name the artist or studio. Paste the attribute block instead.

### S1. Cinematic anime landscape
> Backlit painterly digital illustration. Towering detailed cumulus clouds, high-saturation
> sky in blue and orange. Volumetric light rays. Small human figure in a large landscape.
> Soft focus foreground, sharp midground. No outlines. Lens flare minimal.

**Use for:** T1, T3. Emotional weight, openings, "the big picture" moments.
**Avoid for:** T2, T4 — far too much detail.

---

### S2. Soft hand-painted pastoral
> Gouache and watercolor illustration. Soft edges, visible brush texture. Muted greens
> and warm daylight. Rounded organic shapes, gentle simplified faces. No hard outlines.
> Cozy domestic scale, low contrast.

**Use for:** T1, T3. Everyday-life examples, households, small business.

---

### S3. Newspaper strip
> Hand-inked comic strip. Thick uneven black line, deliberately imperfect. Flat cream
> background. Oversized round heads on small bodies, dot eyes, minimal facial detail.
> Three flat colors maximum. Generous white space. No shading, no gradient.

**Use for:** T1, T2, T5. Humor, gentle irony, a beat of relief in a dense stretch.
**Strongest for:** anything where the joke does the teaching.

---

### S4. Countryball
> Crude MS-Paint comic. Perfectly round spheres filled with flat national flag patterns.
> No limbs, or thin stick limbs. Simple oval eyes. Plain single-color background.
> Deliberately amateur, jagged edges, no anti-aliasing.

**Use for:** T1, T5 — international trade, comparative advantage, tariffs, exchange rates.
**Note:** the crudeness is the point. If it looks polished, it's wrong.

---

### S5. Flat editorial vector *(default house style)*
> Flat vector illustration. No gradients, no shadows, no texture. Geometric simplified
> shapes. Strict four-color palette. Uniform stroke weight or no stroke. Clean negative
> space. Neutral, calm, unfussy.

**Use for:** all templates. This is the spine of the deck.
**Palette:** lock to UCR blue + gold + one neutral + one accent. Specify hex codes explicitly —
`using only #003DA5, #FFB81C, #4A4A4A` beats "blue and gold" every time.

---

## Part 3 — The matrix

|        | S1 cinematic | S2 pastoral | S3 strip | S4 countryball | S5 flat vector |
|--------|:---:|:---:|:---:|:---:|:---:|
| T1 story panel | ✅ | ✅ | ✅ | ✅ | ✅ |
| T2 eye-catcher | ❌ | ➖ | ✅ | ➖ | ✅ |
| T3 filler | ✅ | ✅ | ❌ | ❌ | ✅ |
| T4 spot icon | ❌ | ❌ | ➖ | ❌ | ✅ |
| T5 metaphor | ➖ | ➖ | ✅ | ✅ | ✅ |

Guardrail: **max two styles per lecture.** S5 as the spine, one guest style for contrast.
More than two and the deck reads as assembled rather than designed.

---

## Part 4 — Setup, once

1. Generate 3–5 images you like in S5. Upload them to Recraft as a **custom style**, name it
   `econ003-house`. Every later generation uses it. This is the single highest-value step.
2. Repeat for S3 and S4 if you want them locked. S1/S2 stay in Midjourney with `--style raw --s 50`.
3. Generate a T4 spot-icon batch of 15 common objects in one session — coffee cup, factory,
   house, truck, ballot box, wheat, phone, shopping cart, gas pump, clock, handshake,
   shipping container, apartment block, hard hat, receipt. Export SVG. This library covers most weeks.

## Part 5 — Weekly loop

1. Draft the lecture with placeholders: `[T1/S3: firm decides whether to shut down]`.
2. At the end, collect every placeholder into one list.
3. One sitting: paste template + style + subject for each. Generate all. Don't tweak — regenerate
   with a tighter constraint if it's wrong.
4. Drop in, add captions in Beamer/PowerPoint.

Never interleave step 3 with step 1. Art-directing and lecture-writing are different modes and
switching between them is what makes this feel slow.

---

# Part B — chapter prompts

**Written per lecture, as the lecture is drafted. Not stocked in advance.**

Prompts live here once they exist, added chapter by chapter. Writing them ahead of the deck produced
images for examples that were never taught, so the order is now: draft the lecture, collect the
placeholders, then write and run the prompts for what the deck actually contains.

## How a prompt gets made

1. **Draft the lecture with placeholders** in the notes — `[T1/S3: firm decides whether to shut down]`.
2. **Collect every placeholder** into one list when the deck is done. Do not stop mid-draft to art-direct;
   they are different modes and switching between them is what makes this feel slow.
3. **Assign each one a template and a style** from Part A. S5 flat editorial vector is the spine; one
   guest style per lecture, never two. Check the ❌ cells before pairing.
4. **Write the prompt** — subject clause, then the template block, then the style block, then the globals.
   The subject clause should name the decision being made, not the scene: "two people at the ticket
   window, one holding up two fingers while the other looks at the all-day wristband" carries a choice;
   "a couple at an amusement park" carries a mood. Only the first can sit beside a worked example.
5. **Generate**, then **file the prompt here** under its chapter so the next chapter can borrow the phrasing.

## Running it in Gemini

One chat per style — Gemini holds a look far better across a single conversation than it does across
restated prompts. Each style chat opens with a **style-lock message** sent once:

```
For every image in this chat, use exactly this look, and do not vary it between images:

<the S-block from Part A, verbatim>

Standing constraints for every image in this chat:
16:9 aspect ratio. No text, letters, numbers, or signage anywhere in the image.
No watermark, no border, no frame.

Acknowledge, then wait. I will send subjects one at a time.
```

After that, each image is a **subject message** carrying only the template block with its placeholders
filled. The style and the globals are already held by the chat.

Two standing notes:

- **Never name an artist or studio** in a prompt. The attribute block gets the qualities; the name gets
  that artist's most-reproduced frames.
- **Where a template and a style contradict each other, decide once and record it here.** T1 asks for a
  plain background and a medium shot; S1 asks for a small figure in a large landscape. Settled reading:
  under S1 the sky counts as style rather than scenery, and the shot widens to medium-wide.
- **Text is the usual failure.** Ban the surfaces text lives on, not the text itself — "no signs, banners
  or marquees in frame" beats "blank signs", which produces signs full of garbled glyphs. If a second
  take still has lettering, add `no structures with flat vertical faces in the midground`.

## Filed prompts

*(none yet — added chapter by chapter as the lectures are drafted)*

### Chapter 1
### Chapter 3
### Chapter 4
### Chapter 5
### Chapter 6
### Chapter 7
### Chapter 8
### Chapter 9
### Chapter 10
### Chapter 12


---

# Part C — assets already built

Finished files, not prompts.

## C1. Spot-icon library — 28 SVGs, `Resources/Icons/`

`apartment · balance-scale · ballot-box · burger · clock · coffee-cup · coin-stack · cook · exchange ·
factory · gas-pump · hard-hat · house · ledger · lightbulb · manager · owner · phone · price-tag ·
receipt · register · research · shipping-container · shopping-cart · truck · up-down · waiter · wheat`

The T4 tier, built rather than generated: flat vector, transparent ground, uniform 7px stroke, three
colours only (`#003DA5`, `#FFB81D`, `#4A4A4A`). They scale without resampling and drop into PowerPoint
as SVG. Use them across slides *and* Canvas — the same marks recurring in both is most of what makes
the course read as one system.

`manager`, `cook`, `waiter` and `owner` share one figure; only the gold marker changes. Add roles the
same way rather than drawing new people.

Extend with `Resources/ArtScripts/gen_icons.py`. Two lessons from building the set: at 7px stroke,
detail *added inside* a shape merges into it while detail *cut out* of it survives — the manager only
worked once the shoulders were split and the white gap did the reading. And anything defined by a pose
or by depth fights this weight; name objects and roles, not actions.

## C2. Title-slide triangles — `Resources/CoverArt/Chapter Art/`

`ch03_cover_art_triangle.png` (the gear, the reference) and `ch04_title_triangle_market.png` (gouache
market buyer, in use). All per-chapter title art lives in this subfolder; `Resources/CoverArt/` itself
holds the ten chapter covers.

Cut the wedge with `Resources/ArtScripts/make_triangle.py` and place it in a plain rectangular picture
shape, rather than letting PowerPoint clip a raw image — that takes the mirror out of the equation, and
the mirror is what kills most candidates. Spec, geometry and the remaining prompts are in the project doc
`claude/title-slide-art.md` — the one place prompts *are* stocked in advance, because every chapter
needs exactly one and the format never changes.

`ECON003_Ch04_Cover.pptx` is the worked example: Ch03's title slide with the text and the one image
swapped, layout and master untouched.

## C3. Chapter covers — `Resources/CoverArt/`

Ten 1920×1080 covers, PNG plus SVG source, diagrams solved arithmetically. **Not** deck title slides —
those are the UCR template. These are for the video open and the Canvas homepage. Regenerate with
`Resources/ArtScripts/gen_covers.py`.

## C4. Still open

- Title-slide triangles for Ch. 1 (replacement), 4 (upgrade), 5, 6, 7, 8, 9, 10, 12.
- `Resources/canvas_homepage_template_3.html` — not yet reconciled; first place to put the icons to work.
- Ch01's title slide still uses `Cover2.png`, illegible at triangle size.
