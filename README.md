# FAB Skin Hair & Laser Clinic — WhatsApp Tele-caller Creative Pack

A drop-in pack of 8 on-brand animated GIFs and matching message scripts for TeleCRM-driven WhatsApp follow-ups.

> _a complete ethical aesthetic care_

---

## What's in this pack

```
.
├── Fab Logo.jpg                     # source brand asset
├── assets/fonts/                    # Poppins TTFs used by the renderer
├── creatives/
│   ├── scenario-01-no-answer.gif    # ~485 KB each, 1080×1080, 3s loop
│   ├── scenario-02-disconnected.gif
│   ├── scenario-03-call-later.gif
│   ├── scenario-04-didnt-book.gif
│   ├── scenario-05-price.gif
│   ├── scenario-06-comparing.gif
│   ├── scenario-07-no-show.gif
│   └── scenario-08-dormant.gif
├── scripts/
│   ├── messages.md                  # human-readable copy + triggers
│   ├── messages.json                # CRM-import-ready (placeholders, triggers, word counts)
│   └── build_gifs.py                # generator (re-run to regenerate creatives)
├── preview.html                     # open in browser to review all 8 side-by-side
└── README.md                        # this file
```

All creatives are **1080 × 1080** (WhatsApp-safe square), under **525 KB each**, loop seamlessly, and remain legible on both light and dark WhatsApp themes.

---

## When to send which creative

| # | Scenario | Trigger to fire from TeleCRM |
|---|---|---|
| 01 | No answer / call not picked | Outbound call → no answer after **2 attempts in the same day**. Send 5–10 min after the second miss. |
| 02 | Call disconnected mid-call | Call duration **< 30 s** AND disposition = `disconnected` / `call dropped`. Send within 2 min. |
| 03 | Asked to be called later | Disposition = `callback requested`. Send **30 min before** the lead's preferred slot. |
| 04 | Interested but didn't book | Call duration **> 60 s** AND no consultation booked. Send **24 h after** the call. |
| 05 | Price objection | Disposition tag = `price objection` OR notes contain `expensive`, `costly`, `budget`. Send within 1 h of call end. |
| 06 | Comparing with competitors | Disposition tag = `comparing` OR notes mention another clinic name. Send within 1 h. |
| 07 | No-show after booking | Confirmed appointment marked `no-show`. Send **2 h after** the missed slot. |
| 08 | Cold / dormant lead | No reply or call activity for **7 consecutive days**. Send once; do not stack. |

**Sending hours:** 10:00 AM – 8:00 PM IST only. Skip Sundays unless the lead has actively engaged on a Sunday before.

---

## TeleCRM setup (one-time)

1. Upload each `creatives/scenario-XX-*.gif` as a **WhatsApp media template** in TeleCRM.
2. Import `scripts/messages.json` as your template-text library (the `id` field maps 1:1 with the GIF filename without extension).
3. In each automation rule, attach the matching `creative` + `text`; ensure `{{name}}` and `{{campaign}}` are mapped to the lead fields **First Name** and **Campaign / Source**.
4. Add a **rate-limit guard**: no more than 1 of these creatives to the same lead per 6 hours, and no more than 2 per lead per 24 hours.
5. Add an **opt-out trap**: if a lead replies STOP / NO / "don't call", flag and exclude from all further automation.

---

## Do's

- **Personalise.** Always pass a real `{{name}}` — never send "Hi friend" or leave the placeholder unresolved.
- **One CTA per send.** All 8 messages funnel to a single `Reply YES`. Don't add a second link or number.
- **Respect the time window.** 10 AM–8 PM IST. Anything else feels intrusive on WhatsApp.
- **Match the scenario.** A "price objection" message to a no-show lead breaks trust. Use the trigger table above.
- **Watch the funnel.** Scenarios 04, 05, 06 should convert best — track reply rate per scenario weekly.

## Don'ts

- **No medical claims.** Never write "guaranteed", "permanent", "100%", "no side-effects", or specific outcomes. The pack as shipped is DCGI / ASCI compliant — keep it that way.
- **No stacking.** Don't send two GIFs back-to-back in the same chat thread.
- **No resending within 6 hours.** A lead who didn't reply once won't reply twice in 30 minutes.
- **No invented testimonials.** Even within the GIFs, never add "Anjali, 32, loved her results" — none of the assets contain this; don't add it.
- **No price quotes in copy.** The pack hints at "EMI / offers" but never lists numbers — pricing is the tele-caller's job, on the call.

---

## A/B testing suggestions

Once you have ≥ 500 sends per scenario, start splitting. Try one variable at a time:

| Variable | Variant A | Variant B | Decision metric |
|---|---|---|---|
| **CTA keyword** | `Reply YES` | `Reply 1` | Reply rate within 24 h |
| **Send time** | 10:30 AM | 6:30 PM | Reply rate per slot |
| **Tone (Scenario 05)** | "We hear you on budget…" | "Aapke budget mein perfect plan available hai" | Reply + conversion rate |
| **Headline (Scenario 04)** | "Still thinking it over?" | "Your slot is reserved" | Click-through to booking |
| **CTA destination** _(future)_ | Reply YES | Booking link | Booked consults per 100 sends |

Hold each test for at least **2 weeks** or **1,000 sends per arm**, whichever comes first, before declaring a winner.

---

## Regenerating the creatives

The GIFs are produced by a single self-contained Python script. To re-render (e.g., after changing a headline or colour):

```bash
cd "/Users/rabirashid/Rabi AI Projects/Claude whatsapp creatives"
python3 scripts/build_gifs.py
```

Requires `Pillow`, `imageio`, `numpy` and the four Poppins TTFs in `assets/fonts/`. To tweak copy, edit the `SCENARIOS` list at the top of `scripts/build_gifs.py`.

---

## Compliance note

This pack is designed to stay inside DCGI (Drugs and Cosmetics) and ASCI (Advertising Standards Council of India) guardrails for aesthetic clinic advertising:

- No before/after imagery
- No claims of guaranteed results, permanent fixes, or specific outcomes
- No medical advice or diagnostic language
- No reference to procedure efficacy percentages
- All offers are described in soft language ("seasonal offers available") — the tele-caller is responsible for accurate quotes on the call
- Opt-out keyword respected on every send

If the clinic's regulatory advisor flags any wording, edit `scripts/messages.json` and re-import; the GIFs do not need regenerating unless a headline changes.

---

## Contact

Marketing & creative ownership lives with the FAB marketing team. The generator script (`build_gifs.py`) is the source of truth — any visual change should be made there first, with the GIF re-rendered and the preview reviewed before pushing to TeleCRM.
