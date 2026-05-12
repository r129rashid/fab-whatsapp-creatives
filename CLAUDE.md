# CLAUDE.md — FAB Skin Hair & Laser Clinic WhatsApp Creative Pack

Project context for Claude Code sessions. Read this at the start of every session.

---

## Project in one sentence

Build and maintain a pack of 8 animated WhatsApp creatives for FAB Skin Hair & Laser Clinic's tele-caller follow-up automation, rendered by a single Python script and delivered as MP4 video for WhatsApp playback.

---

## Current status

**v0.3 — production-ready** (as of 12 May 2026).
MP4 + GIF files generated for all 8 scenarios. Centered layout. Visual QC passed.
Next action: phone test with MP4 → TeleCRM upload as Video type.
GitHub: `https://github.com/r129rashid/fab-whatsapp-creatives`

---

## Brand

| Element | Value |
|---|---|
| Clinic name | FAB Skin Hair & Laser Clinic |
| Tagline | a complete ethical aesthetic care |
| Primary | Magenta `#8E1B5C` |
| Accent | Gold `#C4A23F` |
| Text | Charcoal `#2B2B2B` |
| Background | Soft Bloom: rose blush glow (bottom-right, alpha 55) + gold glow (top-left, alpha 38) on cream `#FAF7F2` |
| Font | Poppins Bold 86pt (headline), Regular 40pt (body), Regular 34pt (support line) |
| Logo file | `Fab Logo.jpg` — 553×225px source, white bg auto-removed by renderer |

---

## Architecture

```
scripts/build_gifs.py     ← single renderer — always edit here
scripts/messages.json     ← WhatsApp message copy source of truth
scripts/messages.md       ← human-readable version of messages.json
assets/fonts/             ← Poppins-Bold.ttf, Poppins-Regular.ttf (do NOT delete)
creatives/*.gif           ← GIF output — for web/preview/email
creatives/*.mp4           ← MP4 output — USE THESE FOR WHATSAPP / TeleCRM
preview.html              ← browser review page for all 8 GIFs
```

**To regenerate all 8 creatives (GIF + MP4):**
```bash
cd "/Users/rabirashid/Rabi AI Projects/Claude whatsapp creatives"
python3 scripts/build_gifs.py
# requires: pip install Pillow
# requires: brew install ffmpeg   (for MP4 export)
```

---

## Creative spec

| Property | Value |
|---|---|
| Canvas | 1080×1080 px (1:1, WhatsApp-safe square) |
| Total duration | 4.0 s (1 s static hold + 3 s reveal animation) |
| Playback | Once — holds on last frame |
| GIF: file size | 1.4–1.6 MB (under WhatsApp 2 MB limit) |
| MP4: file size | 320–385 KB (H.264, yuv420p, no audio) |
| **WhatsApp delivery** | **Use MP4 as Video message type in TeleCRM** |
| CTA in creative | None — "Reply YES" is a WhatsApp Quick Reply button in TeleCRM |

**Why MP4, not GIF:**
WhatsApp does not animate `.gif` files sent as image attachments. Animated content must be sent as MP4 video (`message type: video`). The MP4 autoplays inline in chat, plays once, and holds on the last frame.

---

## Design decisions (locked — do not change without /design-review)

| Decision | Rationale |
|---|---|
| Background: Soft Bloom | Most legible on WA light theme; Kaya/Oliva aesthetic; audit winner |
| Bloom: rose bottom-right (alpha 55) + gold top-left (alpha 38) | Two-bloom balance per audit recommendation; boosted from v0.1 |
| Logo: centered, 380px (35% canvas) | Premium clinics use 28–37%; 52% was too dominant |
| Logo top margin: 130px | Breathing room at top |
| All text: center-aligned | User preference (v0.3); consistent axis with centered logo |
| Separator: 3 gold dots (8px diameter, 12px gap), centered | Survives GIF quantization at thumbnail size; hairline does not |
| Headline: Poppins Bold 86pt, magenta | Strong visual hook at thumbnail size |
| Body: Poppins Regular 40pt, charcoal | Legible at WhatsApp chat bubble width (~260px) |
| Support line: Regular 34pt, charcoal 70% opacity | Fills dead bottom zone; subordinate to body text |
| HOLD_FRAMES=10 prepended | Frame 0 = complete design = correct WA thumbnail; fixes blank-first-frame |
| loop=1 (play once) | Plays reveal animation once, holds on final frame |
| No CTA pill in creative | WhatsApp Quick Reply button handles this in TeleCRM |
| No footer tagline | Already in logo; removing eliminates audit-flagged redundancy |

