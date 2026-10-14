# Brand analysis

How to fill the brief before designing. Two parts: reading what exists (Codify)
and deriving what is missing (Derive). In both, every answer should point at
evidence: a file, a letterform, a line of copy.

## Contents
1. The analysis questions
2. Codify: reading an existing system
3. Derive: palette from the logo
4. Derive: type from the logo
5. Graphic language
6. Tone in a few words
7. When the request contradicts the brand

## 1. The analysis questions

Answer each one in a sentence, with the evidence in parentheses.

| Question | What to look at |
|---|---|
| Main form of the logo | Wordmark, monogram, symbol plus wordmark, emblem. Geometric or organic. Weight and contrast of the strokes. |
| Visual style | Serif or sans, construction (geometric, humanist, grotesque, slab, script), terminals, spacing. |
| Personality | Three adjectives the shapes justify ("rounded terminals, open counters: warm, approachable"). |
| Ideal client | Who buys from this brand. Take it from the user or the website, not from the logo. |
| Sector | What the brand does. Same source. |
| Emotional tone | What a client should feel: calm, energy, trust, delight, status. |
| Luxury, tech, closeness, authority | Place it on each axis. Thin high-contrast serifs and wide spacing lean to luxury; geometric sans and monospace lean to tech; rounded shapes and warm color lean to closeness; heavy serif or strong slab leans to authority. |
| Aesthetic direction | One sentence that the whole board follows ("quiet editorial, lots of paper, one ink color"). |
| Palette | From the system, or sampled (section 3). |
| Type | From the system, or matched (section 4). |
| Expandable system | What can repeat across applications: a color pair, a crop of the mark, a grid, a type treatment. |

## 2. Codify: reading an existing system

Look for, in this order:
1. Design tokens (`tokens.json`, `tokens.css`, a `manifest.json` from
   design-system-forge).
2. The website's CSS. Custom properties on `:root` are usually the tokens. If you
   can fetch the live site, read its stylesheet rather than guessing from a
   screenshot.
3. A brand PDF or style guide.
4. Existing applications (social posts, decks) as evidence of how the system is
   really used.

Record each color with the role the brand gives it. If the brand has rules about
when a color may appear ("accent only for calls to action"), the poster follows
them, even if a generic board would show the color bigger. If the brand has a dark
mode, present both worlds; the board can hold a dark panel next to the light one.

## 3. Derive: palette from the logo

1. **Sample the logo colors.** From an SVG, read the `fill` and `stroke` values.
   From a PNG, take the dominant non-transparent colors (Pillow
   `Image.quantize(colors=6)` on the opaque pixels is enough).
2. **Name roles, not colors.** Typically: ink (text), paper (background), brand
   (the logo color), accent (calls to action), one or two support colors, plus
   success, warning and error only if the board shows interface states.
3. **Tint the neutrals.** Build the paper and the ink by mixing the brand hue in a
   little (2 to 6 % chroma). Pure grey, pure white and pure black look like a
   template next to a colored logo.
4. **Check contrast.** Text colors need 4.5:1 on the backgrounds they sit on (3:1
   for large text). Write the ratio next to text colors on the board. If the logo
   color fails as text, keep it for shapes and make a deeper version for text.
5. **One-color logos.** If the logo is a single dark color, the accent can come
   from the sector or the name; say where it came from in the brief.

## 4. Derive: type from the logo

Match the construction of the logo's letters, not its exact font.

| The logo letters are… | Display family (Google Fonts) | Text family |
|---|---|---|
| High-contrast serif, refined | Playfair Display, Cormorant, Fraunces, Petrona | Inter, Source Sans 3, Geist |
| Sturdy serif or slab | Roboto Slab, Zilla Slab, Bitter, Young Serif | Source Sans 3, IBM Plex Sans |
| Geometric sans | Outfit, Manrope, Sora, Space Grotesk | Inter, DM Sans |
| Humanist sans | Figtree, Nunito Sans, Source Sans 3 | same family, lighter weight |
| Grotesque, neutral | Inter Tight, Archivo, Schibsted Grotesk | Inter, Geist |
| Rounded, friendly | Nunito, Quicksand, Fredoka | Nunito Sans, DM Sans |
| Script or handmade | Keep the script in the logo only. Pair with a calm sans. | DM Sans, Figtree |

Use at most two families, plus a monospace only if the brand shows data, code
or technical labels. If you identify the exact font of the logo, mention it in
the brief, but do not set the logo in it: the logo file stays the logo.

## 5. Graphic language

What can repeat across the board and the applications:
- **From the logo:** a crop of the mark at large scale, the mark repeated as a
  quiet pattern, a one-color silhouette used as a stamp, the angle or curve of a
  letter used as a guide for image crops. Always the real file, masked or
  clipped, never a redrawing.
- **Neutral instruments:** hairline rules, corner marks around frames, a visible
  grid, numbered steps in a document, labels in a monospace.
- **Texture:** paper grain at 3 to 6 % opacity, if the brand is warm or
  editorial. Skip it for crisp tech brands.
- **Imagery style:** describe it in one line (light, framing, subject) even if you
  only have one photo, so the next application follows it.

## 6. Tone in a few words

Six short principles, each with a reason, are more useful than a moodboard. For
example: "Calm. One idea per screen." · "Warmth through material, not color."
Take them from the brand's own copy when possible. In Derive mode, base them on the
personality you wrote in the analysis.

## 7. When the request contradicts the brand

Generic prompts ask for things a given brand may not have or may forbid: patterns
derived from the logo, packaging, many logo variants, device frames, section
numbers. Decide by the brand, not by the prompt, and write each conflict in the
brief's "Conflicts" table with what you did instead. The user asked for *their*
brand presented well; the prompt is the intent, the brand is the source of truth.
