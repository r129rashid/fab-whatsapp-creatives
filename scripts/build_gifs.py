"""
build_gifs.py — FAB Skin Hair & Laser Clinic WhatsApp GIF Generator
====================================================================
Renders 8 animated GIF creatives (1080×1080 px) for WhatsApp tele-caller
follow-up campaigns. Each GIF covers one lead re-engagement scenario.

Design spec (v0.2):
  - Canvas      : 1080×1080 px, 1:1 square (WhatsApp-safe)
  - Duration    : 3 seconds, 10 fps, 30 frames, infinite loop
  - File size   : 1.2–1.5 MB each (under WhatsApp's 2 MB practical limit)
  - Background  : Soft Bloom — cream base with rose glow (bottom-right) and
                  gold glow (top-left), implemented via Gaussian-blurred RGBA
                  ellipses composited over the cream canvas
  - Logo        : Centered, 380 px wide (35% of canvas)
  - Separator   : Three 8 px gold dots, left-aligned
  - Headline    : Poppins Bold 86pt, left-aligned, magenta
  - Body text   : Poppins Regular 40pt, left-aligned, charcoal
  - Support line: Poppins Regular 34pt, left-aligned, charcoal 70% opacity
  - CTA         : NOT in the GIF — "Reply YES" is a WhatsApp Quick Reply
                  button configured in TeleCRM

Animation sequence (frame index at 10 fps):
  Frame 0–6   : Logo fades in
  Frame 3–9   : Gold separator dots fade in
  Frame 7–15  : Headline fades in + slides up 12 px
  Frame 12–20 : Body text fades in
  Frame 17–24 : Support line fades in
  Frame 24–30 : All elements fully visible (hold / loop anchor)

Usage:
  python3 scripts/build_gifs.py

Requirements:
  pip install Pillow imageio numpy
  assets/fonts/Poppins-{Bold,SemiBold,Regular,Italic}.ttf must exist
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

# BASE resolves to the project root regardless of where the script is called from
BASE = Path(__file__).resolve().parent.parent
LOGO_PATH = BASE / "Fab Logo.jpg"
FONT_DIR = BASE / "assets" / "fonts"
OUT_DIR = BASE / "creatives"

# ---------------------------------------------------------------------------
# Brand palette (extracted from Fab Logo.jpg)
# ---------------------------------------------------------------------------

MAGENTA = (142, 27, 92)    # #8E1B5C — primary brand colour
GOLD = (196, 162, 63)      # #C4A23F — accent
CHARCOAL = (43, 43, 43)    # #2B2B2B — body text
CREAM = (250, 247, 242)    # #FAF7F2 — background base
WHITE = (255, 255, 255)

# ---------------------------------------------------------------------------
# GIF render settings
# ---------------------------------------------------------------------------

W, H = 1080, 1080   # canvas dimensions (px)
FPS = 10            # frames per second — lower FPS = smaller GIF
N_FRAMES = 30       # animation frames (= 3 s of reveal at 10 fps)
# Frames of the fully-revealed design shown BEFORE the reveal animation restarts.
# Critical for WhatsApp: frame 0 of a GIF is the thumbnail. Without this hold,
# the thumbnail is a blank cream square and the GIF looks broken.
# With disposal=1, identical hold frames compress to near-zero extra bytes.
HOLD_FRAMES = 10    # 1.0 s static hold → thumbnail + tap-to-play anchor on iOS
LOGO_W = 380        # logo render width in px — 35% of canvas (premium range: 28–37%)

# ---------------------------------------------------------------------------
# Scenario data
# Each dict drives one GIF.  Edit headline / body / support_line here,
# then re-run the script to regenerate.
# ---------------------------------------------------------------------------

SCENARIOS = [
    {
        "filename": "scenario-01-no-answer.gif",
        # Visual hook shown large on the GIF canvas (not the WhatsApp message body)
        "headline": "We missed your call",
        # Two-line body preview — kept short so it reads at thumbnail size
        "body": "Reply YES and we'll ring back\nat your convenient time.",
        # Per-scenario warm one-liner that fills the lower canvas zone
        "support_line": "We'd love to hear from you.",
    },
    {
        "filename": "scenario-02-disconnected.gif",
        "headline": "Oops, call dropped",
        "body": "Apologies! Reply YES and we'll\npick up right where we left off.",
        "support_line": "Let's continue where we left off.",
    },
    {
        "filename": "scenario-03-call-later.gif",
        "headline": "Time to chat?",
        "body": "You'd asked us to call back.\nReply YES with a convenient time.",
        "support_line": "Your time, your pace.",
    },
    {
        "filename": "scenario-04-didnt-book.gif",
        "headline": "Still thinking it over?",
        "body": "Your consultation is just one\nstep away. Reply YES to begin.",
        "support_line": "No pressure — we're here for you.",
    },
    {
        "filename": "scenario-05-price.gif",
        "headline": "Smart options for you",
        "body": "Easy EMI & seasonal offers available.\nReply YES to know more.",
        "support_line": "Flexible plans this month.",
    },
    {
        "filename": "scenario-06-comparing.gif",
        "headline": "Why patients pick FAB",
        "body": "Certified specialists. Advanced tech.\nEthical care. Reply YES to learn more.",
        "support_line": "Trusted by thousands in your city.",
    },
    {
        "filename": "scenario-07-no-show.gif",
        "headline": "We missed you today",
        "body": "Hope all is well. Reply YES\nto reschedule at your convenience.",
        "support_line": "Your slot is always here.",
    },
    {
        "filename": "scenario-08-dormant.gif",
        "headline": "Have we lost touch?",
        "body": "Whenever you're ready, our team\nis just one message away.",
        "support_line": "No rush. We're here when you are.",
    },
]


# ---------------------------------------------------------------------------
# Asset loaders
# ---------------------------------------------------------------------------

def load_font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    """Load a Poppins TTF by weight name and pixel size."""
    return ImageFont.truetype(str(FONT_DIR / f"Poppins-{weight}.ttf"), size)


def load_logo() -> Image.Image:
    """
    Load the clinic logo, strip the white background, and resize to LOGO_W.

    The logo JPEG has a white background that would look wrong on the cream
    canvas. We make any pixel with R,G,B > 240 fully transparent so the logo
    blends cleanly with the Soft Bloom background underneath.
    """
    im = Image.open(LOGO_PATH).convert("RGBA")
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, _ = px[x, y]
            if r > 240 and g > 240 and b > 240:
                px[x, y] = (r, g, b, 0)  # make near-white pixels transparent
    target_h = int(im.height * LOGO_W / im.width)
    return im.resize((LOGO_W, target_h), Image.LANCZOS)


def make_background() -> Image.Image:
    """
    Render the static Soft Bloom background (pre-computed once, reused per frame).

    Two Gaussian-blurred RGBA ellipses are composited over the cream base:
      • Bloom 1 — rose/blush at bottom-right corner (alpha 55 at peak)
        Gives the design its skincare-brand warmth, echoing Kaya/Oliva aesthetics.
      • Bloom 2 — warm gold/honey at top-left (alpha 38 ≈ 15% opacity)
        Balances the composition so the bottom-heavy bloom doesn't feel lopsided.

    The GaussianBlur radius (180–210 px) ensures the colour is imperceptible as
    a gradient band and reads as a soft ambient glow — critical for GIF palette
    efficiency (only ~20 colours cover the entire background variation).
    """
    base = Image.new("RGBA", (W, H), CREAM + (255,))

    # Rose/blush bloom — large ellipse anchored off-canvas at bottom-right
    bloom1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(bloom1).ellipse(
        [W // 3, H // 3, W + 500, H + 500], fill=(224, 165, 175, 55)
    )
    bloom1 = bloom1.filter(ImageFilter.GaussianBlur(radius=210))
    base.alpha_composite(bloom1)

    # Gold/honey bloom — large ellipse anchored off-canvas at top-left
    bloom2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(bloom2).ellipse(
        [-380, -380, W // 2, H // 2], fill=(220, 195, 148, 38)
    )
    bloom2 = bloom2.filter(ImageFilter.GaussianBlur(radius=180))
    base.alpha_composite(bloom2)

    return base


# ---------------------------------------------------------------------------
# Animation helpers
# ---------------------------------------------------------------------------

def smoothstep(t: float, a: float, b: float) -> float:
    """
    Return a smooth 0→1 ramp between frame indices a and b.

    Uses the cubic smoothstep formula (p² × (3 - 2p)) which produces
    ease-in-out motion — elements accelerate into view and decelerate to rest.
    More natural-feeling than a linear fade for a premium brand aesthetic.
    """
    if t <= a:
        return 0.0
    if t >= b:
        return 1.0
    p = (t - a) / (b - a)
    return p * p * (3 - 2 * p)


def fade(layer: Image.Image, alpha: float) -> Image.Image:
    """
    Scale the alpha channel of an RGBA image by alpha ∈ [0, 1].

    Used to animate each layer's opacity independently without touching the
    underlying pixel colours (avoids hue shifts during fade transitions).
    """
    if alpha >= 1.0:
        return layer
    if alpha <= 0:
        return Image.new("RGBA", layer.size, (0, 0, 0, 0))
    r, g, b, a = layer.split()
    a = a.point(lambda v: int(v * alpha))
    return Image.merge("RGBA", (r, g, b, a))


# ---------------------------------------------------------------------------
# Frame renderer
# ---------------------------------------------------------------------------

def render_frame(
    t: int,
    scenario: dict,
    logo: Image.Image,
    fonts: dict,
    bg: Image.Image,
) -> Image.Image:
    """
    Render a single animation frame at time index t.

    Each visual element lives on its own transparent RGBA overlay layer.
    Layers are composited in order (back-to-front) onto a copy of the
    pre-rendered Soft Bloom background, then flattened to RGB for GIF export.

    Layout positions are computed relative to logo.height so the design
    stays proportional if the logo source file ever changes.

    Args:
        t        : Frame index (0 to N_FRAMES-1)
        scenario : Dict with 'headline', 'body', 'support_line' keys
        logo     : Pre-loaded, white-stripped, resized logo image
        fonts    : Dict of loaded Poppins ImageFont objects
        bg       : Pre-rendered Soft Bloom background (RGBA)

    Returns:
        RGB Image ready to be quantized and saved into the GIF.
    """
    # Start from a copy of the static background — never mutate the original
    base = bg.copy()
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # ── Layout positions ──────────────────────────────────────────────────
    # All y-values derived from logo position so the composition scales if
    # the logo source dimensions change.
    logo_x = (W - logo.width) // 2   # logo is centered horizontally
    logo_y = 130                      # top margin
    sep_y = logo_y + logo.height + 36        # separator dots vertical centre
    headline_y = sep_y + 54                  # headline top edge
    body_y1 = headline_y + 142              # body line 1 (86pt ≈ 115 px + 27 px gap)
    body_y2 = body_y1 + 64                  # body line 2
    support_y = body_y2 + 72                # support line top edge

    # ── 1. Logo (fade-in frames 0–6) ─────────────────────────────────────
    alpha_logo = smoothstep(t, 0, 6)
    if alpha_logo > 0:
        overlay.alpha_composite(fade(logo, alpha_logo), (logo_x, logo_y))

    # ── 2. Separator: 3 gold dots, left-aligned (fade-in frames 3–9) ─────
    # Three dots survive GIF quantization at WhatsApp thumbnail size (~260 px);
    # a 2 px hairline would alias to invisible below that threshold.
    alpha_line = smoothstep(t, 3, 9)
    if alpha_line > 0:
        sep_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sep_layer)
        dot_r = 8
        dot_spacing = dot_r * 2 + 12   # centre-to-centre = diameter + gap
        dot_fill = GOLD + (int(255 * alpha_line),)
        for i in range(3):
            cx = 80 + dot_r + i * dot_spacing   # left-align with headline x=80
            sd.ellipse(
                [cx - dot_r, sep_y - dot_r, cx + dot_r, sep_y + dot_r],
                fill=dot_fill,
            )
        overlay.alpha_composite(sep_layer)

    # ── 3. Headline (fade-in frames 7–15, 12 px upward slide) ────────────
    # Left-aligned at x=80 intentionally breaks the centered-everything pattern
    # that reads as auto-generated. The slide-up reinforces the reveal direction.
    alpha_h = smoothstep(t, 7, 15)
    if alpha_h > 0:
        slide = int(12 * (1 - alpha_h))   # 12 px at start → 0 px at end
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(layer).text(
            (80, headline_y + slide),
            scenario["headline"],
            font=fonts["headline"],
            fill=MAGENTA + (int(255 * alpha_h),),
        )
        overlay.alpha_composite(layer)

    # ── 4. Body text (fade-in frames 12–20) ──────────────────────────────
    alpha_b = smoothstep(t, 12, 20)
    if alpha_b > 0:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        for y_pos, line in zip([body_y1, body_y2], scenario["body"].split("\n")):
            d.text(
                (80, y_pos),
                line,
                font=fonts["body"],
                fill=CHARCOAL + (int(255 * alpha_b),),
            )
        overlay.alpha_composite(layer)

    # ── 5. Support line (fade-in frames 17–24) ───────────────────────────
    # Scenario-specific warm 1-liner that anchors the lower canvas zone.
    # 70% opacity (alpha 178) keeps it subordinate to the body text hierarchy.
    alpha_s = smoothstep(t, 17, 24)
    if alpha_s > 0:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(layer).text(
            (80, support_y),
            scenario["support_line"],
            font=fonts["support"],
            fill=CHARCOAL + (int(178 * alpha_s),),
        )
        overlay.alpha_composite(layer)

    # Flatten to RGB — GIF format does not support full RGBA
    return Image.alpha_composite(base, overlay).convert("RGB")


# ---------------------------------------------------------------------------
# GIF encoder
# ---------------------------------------------------------------------------

def render_gif(
    scenario: dict,
    logo: Image.Image,
    fonts: dict,
    out_path: Path,
    bg: Image.Image,
) -> int:
    """
    Render all frames for one scenario and save as an optimised GIF.

    Palette strategy:
      A shared 128-colour palette is derived from the fully-revealed final
      frame (frame 29), which contains every colour present in the animation.
      All frames are then quantised against this shared palette using
      Floyd-Steinberg dithering for smooth gradient reproduction.

    GIF compression strategy:
      disposal=1 (leave-in-place) means the GIF decoder accumulates frame
      deltas on a single buffer. Because the Soft Bloom background is static,
      only the animated overlay pixels change between frames — dramatically
      reducing the per-frame delta and enabling efficient LZW compression.

    Args:
        scenario : Scenario dict (from SCENARIOS list)
        logo     : Pre-loaded logo image
        fonts    : Dict of loaded font objects
        out_path : Output .gif file path
        bg       : Pre-rendered background (shared across all scenarios)

    Returns:
        File size in bytes.
    """
    frames = [render_frame(t, scenario, logo, fonts, bg) for t in range(N_FRAMES)]

    # Prepend static hold frames showing the fully-revealed design.
    # The first frame of a GIF is WhatsApp's thumbnail AND the starting display
    # state. Without this, frame 0 is a blank cream square (all elements are at
    # opacity 0 at t=0), making the creative appear broken before it animates.
    # Identical frames compress to near-zero bytes with disposal=1 delta encoding.
    frames = [frames[-1]] * HOLD_FRAMES + frames

    # Build palette from the hold frame — it contains every colour in the animation
    palette_src = frames[0].quantize(
        colors=128, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG
    )
    quantized = [
        f.quantize(palette=palette_src, dither=Image.FLOYDSTEINBERG) for f in frames
    ]

    quantized[0].save(
        out_path,
        save_all=True,
        append_images=quantized[1:],
        duration=int(1000 / FPS),   # milliseconds per frame
        loop=1,                      # 1 = play once then hold on last frame
        optimize=True,
        disposal=1,                  # leave-in-place for delta compression
    )
    return out_path.stat().st_size


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load shared assets once — reused across all 8 renders
    logo = load_logo()
    bg = make_background()
    fonts = {
        "headline": load_font("Bold", 86),
        "body":     load_font("Regular", 40),
        "support":  load_font("Regular", 34),
    }

    print(f"Rendering {len(SCENARIOS)} GIFs to {OUT_DIR}  (v0.2)")
    total = 0
    for s in SCENARIOS:
        out_path = OUT_DIR / s["filename"]
        size = render_gif(s, logo, fonts, out_path, bg)
        kb = size / 1024
        total += size
        flag = "OK " if size < 2 * 1024 * 1024 else "BIG"
        print(f"  [{flag}] {s['filename']:<36} {kb:8.1f} KB")

    print(f"\nTotal: {total / 1024:.1f} KB across {len(SCENARIOS)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
