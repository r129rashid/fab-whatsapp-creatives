# Project Progress — FAB Skin Hair & Laser Clinic WhatsApp Creative Pack

_Last updated: 12 May 2026_

---

## What we set out to build

A complete WhatsApp tele-caller follow-up creative pack for FAB Skin Hair & Laser Clinic:
8 animated creatives (1080×1080, WhatsApp-safe) + matching copy scripts covering the 8 most common lead re-engagement scenarios, ready for TeleCRM automation.

---

## What we have accomplished ✅

### Brand Discovery
- Located and analysed the only brand asset: `Fab Logo.jpg`
- Extracted palette: Magenta `#8E1B5C` (primary), Gold `#C4A23F` (accent), Charcoal `#2B2B2B`, Cream `#FAF7F2`
- Clinic name: **FAB Skin Hair & Laser Clinic** | Tagline: "a complete ethical aesthetic care"

### Copy — 8 Message Scripts
All 8 WhatsApp messages written, reviewed, and finalised in `scripts/messages.json`:
- ≤ 35 words each (actual: 30–33 words)
- `{{name}}` + `{{campaign}}` placeholders throughout
- Single CTA: Reply **YES** (WhatsApp Quick Reply button — NOT in creative visual)
- DCGI / ASCI compliant (no medical claims, no guaranteed results)

| # | Scenario | Trigger |
|---|---|---|
| 1 | No answer / call not picked | 2 missed outbound calls |
| 2 | Call disconnected mid-conversation | Call < 30s, disposition = dropped |
| 3 | Lead asked to be called later | Callback requested |
| 4 | Showed interest but didn't book | Call > 60s, no consult booked |
| 5 | Price objection | Tag = price objection |
| 6 | Comparing with competitors | Tag = comparing |
| 7 | No-show after booking | Appointment = no-show |
| 8 | Cold / dormant (7+ days silence) | 7 days no activity |

### Design Review (via /design-review)
Full audit across 3 proposed directions, 8 findings resolved:
- **Direction chosen: A — Soft Bloom** (blush glow on cream, boosted opacity)
- Audit report: `design-preview/audit/design-audit-fab-whatsapp.md`

### v0.1 GIFs (baseline render)
- All 8 GIFs rendered, ~485 KB each
- Functional baseline with 4 HIGH-severity design issues identified in audit

### v0.2 GIFs (design audit fixes)
5 audit fixes applied: logo resized (560→380px), Soft Bloom background, 3 gold dot separator, left-aligned headline, per-scenario support line. All under 2 MB.

### v0.3 GIFs + MP4s (current — production ready) ✅

Three user-requested changes implemented:

#### 1. WhatsApp animation fix → MP4 export
WhatsApp does **not** animate `.gif` files sent as image attachments — this is a platform-level limitation. Animated content must be delivered as MP4 video. The renderer now outputs both formats per scenario:
- `creatives/*.gif` — for preview, web, email
- `creatives/*.mp4` — **use this for WhatsApp / TeleCRM** (320–385 KB each)

For TeleCRM: upload `.mp4` files as **Video** message type (not Image/GIF). The video autoplays inline, plays once through the 4-second reveal, and holds on the last frame.

#### 2. Center alignment
All elements switched from left-aligned to horizontally centered: headline, body text, support line, and separator dots. Logo was already centered.

#### 3. Richer body copy
Body text updated to be warmer and more complete across all 8 scenarios:

| # | Headline | Body line 1 | Body line 2 | Support line |
|---|---|---|---|---|
| 01 | We missed your call | We tried reaching you but missed you today. | Reply YES — we'll call you right back. | We'd love to hear from you. |
| 02 | Oops, call dropped | Our call got disconnected midway — sorry! | Reply YES to continue from where we stopped. | Let's continue where we left off. |
| 03 | Time to chat? | You'd asked us to reach back out — we're here! | Reply YES to confirm a convenient time. | Your time, your pace. |
| 04 | Still thinking it over? | Your consultation is just one step away. | Reply YES and we'll guide you through it. | No pressure — we're here for you. |
| 05 | Smart options for you | We have flexible EMI plans and special offers. | Reply YES to find the best plan for you. | Flexible plans this month. |
| 06 | Why patients pick FAB | Thousands trust FAB for certified, ethical care. | Reply YES for a transparent, no-pressure chat. | Trusted by thousands in your city. |
| 07 | We missed you today | We held your slot open — hope you're doing well. | Reply YES to reschedule at your convenience. | Your slot is always here. |
| 08 | Have we lost touch? | It's been a while — we've been thinking of you. | Reply YES whenever you're ready to reconnect. | No rush. We're here when you are. |

