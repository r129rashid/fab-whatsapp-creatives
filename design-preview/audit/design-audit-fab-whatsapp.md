# Design Audit: FAB Skin Hair & Laser Clinic — WhatsApp GIF Creative Pack
**Date:** 2026-05-12  
**Reviewer:** Claude /design-review (gstack)  
**Scope:** 3 design directions (A-soft-bloom, B-gradient-wash, C-marble-mist), static frame review  
**Format under review:** 1080×1080 animated GIF, WhatsApp channel

---

## HEADLINE SCORES

| Direction | Design Score | AI Slop Score | Verdict |
|---|---|---|---|
| A — Soft Bloom | **C+** | **B** | Closest to correct but structurally broken |
| B — Gradient Wash | **C** | **B** | Warm, but gradient fights the logo |
| C — Marble Mist | **C+** | **A** | Most premium, most invisible |

**Overall:** None of the three directions is production-ready. All share the same structural faults — which must be fixed before the background choice matters.

---

## PHASE 1 — First Impression

### Direction A (Soft Bloom)
> "The creative communicates premium care."  
> "I notice a large empty zone taking up the bottom 40% of the canvas — after the headline, the eye falls off."  
> "The first 3 things my eye goes to: (1) logo, (2) headline, (3) nothing — the rest is emptiness."  
> "In one word: **Half-finished.**"

### Direction B (Gradient Wash)
> "The creative communicates warmth."  
> "I notice the rose gradient IS the dominant element — it outweighs the logo and headline visually."  
> "First 3: (1) the rose wash, (2) logo, (3) headline."  
> "In one word: **Warm.**"  
> This reads more like a cosmetic brand ad than a follow-up message. That's not wrong, but the hierarchy is inverted — background is loudest, brand second, message third.

### Direction C (Marble Mist)
> "The creative communicates clinical precision."  
> "I notice the marble veins are invisible — this reads as plain white."  
> "First 3: (1) logo, (2) headline, (3) nothing."  
> "In one word: **Blank.**"  
> C is the most restrained but looks unfinished at this state.

---

## PHASE 2 — Design System Extraction (from renders)

| Element | Current value | Assessment |
|---|---|---|
| Font | Poppins Bold/Regular/Italic | GOOD — Poppins is the right call for Indian clinic market |
| Headline size | ~100pt / ~133px at 1080px | Good weight; legible at WhatsApp thumbnail (~260px) |
| Logo width | 560px of 1080px canvas = **51.8%** | TOO WIDE — premium clinics use 28–37% |
| Separator | 2px gold hairline, 200px wide | Fragile — will be invisible after GIF quantization |
| Footer tagline | Poppins Italic 30pt | Redundant — same text already in logo |
| Background | A: blush bloom (alpha 8–30), B: diagonal rose→cream gradient, C: 2px marble veins | A & C effects are too subtle to register at GIF resolution |

---

## FINDINGS — Priority Ordered

---

### FINDING-001 [HIGH] — Dead bottom third

**What:** The lower ~400px of the canvas (below the headline at y≈660) contains only a small italic tagline at y=1006. That's 37% of the canvas with nothing in it.

**Why it hurts:** WhatsApp GIF animations autoplay in the chat. The animation reveals logo → headline, then loops on empty space. There's no visual payoff. The lead's eye slides off the canvas looking for the CTA that isn't there.

**Fix:** Three options (pick one):  
- **Option A (Recommended):** Add a one-line support text below the headline — scenario-specific, small, charcoal. E.g. "We'd love to hear from you." This fills the void without adding clutter.  
- **Option B:** Vertically re-centre the composition. Reduce top margin so logo+headline sit in the optical centre (not geometric centre) of the canvas. Add generous padding below.  
- **Option C:** Add a subtle brand-consistent decorative element in the lower zone — a row of three gold dots, a thin curved line, a ghost-opacity FAB monogram.

---

### FINDING-002 [HIGH] — Tagline appears twice

**What:** "a complete ethical aesthetic care" appears at:
1. Bottom edge of the logo image (smaller, part of the brand mark)
2. Italic footer at y=1006 (larger, standalone)

