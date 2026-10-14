# Block catalog

Each block lists what it must show and the pitfalls seen in real builds. Pick
the blocks the brand can fill with real content. Mark each one with
`data-block="<name>"` so `render.py` can audit and crop it.

## Contents
cover · logo · clearspace · backgrounds · color · color-dark · type · graphics ·
icons · applications · tone · rules · close · a layout recipe

## cover
- The brand's name or logo, the board's title, one line on the identity's idea,
  and a few metadata lines (version, date, scope) in small type.
- Background: a brand photo or scene, or a typographic composition. Put text on a
  solid plate over images; never on a busy area.
- Pitfall: a plate that holds the title, a paragraph and metadata will overflow a
  short row. Give the plate a top and bottom (`top: X; bottom: X`), make it a
  flex column, and let the metadata take `margin-top: auto`.

## logo
- The primary logo large, on a quiet surface, with corner marks or a frame.
- The variants the brand really has: horizontal or stacked lockup, symbol alone,
  one-color versions, app icon or favicon at two or three sizes.
- One sentence on what the logo is made of.
- Pitfall: a logo with a fixed aspect ratio inside a flex column can push the
  block taller than its row. Use `min-height: 0` on the stage and `max-height:
  100%` on the logo.

## clearspace
- The logo with its protected area drawn (dashed outline) and the unit marked
  with small measure lines and a label ("x = cap height of the M").
- Minimum size, shown at real size with its value.
- Four misuses with a cross and a word: stretched, recolored outside the palette,
  effects (shadow or gradient), on a busy background or with an added symbol.
  Build them from the real logo with CSS (`transform: scaleX`, a gradient mask, a
  `filter: drop-shadow`), never as drawings.

## backgrounds
- The logo on five or six surfaces: paper, a light tint, the brand color, the ink
  color, a dark mode background, and over a photo on a plate.
- Each with a caption: surface name, positive or negative, code.
- Use a mask (`{{mask:...}}`) for negatives of single-color logos. For
  multicolor logos, use the brand's own reversed file or show only the surfaces
  where the original works.

## color
- Base colors as large swatches (backgrounds, ink), then the voices or roles as
  a list: swatch, name, role sentence, code, and a live component (button, tag,
  link, alert) that uses it.
- A proportion strip: a single bar split by how much each color is used.
- Contrast ratio next to text colors.
- Pitfall: role descriptions that wrap to three lines make the list taller than
  the row. Keep each to one short sentence.

## color-dark
- Only if the brand has a dark mode or dark surfaces. Same structure, on a dark
  panel, with the components in their dark state.

## type
- One row per family: a large "Aa" in the family, its name, its role and weights,
  and a sample sentence from the brand's copy.
- A size scale with names (title, section, subtitle, lead, body, label) and
  values.

## graphics
- The graphic devices: crops or patterns from the mark, frames, rules, texture,
  an image treatment. Each with a one-line caption on how it is used.
- If the brand has illustrations or a photo style, show two or three examples.

## icons
- Ten to twelve icons from one family, at one stroke width, with labels in the
  brand's language. Choose icons the brand would actually use.

## applications
- Four to six mockups of different sizes: business card front and back, social
  post (feed 4:5 or 3:4) and story or reel cover (9:16), a document page, a web
  or app screen, signage or packaging only if relevant.
- Build them from the tokens, with the brand's real copy, or use real
  screenshots. Label example content ("example").
- Pitfalls: overlapping cards that cover the text of the card behind (keep the
  overlap over empty areas); a document page whose list gets clipped (cut
  descriptions before cutting type size); a phone screenshot needs a radius and a
  shadow, not a bezel.

## tone
- Six short principles, two columns, each "**Principle.** reason". This block
  works well as the one full-color region of the board.

## rules
- Spacing scale (squares), corner radii, shadows or elevation, and four rules in
  one line each ("One primary button per screen").

## close
- A closing line in the brand's voice and the contact (domain, email, handle).
- Pitfall: decorative layers at the bottom (a strip, a texture) need padding
  reserved, or the contact text gets clipped.

## A layout recipe (2400 × 3600, 12 columns)

```
row 1 (≈680fr)  cover ............................ 8 | logo ........ 4
row 2 (≈410fr)  clearspace ........ 5 | backgrounds ................. 7
row 3 (≈630fr)  color ......................... 7 | color-dark .... 5
row 4 (≈500fr)  type .................. 6 | graphics + icons ....... 6
row 5 (≈840fr)  applications ................................... 12
row 6 (≈250fr)  tone ........ 5 | rules ......... 4 | close ....... 3
```

Padding 72 px, gaps 30 to 32 px, block padding about 40 px. Without a dark
mode, give color the full row 3 or pair it with graphics. Treat the recipe as a
start: the brand's material decides the final map.
