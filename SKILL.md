---
name: brand-identity-poster
description: Builds a client-ready brand identity poster (brand guideline board) from a brand's real logo and assets, with logo rules, color in use, type, graphics, mockups and tone, as self-contained HTML, PNG and PDF. Use for "brand board", "brand guidelines poster", "identity sheet", "present my brand on Behance". Not for logo design or full brand books.
---

# Brand Identity Poster

Make one vertical poster that presents a brand's visual identity the way a senior
studio would show it to a client: logo, clear space, backgrounds, color, type,
graphic language, real-looking applications and tone, on a single board.

The deliverables are `poster.html` (self-contained, scales to any screen),
`poster.png` (2400 × 3600 by default), `poster.pdf` (one page) and
`brand-brief.md` (the analysis and decisions behind the board).

## What this skill exists to prevent

Boards like this usually fail in one of two ways, and both are easy to spot.

1. **Invented identity.** A symbol the brand never had, a palette picked by mood,
   "+300 % growth" stats, a stock founder photo. The client sees a stranger's brand.
   Everything on the board must come from the brand's real material, or be
   derived from it in a way you can explain in one sentence.
2. **Broken craft.** Text that spills out of its card, a list clipped at the
   bottom, a fallback font in the PDF, a table of hex codes nobody can judge.
   These come from building blind. This skill renders and audits every
   iteration, so you see what the client will see.

## Step 1: Gather what is real

Ask only for what is missing. Most of it may already be in the conversation or
in the user's files.

**Essential**
- **The logo file.** Best: SVG. Good: PNG or WebP with transparency. If you only
  get a JPG or a screenshot, ask for the original once. Without it you can still
  show the positive version, but you cannot honestly make a negative or a
  one-color version, so say so in the brief instead of faking one.
- **Brand name and the language of the poster.** Write all poster copy in the
  brand's language, whatever language these instructions are in.
- **What the poster is for.** A pitch to a client, a Behance post, an investor
  deck. It changes which applications you show.