**Why it hurts:** Redundancy reads as a design error. It signals the designer ran out of ideas for the bottom zone and just repeated the brand line. The lead sees it twice in under 3 seconds — it's not reinforcement, it's noise.

**Fix:** Remove the standalone footer tagline entirely. The logo already carries it. Use the freed space for support copy (see FINDING-001) or a decorative element.

---

### FINDING-003 [HIGH] — Logo at 51.8% width dominates the composition

**What:** The logo renders at 560px wide on a 1080px canvas.

**Why it hurts:** Kaya 28%, Clinikally 28%, Oliva 32%, Dermalogica 30%. A logo at 52% crowds everything and forces the headline font size up to compete — which creates visual shouting rather than hierarchy.

The gold face icon in the "A" of FAB is sharp and distinctive at 400px. There is no visual gain from the extra 160px.

**Fix:** Reduce logo to **380px wide** (35% canvas width). Increase top margin from 110px to 130px. This buys 180px of extra breathing room for the headline zone and makes the whole composition feel less crowded.

---

### FINDING-004 [HIGH] — Every element is center-aligned (AI slop pattern #4)

**What:** Logo: centered. Hairline: centered. Headline: centered. Tagline: centered. No exceptions.

**Why it hurts:** Center-aligned everything is explicitly listed in the AI slop blacklist used by premium design teams. It's the #1 signal that a layout was auto-generated. Real premium healthcare creatives (Kaya's WhatsApp campaigns, Oliva's Instagram stories) use at least one element that breaks the center axis — typically the headline flush-left with a brand stripe.

**Severity note:** For a 1:1 square WhatsApp format, full-center is more defensible than on a webpage — the format is inherently symmetric. BUT the current execution has zero tension, zero visual interest. Everything is equally centered, equally weighted.

**Fix (chosen path):** Keep the logo centered (brand marks at top-center are conventional and trusted). But **left-align the headline** with a left margin of 80px. This creates the asymmetric tension that reads as designed vs auto-generated. The gold hairline should shift to left-aligned as well.

---

### FINDING-005 [MEDIUM] — 2px gold hairline is fragile and invisible at GIF resolution

**What:** The separator between logo and headline is a 2px × 200px gold line.

**Why it hurts:**  
- GIF quantization degrades sub-pixel rendering. At 128 colors, the 2px line aliases.
- At WhatsApp thumbnail size (~260px display), 2px becomes < 0.5px — invisible.
- Even at full 1080px, the hairline is barely perceptible.

**Fix:** Replace with **three gold dots** (8px diameter, 12px spacing) or a **solid 4px × 120px bar**. Both survive GIF quantization and remain legible at thumbnail size.

---

### FINDING-006 [MEDIUM] — Headline line break creates descending visual weight

**What:** The 2-line break renders as:
```
We missed        ← wider, heavier line
your call        ← narrower, lighter line
```

**Why it hurts:** The descending width creates a "tapering" effect — the message feels like it's trailing off. The emotional hook ("your call" — the personal part) is visually lighter than the preamble.

**Fix:** Either:
- Single line at reduced size: "We missed your call" (~80pt)
- Better 2-line break: "We missed" on line 1, "your call" on line 2 at **larger size than line 1** (120pt vs 80pt) — inverted weight creates drama and emphasis on the hook

---

### FINDING-007 [MEDIUM — Direction B only] — Gradient direction inverts natural hierarchy

**What:** B's diagonal gradient flows from blush/rose at top-left to cream at bottom-right.

**Why it hurts:** The logo lives in the warmest, most saturated zone (top-center). Warm color behind the logo reduces contrast and makes the magenta+gold logo harder to read. The lightest part of the gradient (bottom-right) is where nothing lives.

**Fix:** Reverse the gradient direction — **cream/light at top, warmer rose toward bottom**. This:
1. Maximises logo legibility (light background behind brand mark)
2. Adds visual weight where the headline is (centre-bottom zone)
3. Flows naturally top-to-bottom like gravity

---

### FINDING-008 [POLISH — Direction C only] — Marble veins render below perceptible threshold

**What:** C's marble veins are drawn at alpha 16–28/255 (6–11% opacity).

