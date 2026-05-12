# FAB Skin Hair & Laser Clinic — WhatsApp Tele-caller Messages

All messages are ≤ 35 words, DCGI/ASCI-compliant (no medical claims, no guaranteed results), use placeholders `{{name}}` and `{{campaign}}`, and end with the clinic signature.

**Single CTA across the pack:** Reply **YES** → tele-caller is notified for callback.

---

## 1 — No answer / call not picked
**Creative:** `creatives/scenario-01-no-answer.gif`
**Trigger:** Outbound call → no answer (after 2 attempts in the same day)

> Hi {{name}}, we just tried reaching you about your {{campaign}} enquiry — missed you! Reply **YES** and our consultant will call back at your convenient time. — FAB Skin Hair & Laser Clinic

---

## 2 — Call disconnected mid-conversation
**Creative:** `creatives/scenario-02-disconnected.gif`
**Trigger:** Call duration < 30 s and disposition = "disconnected" / "call dropped"

> Hi {{name}}, looks like our call dropped midway. Apologies! Reply **YES** and we'll continue right where we left off on your {{campaign}} query. — FAB Skin Hair & Laser Clinic

---

## 3 — Lead asked to be called later
**Creative:** `creatives/scenario-03-call-later.gif`
**Trigger:** Disposition = "callback requested"; send 30 min before the lead's preferred slot

> Hi {{name}}, a gentle reminder — you'd asked us to call back for {{campaign}}. Reply **YES** with a convenient time, and our consultant will reach out. — FAB Skin Hair & Laser Clinic

---

## 4 — Showed interest but didn't book
**Creative:** `creatives/scenario-04-didnt-book.gif`
**Trigger:** Lead engaged (call > 60 s) but did not confirm a consultation; send 24 h after the call

> Hi {{name}}, your interest in {{campaign}} deserves a proper consultation with our experts. Reply **YES** and we'll help you take the next step at your pace. — FAB Skin Hair & Laser Clinic

---

## 5 — Price objection / "too expensive"
**Creative:** `creatives/scenario-05-price.gif`
**Trigger:** Disposition tag = "price objection" or notes contain "expensive / costly / budget"

> Hi {{name}}, we hear you on budget. Easy EMI options and seasonal offers on {{campaign}} are available this month. Reply **YES** to know more. — FAB Skin Hair & Laser Clinic

---

## 6 — Comparing with competitors
**Creative:** `creatives/scenario-06-comparing.gif`
**Trigger:** Disposition tag = "comparing" or notes mention other clinic names

> Hi {{name}}, before you decide on {{campaign}}, here's why patients choose FAB — certified specialists, advanced technology, ethical care. Reply **YES** for a no-pressure consultation. — FAB Skin Hair & Laser Clinic

---

## 7 — No-show after booking
**Creative:** `creatives/scenario-07-no-show.gif`
**Trigger:** Booked appointment marked "no-show"; send same day, 2 h after the missed slot

> Hi {{name}}, we kept your slot open today and missed seeing you. Hope all is well! Reply **YES** to reschedule your {{campaign}} consultation at your convenience. — FAB Skin Hair & Laser Clinic

---

## 8 — Cold / dormant (7+ days silence)
**Creative:** `creatives/scenario-08-dormant.gif`
**Trigger:** No reply or call disposition for 7 consecutive days

> Hi {{name}}, it's been a while! Still thinking about {{campaign}}? Whenever you're ready, our team is just one message away. Reply **YES** to reconnect. — FAB Skin Hair & Laser Clinic