---

## Layout positions (v0.3, centered, for reference when editing render_frame)

Computed dynamically from `logo.height`. Approximate values with 380px logo (height ≈ 155px):

| Element | Approx y | Alignment |
|---|---|---|
| Logo | 130 | Centered horizontally |
| Separator dots (centre) | ~321 | Centered (3-dot group) |
| Headline | ~375 | Centered |
| Body line 1 | ~517 | Centered |
| Body line 2 | ~581 | Centered |
| Support line | ~653 | Centered |
| Bottom breathing room | ~653–1080 | Intentional luxury whitespace |

---

## Animation timings (frame index at 10 fps, AFTER hold frames)

| Element | Fade-in range | Extra |
|---|---|---|
| Logo | 0–6 | — |
| Separator dots | 3–9 | — |
| Headline | 7–15 | +12px upward slide |
| Body text | 12–20 | — |
| Support line | 17–24 | — |
| Hold (fully visible) | 24–29 | — |

---

## Scenarios

| ID | Scenario | Headline | Trigger |
|---|---|---|---|
| 01 | No answer / call not picked | We missed your call | 2 missed outbound calls (same day) |
| 02 | Call disconnected | Oops, call dropped | Call < 30s, disposition = dropped |
| 03 | Asked to call later | Time to chat? | Disposition = callback requested |
| 04 | Interested, didn't book | Still thinking it over? | Call > 60s, no consult booked; 24h later |
| 05 | Price objection | Smart options for you | Tag = price objection / expensive / budget |
| 06 | Comparing competitors | Why patients pick FAB | Tag = comparing / mentions other clinic |
| 07 | No-show after booking | We missed you today | Appointment = no-show; 2h after missed slot |
| 08 | Cold / dormant | Have we lost touch? | No activity for 7 consecutive days |

Full body copy and support lines are in `SCENARIOS` list in `scripts/build_gifs.py` and the WhatsApp message scripts are in `scripts/messages.json`.

---

## Content rules (non-negotiable)

- Max 35 words per WhatsApp message (`messages.json`)
- Always include `{{name}}` and `{{campaign}}` placeholders
- No medical claims, no guaranteed results — DCGI/ASCI compliant
- End every message with `— FAB Skin Hair & Laser Clinic`
- Single CTA only: Reply **YES**
- Sending window: 10 AM–8 PM IST only

---

## TeleCRM delivery checklist

- [ ] Upload `creatives/scenario-XX-*.mp4` as **Video** template (not Image/GIF)
- [ ] Import `scripts/messages.json` as template-text library
- [ ] Map `{{name}}` → lead First Name field
- [ ] Map `{{campaign}}` → Campaign / Source field
- [ ] Rate-limit guard: max 1 creative per lead per 6 hours, max 2 per 24 hours
- [ ] Opt-out trap: STOP / NO reply → flag and exclude from all automation
- [ ] Sending hours rule: 10 AM–8 PM IST only

---

## Skill routing

- Visual design changes → `/design-review`
- New feature or copy changes → `/brainstorming` first
- Bugs in `build_gifs.py` → `/investigate`
- Shipping / PR → `/ship`

---

## What NOT to do

- Do not send `.gif` files to WhatsApp expecting animation — use `.mp4`
- Do not add a CTA button inside the creative visuals
- Do not invent clinic names, doctor names, or testimonials
- Do not change brand colours or fonts without re-running `/design-review`
- Do not delete `assets/fonts/` — Poppins TTFs are required by the renderer
- Do not edit GIF/MP4 files directly — always edit `build_gifs.py` and regenerate
- Do not commit secrets or API keys

---

## Reference files

- `progress.md` — full project history, current state, next steps
- `design-preview/audit/design-audit-fab-whatsapp.md` — /design-review report (8 findings)
- `scripts/messages.json` — canonical WhatsApp message copy for all 8 scenarios
- GitHub: `https://github.com/r129rashid/fab-whatsapp-creatives`