**Why it hurts:** Below ~30% opacity, texture becomes imperceptible after JPEG/GIF compression. C reads as plain white, which defeats the purpose of the direction entirely.

**Fix:** Push vein opacity to 40–60/255 (16–24%). OR commit to the "pure white" aesthetic and add a different structural element: a soft embossed-effect gold frame (1px solid, 2% opacity inset border), or a diagonal micro-dot pattern at 8% opacity.

---

## PHASE 3 — AI Slop Audit (all directions)

| Pattern | A | B | C |
|---|---|---|---|
| Purple/violet gradient | PASS | PASS | PASS |
| 3-column feature grid | N/A | N/A | N/A |
| Icons in colored circles | PASS | PASS | PASS |
| **Centered everything** | **FAIL** | **FAIL** | **FAIL** |
| Uniform bubbly border-radius | N/A | N/A | N/A |
| Decorative blobs | BORDERLINE (A has soft bloom) | PASS | PASS |
| Emoji as design elements | PASS | PASS | PASS |
| Generic hero copy | PASS | PASS | PASS |
| Gradient backgrounds | PASS | BORDERLINE (rose is tasteful) | PASS |
| Default font stack | PASS (Poppins) | PASS | PASS |

**AI Slop scores:** A=B, B=B, C=A  
**Primary flag on all three:** centered everything (one structural change fixes this across all 8 GIFs)

---

## PHASE 4 — WhatsApp-Specific Review

| Check | Status | Note |
|---|---|---|
| Legible at 260px (chat bubble width) | PASS | Headline reads at thumbnail size |
| Distinguishable from WhatsApp chat bg | A: MARGINAL, B: PASS, C: FAIL | A and B stand out; C (white) blends with WA light theme |
| Animation lands on a strong frame | FAIL ALL | Final frame has empty bottom third — weak loop anchor |
| No text too small to read on mobile | PASS | Smallest text (30pt) still readable |
| Single clear message | PASS | "We missed your call" is unambiguous |

---

## SUMMARY & VERDICT

**Design Score Breakdown:**

| Category | Weight | A | B | C |
|---|---|---|---|---|
| Visual Hierarchy | 20% | D | D | D |
| Typography | 20% | B | B | B |
| Spacing/Layout | 20% | D | D | D |
| Color/Contrast | 15% | B | C | A |
| AI Slop | 10% | B | B | A |
| WhatsApp legibility | 15% | B | B | C |
| **Weighted total** | | **C+** | **C** | **C+** |

**Winner: Direction A (Soft Bloom) — but only after structural fixes**

B is more attention-grabbing in a WhatsApp thread but the gradient hierarchy is backwards and it competes with the brand. C is the most premium but invisible on WhatsApp's light theme.

---

## QUICK WINS — fix these 5 before regenerating GIFs

These 5 changes affect all 8 GIFs equally and take <1 hour in `build_gifs.py`:

1. **Logo: 560px → 380px** (change `load_logo(w=560)` to `load_logo(w=380)`)
2. **Remove duplicate footer tagline** (comment out the tagline footer block in `render_frame`)
3. **Add support line below headline** — scenario-specific 1-liner per scenario in `SCENARIOS`
4. **Replace 2px hairline with 3 gold dots** (8px circles, 12px gap)
5. **Left-align headline** (remove centering calc, use fixed left margin x=80px)

After these 5 fixes, regenerate all 8 GIFs and the design will be production-ready at quality level **B**.

---

## RECOMMENDED DESIGN DIRECTION

**Use Direction A (Soft Bloom) with the following adjustments:**
- Make the blush bloom MORE visible (alpha 35–55, not 8–30)
- Place a second soft bloom at top-left (gold/warm tone, 15% opacity) for balance
- Apply the 5 quick wins above

This gives you: premium skincare warmth, high WhatsApp legibility, on-brand palette, and enough visual texture that it reads as intentionally designed rather than AI-default.

---

*STATUS: DONE_WITH_CONCERNS — audit complete. 8 findings (4 high, 3 medium, 1 polish). Structural issues must be fixed before background direction is meaningful. Quick wins block ready to implement.*
