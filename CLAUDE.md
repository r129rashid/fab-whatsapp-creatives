# CLAUDE.md — FAB Skin Hair & Laser Clinic WhatsApp Creative Pack

Project context for Claude Code sessions. Read this at the start of every session.

---

## Project in one sentence

Build and maintain a pack of 8 animated WhatsApp GIF creatives for FAB Skin Hair & Laser Clinic's tele-caller follow-up automation, driven by a single Python renderer and a JSON content file.

---

## Current status

**v0.2 — production-ready** (as of 12 May 2026).
All 5 design-review audit fixes applied. 8 GIFs generated, all under 2 MB. Visual QC passed.
Next action: phone test → TeleCRM upload.

---

## Brand

| Element | Value |
|---|---|
| Clinic name | FAB Skin Hair & Laser Clinic |
| Tagline | a complete ethical aesthetic care |
| Primary | Magenta `#8E1B5C` |
| Accent | Gold `#C4A23F` |
| Text | Charcoal `#2B2B2B` |
| Background | Soft Bloom: rose blush glow (bottom-right) + gold glow (top-left) on off-white `#FAF7F2` |
| Font | Poppins Bold 86pt (headlines), Regular 40pt (body), Regular 34pt (support line) |
| Logo file | `Fab Logo.jpg` — 553×225px source, white background (auto-removed by renderer) |

---

## Architecture

```
scripts/build_gifs.py     ← single renderer — always edit here
scripts/messages.json     ← content source of truth (text, triggers, word counts)
scripts/messages.md       ← human-readable version of messages.json
assets/fonts/             ← Poppins TTF files (do NOT delete)
creatives/                ← 8 output GIFs (regenerate via build_gifs.py)
preview.html              ← review page (open in browser after regeneration)
```

**To regenerate all 8 GIFs:**
```bash
cd "/Users/rabirashid/Rabi AI Projects/Claude whatsapp creatives"
python3 scripts/build_gifs.py
```

**To regenerate a single scenario**, edit only its dict in `SCENARIOS` inside `build_gifs.py`, then re-run. All 8 render in ~60 seconds total.

---

## GIF spec

- Canvas: 1080×1080 px (1:1, WhatsApp-safe square)
- Duration: 3 seconds, 10 fps, 30 frames, loops infinitely
- File size: < 2 MB each (v0.2 actual: 1.2–1.5 MB due to Soft Bloom gradient)
- Format: GIF with 128-color shared palette, disposal=1, optimize=True
- **No CTA pill in the GIF** — "Reply YES" is a WhatsApp Quick Reply button set in TeleCRM

---

## Design decisions (locked — do not change without /design-review)

| Decision | Rationale |
|---|---|
| Background: Soft Bloom | Most legible on WA light theme; Kaya/Oliva aesthetic; audit winner over gradient and marble |
| Bloom: rose at bottom-right (alpha 55), gold at top-left (alpha 38) | Boosted from v0.1 (alpha 8–30) for visible texture; two-bloom balance per audit recommendation |
| Logo width: 380px (35% canvas) | Premium clinics use 28–37%; 560px/52% was too dominant |
| Logo top margin: 130px | Slightly more breathing room than v0.1 (110px) after logo shrink |
| Headline: Poppins Bold 86pt, left-aligned at x=80px | Breaks centered-everything AI slop; editorial tension |
| Separator: 3 gold dots (8px diameter, 12px gap), left-aligned at x=80px | 2px hairline doesn't survive GIF quantization at thumbnail size |
| Body text: Regular 40pt, left-aligned at x=80px | Consistent left axis with headline |
| Support line: Regular 34pt, charcoal 70% opacity, left-aligned | Fills dead bottom zone; per-scenario 1-liner (not a repeated tagline) |
| No footer tagline | Already in logo; removing eliminates redundancy flagged in audit |
| No CTA pill | WhatsApp Quick Reply button handles this in TeleCRM — cleaner GIF, larger for animation |

---

## Layout positions (v0.2, for reference when editing render_frame)

These are computed dynamically in code from `logo.height`, but approximate values with the 380px logo (height ≈ 155px):

| Element | Approx y |
|---|---|
| Logo top | 130 |
| Logo bottom | ~285 |
| Separator dots (centre) | ~321 |
| Headline top | ~375 |
| Body line 1 | ~517 |
| Body line 2 | ~581 |
| Support line | ~653 |
| Bottom breathing room | ~653–1080 (intentional) |

---

## Animation timings (frame index, 10 fps)

| Element | Fade-in range | Extra |
|---|---|---|
| Logo | 0–6 | — |
| Separator dots | 3–9 | — |
| Headline | 7–15 | +12px slide-up |
| Body | 12–20 | — |
| Support line | 17–24 | — |

---

## Content rules (non-negotiable)

- Max 35 words per WhatsApp message
- Always include `{{name}}` and `{{campaign}}` placeholders
- No medical claims, no guaranteed results — DCGI/ASCI compliant
- End every message with `— FAB Skin Hair & Laser Clinic`
- Single CTA only: Reply **YES**
- Sending window: 10 AM–8 PM IST only

---

## Scenarios

| ID | Scenario | GIF headline | Support line | Trigger |
|---|---|---|---|---|
| 01 | No answer / call not picked | We missed your call | We'd love to hear from you. | 2 missed outbound calls (same day) |
| 02 | Call disconnected | Oops, call dropped | Let's continue where we left off. | Call < 30s, disposition = dropped |
| 03 | Asked to call later | Time to chat? | Your time, your pace. | Disposition = callback requested |
| 04 | Interested, didn't book | Still thinking it over? | No pressure — we're here for you. | Call > 60s, no consult booked; 24h later |
| 05 | Price objection | Smart options for you | Flexible plans this month. | Tag = price objection / expensive / budget |
| 06 | Comparing competitors | Why patients pick FAB | Trusted by thousands in your city. | Tag = comparing / mentions other clinic |
| 07 | No-show after booking | We missed you today | Your slot is always here. | Appointment = no-show; 2h after missed slot |
| 08 | Cold / dormant | Have we lost touch? | No rush. We're here when you are. | No activity for 7 consecutive days |

---

## Skill routing

When the user's request matches an available skill, invoke it via the Skill tool.

- Visual design changes or polish → `/design-review`
- New feature or content changes → `/brainstorming` first
- Bugs in build_gifs.py → `/investigate`
- Shipping / PR → `/ship`

---

## What NOT to do

- Do not add a CTA pill or button inside the GIF visuals
- Do not invent clinic names, doctor names, or testimonials
- Do not use stock photos of real people
- Do not change brand colours, fonts, or layout without re-running `/design-review`
- Do not delete `assets/fonts/` — Poppins TTFs are required by the renderer
- Do not commit secrets or API keys
- Do not edit GIFs directly — always edit `build_gifs.py` and regenerate

---

## Reference files

- `progress.md` — current state, accomplished work, next steps
- `design-preview/audit/design-audit-fab-whatsapp.md` — full /design-review audit (8 findings)
- `scripts/messages.json` — canonical copy source for all 8 messages