#### v0.3 file sizes

| File | GIF | MP4 |
|---|---|---|
| scenario-01-no-answer | 1495.5 KB | 355.3 KB |
| scenario-02-disconnected | 1494.5 KB | 352.5 KB |
| scenario-03-call-later | 1407.6 KB | 321.8 KB |
| scenario-04-didnt-book | 1576.6 KB | 357.0 KB |
| scenario-05-price | 1573.3 KB | 357.8 KB |
| scenario-06-comparing | 1619.0 KB | 383.7 KB |
| scenario-07-no-show | 1516.5 KB | 369.4 KB |
| scenario-08-dormant | 1580.4 KB | 366.0 KB |

All GIFs under 2 MB. All MP4s under 400 KB.

### Git & GitHub
Project initialised as a git repository and published to GitHub:
- Repo: `https://github.com/r129rashid/fab-whatsapp-creatives`
- Latest commit: `b02ee9c` (v0.3)
- All Python source, assets, GIFs, MP4s, and docs committed

---

## Current State 🎯

**v0.3 is production-ready.** All creatives are rendered, QC passed visually. MP4 files are ready for TeleCRM upload. GIFs are available for web/preview use.

---

## What's next 🔜

### Immediate — before going live
1. **Phone test with MP4**: send one `.mp4` from `creatives/` to a WhatsApp contact, verify:
   - Video autoplays inline in chat
   - Reveal animation plays through cleanly (4 seconds)
   - Holds on final frame after playing
   - Text legible on light and dark WhatsApp themes
2. **TeleCRM upload**:
   - Upload each `creatives/scenario-XX-*.mp4` as a **Video** template (not Image/GIF)
   - Import `scripts/messages.json` as template-text library
   - Map `{{name}}` → lead First Name, `{{campaign}}` → Campaign/Source field
   - Set rate-limit guard: max 1 creative per lead per 6 hours, max 2 per 24 hours
   - Configure opt-out trap: if lead replies STOP/NO, flag and exclude from automation

### Optional / future
3. **Hinglish A/B variants** — alternative copy for scenarios 03, 05, 08 (edit `messages.json`, no GIF regeneration needed unless headlines change)
4. **Scenario 9+ expansion** — e.g. post-consultation follow-up, seasonal campaign push
5. **Dark-theme MP4 variant** — dark background set for WhatsApp dark mode users

---

## File Map

```
.
├── Fab Logo.jpg                     # brand asset (input only)
├── CLAUDE.md                        # project context for Claude sessions
├── README.md                        # tele-caller team playbook
├── progress.md                      # this file
├── preview.html                     # review all 8 GIFs side-by-side in browser
├── assets/fonts/                    # Poppins TTFs (Bold, Regular) — do not delete
├── creatives/
│   ├── scenario-01-no-answer.gif    # 1.5 MB — for web/preview
│   ├── scenario-01-no-answer.mp4    # 355 KB — USE THIS FOR WHATSAPP
│   ├── ... (× 8 scenarios)
├── scripts/
│   ├── build_gifs.py                # renderer v0.3 — edit here, re-run to regenerate
│   ├── messages.md                  # human-readable copy + triggers
│   └── messages.json                # CRM-import JSON
└── design-preview/
    ├── A-soft-bloom.png / B / C     # design direction mockups
    ├── index.html                   # direction comparison page
    └── audit/
        └── design-audit-fab-whatsapp.md  # full /design-review report
```

---

## Open Questions
None blocking. All decisions resolved:
- ✅ CTA destination: WhatsApp Quick Reply button (not in creative)
- ✅ Renderer: Python (Pillow) + ffmpeg for MP4
- ✅ Language: English (Hinglish A/B optional)
- ✅ Design direction: A — Soft Bloom, center-aligned, v0.3
- ✅ WhatsApp delivery format: MP4 video (not GIF image)
- ✅ GitHub: `r129rashid/fab-whatsapp-creatives`