**Use if it exists** (search the user's files before asking)
- A design system: tokens, a CSS file, a brand PDF, a Figma export, the website's
  stylesheet, or a `manifest.json` from the `design-system-forge` skill.
- Real copy: website headlines, taglines, product names, contact line.
- Real imagery: brand photos, illustrations, product shots, screenshots of the
  site or app.

Then pick the mode and write it in the brief:

| Mode | When | The rule |
|---|---|---|
| **Codify** | The brand already has a system (colors, fonts, rules) | The system wins. You present it; you do not redesign it. Where a generic best practice clashes with the brand's rules, follow the brand and note the clash in the brief. |
| **Derive** | You only have a logo (and maybe a name and a sector) | You build the smallest coherent system the logo implies: palette sampled from the logo, neutrals tinted toward its hue, type matched to its letter construction. Every derivation is written in the brief as a proposal. |

How to read a logo, sample a palette, pair fonts and describe a tone:
`references/brand-analysis.md`.

## Step 2: Write the brand brief first

Before any HTML, write `brand-brief.md` next to the poster. Use this structure:

```markdown
# <Brand>: brand brief
## Mode
Codify | Derive, and the sources used (files, URLs).
## Analysis
| Question | Answer |   ← logo form, personality, ideal client, sector, emotional
                          tone, level of luxury/tech/closeness, aesthetic direction
## Decisions
Palette with roles · type families and roles · graphic language · imagery · icon family
## Given vs derived
What came from the brand, what you derived, and from what.
## Conflicts
What the request asked for that the brand contradicts, and what you did.
## Board map
An ASCII sketch of the blocks on the 12-column grid.
```

Writing it first forces the decisions before the pixels, and it becomes the
document the user hands to their client next to the poster.

## Step 3: Plan the board

- **Canvas.** 2400 × 3600 px (2:3), the classic poster ratio. Use 2400 × 3000
  (4:5) when the board is mainly for Instagram. Declare it with
  `<meta name="poster-size" content="2400x3600">`; the renderer reads it.
- **Grid.** 12 columns, rows sized in `fr` so the board always fits the canvas.
  Give rows that hold more content more `fr` instead of shrinking type.
- **Blocks.** Choose from the catalog in `references/blocks.md`. Always include:
  cover, logo, clear space and misuse, logo on backgrounds, color, typography,
  applications, and a closing line. Add graphic elements, icons, tone, rules or a
  dark-mode panel when the brand has real material for them.
- **Vary the blocks.** Different widths, different surfaces (paper, tinted,
  inverted, image). A grid of identical cards is the fastest way to look like a
  template.
- **Do not ship the template's layout unchanged.** It is a map of what goes
  where. Give the cover real presence (a large logo, a big brand line, a full
  photo), change proportions where the brand's character asks for it, and decide
  where the eye lands first. In tests, boards that kept the template's
  proportions came out correct but forgettable.

## Step 4: Build

1. Make a working folder. Put the brand files in `brand/`. Copy
   `assets/template.html` to `poster.src.html`.
2. Restyle the template's tokens (`:root` variables) to the brand. The template is
   scaffolding with neutral styling, not a look to keep.
3. Reference files through placeholders; `scripts/build.py` turns them into one
   self-contained file:

   | Placeholder | Becomes |
   |---|---|
   | `{{svg:brand/logo.svg}}` | the SVG inlined, original colors kept |
   | `{{mask:brand/logo.svg}}` | a data URI for `mask-image`, to recolor the real logo (negative, one-color, favicon) |
   | `{{img:brand/photo.jpg?w=1600}}` | an image data URI, resized and converted to WebP |
   | `{{font:brand/Font.woff2}}` | a font data URI for `@font-face` |
   | `{{lucide:calendar-days}}` | an inline Lucide icon (pinned version) |

   `{{img:...}}` and `{{mask:...}}` also work inside CSS, as `url({{img:brand/pattern.svg}})`.
   Each block has an explicit `grid-row` and `grid-column`: when you delete or
   move a block, update them and `grid-template-rows`. `--mono` is optional;
   point it at `--text` if the brand has no monospace.

   ```bash
   python3 scripts/build.py poster.src.html poster.html
   ```

**Craft rules, and why they matter**

- **The logo is sacred.** Use the real file, inline or as a mask. Never retype it,
  redraw it, stretch it, outline it, or add gradients, shadows or glows. Recoloring
  is only for single-color versions the brand would plausibly use.
- **Logo variants, honestly.** Pick by how the logo is built:
  - *One color* (a single fill, no knockouts): `{{mask:...}}` recolors it
    anywhere through `.mark`. This is the easy case the template assumes.
  - *Several colors, or shapes knocked out of a solid* (a symbol inside a filled
    square, letters cut out of a badge): a mask turns it into a solid blob. Make
    copies of the real SVG in `brand/` and change only the `fill` and `stroke`
    values to palette tokens: a reversed version for dark backgrounds, a
    one-color version, the symbol alone (the same file with the other paths
    removed or the `viewBox` cropped). Inline them with `{{svg:...}}`.
  - Write every derived file in the brief as a proposal ("reversed version: same
    geometry, brown swapped for cream"). If the brand already has its own
    variants, use those instead.
- **Clear space comes from the logo.** Measure it with a unit taken from the logo
  itself (the cap height, the width of a letter, the size of the symbol), and draw
  that unit on the board. A fixed percentage fits no real logo.
- **Show color in use, not a hex table.** Each color gets its role ("buttons",
  "backgrounds", "only for alerts"), its code, the contrast ratio when it is a
  text color, and a small live component that uses it.
  `python3 scripts/contrast.py --grid "#hex" "#hex" ...` gives every ratio. A proportion strip (lots
  of background, little accent) explains more than any number of swatches.
- **Typography with real sentences.** Specimens use the brand's own lines, plus a
  size scale. Load fonts from Google Fonts or embed the files; if the brand font is
  unavailable, use the closest match and say so in the brief.
- **Graphic elements must be traceable.** In Codify mode, use the brand's existing
  patterns and devices. In Derive mode, build them only from the real logo
  geometry (crop of the mark, repetition, scale changes, one-color masks) plus
  neutral instruments (rules, grids, corner marks). Never draw a new symbol.
- **One icon family.** The brand's own if it has one; otherwise Lucide with one
  stroke width.
- **Mockups built from the system.** Business card (front and back), a social
  post, a document page, a web or app screen, signage, packaging only if the brand
  sells physical products. Build them in HTML/CSS with the brand's tokens, or use
  real screenshots. Skip fake browser dots and phone bezels: they date the board
  and read as a template; a clean rounded screen with a soft shadow is enough.
- **Real content only.** Copy comes from the brand. No invented metrics,
  testimonials, client names or prices. Placeholder content is labeled as an
  example, visibly.
- **Imagery.** Use the brand's own. Never generate a person who could pass for the
  founder or a real customer. With no imagery, make the cover typographic or build
  it from the logo and color.

**Patterns that make a board look generated.** Avoid them unless the brand
itself uses them. They are drawn from the public Hallmark anti-pattern catalog
(github.com/Nutlope/hallmark).
- Numbered labels over section titles ("01 / PALETTE"): the title alone is enough.
- A thick colored stripe on one side of a card.
- Three identical cards in a row.
- Gradient text, purple-blue "AI" gradients, glassmorphism, glowing blobs.
- Everything centered, section after section.
- Emoji as icons, or icons mixed from several libraries.
- Pure `#000` and `#FFF`: tint the neutrals toward the brand.

## Step 5: Render, audit, look

```bash
python3 scripts/render.py poster.html --crops
```

It writes `poster.png`, `poster.pdf`, `audit.json`, one full-resolution crop per
block in `crops/`, and `sweep.png` at 65 %. It reports:

- **ERROR** content outside its block, content clipped by `overflow: hidden`,
  web fonts that failed, broken images. Fix all of them.
- **WARNING** fonts that are neither linked nor embedded, text under 13 px,
  horizontal scroll at 1440 px, a PDF with more than one page or fallback fonts.

Mark blocks with `data-block="name"` and the poster root with `data-poster`.
Mark anything meant to bleed outside its block (a card that overlaps an edge, a
logo cropped inside a pattern tile) with `data-bleed`, so the audit does not flag
it. A container with `overflow: hidden` that holds a `data-bleed` child is not
reported as clipped.

A clean audit means nothing is broken; it does not mean the board is good. The
audit cannot see empty areas, weak hierarchy or a dull cover.

Then look, because the audit cannot judge design:
1. Open every crop at full size. Check alignment, spacing, and text that touches
   an edge.
2. Open `sweep.png`. Without reading, can you tell each block apart and see where
   the eye lands first? If two blocks blur together, change a surface or a size.
3. Run the checklist in `references/checklist.md`.

Common fixes: give the row more `fr` or shorten the copy rather than shrinking
type below 13 px; flex or grid children with a fixed aspect ratio need
`min-height: 0`; overlapping cards must not cover text (move the text, not the
card); a long list in a small card becomes two columns or loses its descriptions.

Iterate until the audit has no errors and the checklist passes. Three or four
rounds is normal.

## Step 6: Deliver

Hand over `poster.html`, `poster.png`, `poster.pdf`, `brand-brief.md`, and the
source (`poster.src.html` plus `brand/`) so the board can be rebuilt. For a print
shop, re-render with `--scale 2` (4800 × 7200 px).

In your reply, say what came from the brand and what you derived, any conflict
you resolved, and any warning you chose to leave (for example, "fonts load from
Google Fonts, so the HTML needs internet").
