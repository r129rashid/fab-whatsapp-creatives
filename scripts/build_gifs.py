"""
build_gifs.py — FAB Skin Hair & Laser Clinic WhatsApp GIF + MP4 Generator
==========================================================================
Renders 8 animated creatives (1080×1080 px) for WhatsApp tele-caller
follow-up campaigns, each covering one lead re-engagement scenario.

Outputs TWO formats per scenario:
  • creatives/*.gif  — for preview, web, and email use
  • creatives/*.mp4  — for WhatsApp delivery (requires ffmpeg)

WHY MP4 FOR WHATSAPP:
  WhatsApp does NOT animate GIF files sent as image attachments from the
  gallery or via the Business API image message type. Animated content must
  be sent as MP4 video (message type: video / document). The MP4 plays
  inline, autoplays once, and holds on the last frame — exactly the
  behaviour we want for a tele-caller follow-up creative.

Design spec (v0.3 — center-aligned):
  Canvas      : 1080×1080 px, 1:1 square (WhatsApp-safe)
  Duration    : 4 s total (1 s static hold + 3 s reveal), plays once
  Background  : Soft Bloom — cream base with rose glow (bottom-right) and
                gold glow (top-left), Gaussian-blurred for smoothness
  Logo        : Centered, 380 px wide (35% of canvas)
  Separator   : Three 8 px gold dots, centered
  Headline    : Poppins Bold 86pt, centered, magenta
  Body text   : Poppins Regular 40pt, centered, charcoal
  Support line: Poppins Regular 34pt, centered, charcoal 70% opacity
  CTA         : NOT in the creative — "Reply YES" is a WhatsApp Quick
                Reply button configured in TeleCRM

Animation sequence (frame index at 10 fps, after HOLD_FRAMES):
  Frame 0–6   : Logo fades in
  Frame 3–9   : Gold separator dots fade in
  Frame 7–15  : Headline fades in + slides up 12 px
  Frame 12–20 : Body text fades in
  Frame 17–24 : Support line fades in
  Frame 24–29 : All elements fully visible (hold / last-frame anchor)

Changes from v0.2:
  - All text elements center-aligned (headline, body, support, separator)
  - Richer body copy: warmer, more descriptive 2-liners per scenario
  - MP4 export via ffmpeg for WhatsApp animated delivery
  - HOLD_FRAMES=10 prepended so frame 0 = complete design (WA thumbnail fix)

Usage:
  python3 scripts/build_gifs.py

Requirements:
  pip install Pillow
  ffmpeg (brew install ffmpeg) — for MP4 export
  assets/fonts/Poppins-{Bold,Regular}.ttf must exist
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

BASE = Path(__file__).resolve().parent.parent
LOGO_PATH = BASE / "Fab Logo.jpg"
FONT_DIR = BASE / "assets" / "fonts"
OUT_DIR = BASE / "creatives"

# ---------------------------------------------------------------------------
# Brand palette
# ---------------------------------------------------------------------------

MAGENTA  = (142,  27,  92)   # #8E1B5C — primary brand colour
GOLD     = (196, 162,  63)   # #C4A23F — accent
CHARCOAL = ( 43,  43,  43)   # #2B2B2B — body text
CREAM    = (250, 247, 242)   # #FAF7F2 — background base

# ---------------------------------------------------------------------------
# Render settings
# ---------------------------------------------------------------------------

W, H       = 1080, 1080
FPS        = 10
N_FRAMES   = 30       # animation frames = 3 s at 10 fps
LOGO_W     = 380      # 35% of canvas width

# Frames of the fully-revealed design prepended before the reveal animation.
# Fixes WhatsApp thumbnail: frame 0 of a GIF/video must show the complete
# creative, not the blank starting state of the fade-in animation.
# With disposal=1 delta encoding, identical hold frames add ~0 bytes to GIF size.
HOLD_FRAMES = 10      # 1.0 s static hold before each reveal cycle

# ---------------------------------------------------------------------------
# Scenario data — edit here, then re-run to regenerate
# ---------------------------------------------------------------------------

SCENARIOS = [
    {
        "filename": "scenario-01-no-answer",
        "headline": "We missed your call",
        "body": "We tried reaching you but missed you today.\nReply YES — we'll call you right back.",
        "support_line": "We'd love to hear from you.",
    },
    {
        "filename": "scenario-02-disconnected",
        "headline": "Oops, call dropped",
        "body": "Our call got disconnected midway — sorry!\nReply YES to continue from where we stopped.",
        "support_line": "Let's continue where we left off.",
    },
    {
        "filename": "scenario-03-call-later",
        "headline": "Time to chat?",
        "body": "You'd asked us to reach back out — we're here!\nReply YES to confirm a convenient time.",
        "support_line": "Your time, your pace.",
    },
    {
        "filename": "scenario-04-didnt-book",
        "headline": "Still thinking it over?",
        "body": "Your consultation is just one step away.\nReply YES and we'll guide you through it.",
        "support_line": "No pressure — we're here for you.",
    },
    {
        "filename": "scenario-05-price",
        "headline": "Smart options for you",
        "body": "We have flexible EMI plans and special offers.\nReply YES to find the best plan for you.",
        "support_line": "Flexible plans this month.",
    },
    {
        "filename": "scenario-06-comparing",
        "headline": "Why patients pick FAB",
        "body": "Thousands trust FAB for certified, ethical care.\nReply YES for a transparent, no-pressure chat.",
        "support_line": "Trusted by thousands in your city.",
    },
    {
        "filename": "scenario-07-no-show",
        "headline": "We missed you today",
        "body": "We held your slot open — hope you're doing well.\nReply YES to reschedule at your convenience.",
        "support_line": "Your slot is always here.",
    },
    {
        "filename": "scenario-08-dormant",
        "headline": "Have we lost touch?",
        "body": "It's been a while — we've been thinking of you.\nReply YES whenever you're ready to reconnect.",
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
    Load the clinic logo, strip its white background, and resize to LOGO_W.

    The logo JPEG has a solid white background. We make any pixel with all
    RGB channels > 240 transparent so the logo blends cleanly with the Soft
    Bloom background underneath.
    """
    im = Image.open(LOGO_PATH).convert("RGBA")
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, _ = px[x, y]
            if r > 240 and g > 240 and b > 240:
                px[x, y] = (r, g, b, 0)
    target_h = int(im.height * LOGO_W / im.width)
    return im.resize((LOGO_W, target_h), Image.LANCZOS)


def make_background() -> Image.Image:
    """
    Render the static Soft Bloom background (pre-computed once, reused per frame).

    Two Gaussian-blurred RGBA ellipses are composited over the cream base:
      • Bloom 1 — rose/blush at bottom-right (alpha 55 peak): gives the
        design its skincare-brand warmth, echoing Kaya / Oliva aesthetics.
      • Bloom 2 — warm gold/honey at top-left (alpha 38 ≈ 15%): balances
        the composition so the bottom-right bloom doesn't feel lopsided.

    The large blur radius (180–210 px) ensures colours read as ambient glow
    rather than visible gradient bands — important for GIF palette efficiency.
    """
    base = Image.new("RGBA", (W, H), CREAM + (255,))

    bloom1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(bloom1).ellipse(
        [W // 3, H // 3, W + 500, H + 500], fill=(224, 165, 175, 55)
    )
    bloom1 = bloom1.filter(ImageFilter.GaussianBlur(radius=210))
    base.alpha_composite(bloom1)

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
    Smooth 0→1 ramp between frame indices a and b.

    Uses the cubic formula p²(3−2p) for ease-in-out motion — elements
    accelerate into view and decelerate to rest. More natural than a linear
    fade for a premium brand aesthetic.
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

    Animates opacity without touching pixel hue (avoids colour shifts).
    """
    if alpha >= 1.0:
        return layer
    if alpha <= 0:
        return Image.new("RGBA", layer.size, (0, 0, 0, 0))
    r, g, b, a = layer.split()
    a = a.point(lambda v: int(v * alpha))
    return Image.merge("RGBA", (r, g, b, a))


def draw_text_centered(
    draw: ImageDraw.ImageDraw,
    text: str,
    y: int,
    font: ImageFont.FreeTypeFont,
    fill: tuple,
) -> None:
    """Draw text horizontally centered on the canvas at vertical position y."""
    bbox = draw.textbbox((0, 0), text, font=font)
    x = (W - (bbox[2] - bbox[0])) // 2 - bbox[0]
    draw.text((x, y), text, font=font, fill=fill)

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

    Each element lives on its own transparent RGBA overlay layer, composited
    in back-to-front order onto a copy of the pre-rendered Soft Bloom
    background, then flattened to RGB for GIF/MP4 export.

    All text and separator elements are center-aligned on the canvas.
    Layout y-positions are derived from logo.height so the design stays
    proportional if the logo source file ever changes.

    Args:
        t        : Frame index (0 to N_FRAMES-1)
        scenario : Dict with 'headline', 'body', 'support_line' keys
        logo     : Pre-loaded, white-stripped, resized logo image
        fonts    : Dict of loaded Poppins ImageFont objects
        bg       : Pre-rendered Soft Bloom background (RGBA)

    Returns:
        RGB Image ready to be quantized and written into the GIF/MP4.
    """
    base = bg.copy()
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # ── Layout y-positions (all derived from logo size) ───────────────────
    logo_x    = (W - logo.width) // 2
    logo_y    = 130
    sep_y     = logo_y + logo.height + 36    # separator dots vertical centre
    headline_y = sep_y + 54                  # headline top edge
    body_y1   = headline_y + 142             # body line 1 (86pt ≈ 115 px + 27 px gap)
    body_y2   = body_y1 + 64                 # body line 2
    support_y = body_y2 + 72                 # support line top edge

    # ── 1. Logo (fade-in frames 0–6) ─────────────────────────────────────
    alpha_logo = smoothstep(t, 0, 6)
    if alpha_logo > 0:
        overlay.alpha_composite(fade(logo, alpha_logo), (logo_x, logo_y))

    # ── 2. Separator: 3 gold dots, centered (fade-in frames 3–9) ─────────
    # Three solid dots survive GIF quantization at WhatsApp thumbnail size
    # (~260 px); a 2 px hairline aliases to invisible below that threshold.
    alpha_line = smoothstep(t, 3, 9)
    if alpha_line > 0:
        sep_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sep_layer)
        dot_r  = 8
        dot_gap = 12                          # gap between dot edges
        spacing = dot_r * 2 + dot_gap         # centre-to-centre distance
        total_w = 3 * (dot_r * 2) + 2 * dot_gap   # total group width
        first_cx = (W - total_w) // 2 + dot_r     # centre of leftmost dot
        dot_fill = GOLD + (int(255 * alpha_line),)
        for i in range(3):
            cx = first_cx + i * spacing
            sd.ellipse(
                [cx - dot_r, sep_y - dot_r, cx + dot_r, sep_y + dot_r],
                fill=dot_fill,
            )
        overlay.alpha_composite(sep_layer)

    # ── 3. Headline (fade-in frames 7–15, 12 px upward slide), centered ──
    alpha_h = smoothstep(t, 7, 15)
    if alpha_h > 0:
        slide = int(12 * (1 - alpha_h))   # 12 px at start of fade → 0 px at end
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw_text_centered(
            ImageDraw.Draw(layer),
            scenario["headline"],
            headline_y + slide,
            fonts["headline"],
            MAGENTA + (int(255 * alpha_h),),
        )
        overlay.alpha_composite(layer)

    # ── 4. Body lines (fade-in frames 12–20), centered ───────────────────
    alpha_b = smoothstep(t, 12, 20)
    if alpha_b > 0:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        for y_pos, line in zip([body_y1, body_y2], scenario["body"].split("\n")):
            draw_text_centered(
                d, line, y_pos, fonts["body"],
                CHARCOAL + (int(255 * alpha_b),),
            )
        overlay.alpha_composite(layer)

    # ── 5. Support line (fade-in frames 17–24), centered ─────────────────
    # Scenario-specific warm 1-liner that anchors the lower canvas zone.
    # 70% opacity (alpha 178) keeps it subordinate to the body text hierarchy.
    alpha_s = smoothstep(t, 17, 24)
    if alpha_s > 0:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw_text_centered(
            ImageDraw.Draw(layer),
            scenario["support_line"],
            support_y,
            fonts["support"],
            CHARCOAL + (int(178 * alpha_s),),
        )
        overlay.alpha_composite(layer)

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
    Render all frames and save as an optimised, play-once GIF.

    Frame layout:
      [HOLD_FRAMES × fully-revealed frame] + [N_FRAMES × reveal animation]
    The hold at the start puts the complete design at frame 0, which is what
    WhatsApp displays as the thumbnail and starting state.

    Palette: built from the hold frame (= fully-revealed), which contains
    every colour present in the animation. All frames quantised against this
    shared 128-colour palette using Floyd-Steinberg dithering.

    Compression: disposal=1 (leave-in-place) means the decoder accumulates
    frame deltas. Identical hold frames encode as near-zero-byte deltas.
    The transition from last hold frame to animation frame 0 is the only
    expensive delta (all content pixels change to background), but it only
    occurs once per loop cycle.
    """
    frames = [render_frame(t, scenario, logo, fonts, bg) for t in range(N_FRAMES)]

    # Prepend static hold frames — the complete design must be visible at
    # frame 0 so WhatsApp shows the full creative as the thumbnail, not a
    # blank cream square (which was the v0.1 / v0.2 issue).
    frames = [frames[-1]] * HOLD_FRAMES + frames

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
        duration=int(1000 / FPS),
        loop=1,         # play once then hold on last frame
        optimize=True,
        disposal=1,     # leave-in-place for delta compression
    )
    return out_path.stat().st_size

# ---------------------------------------------------------------------------
# MP4 exporter (requires ffmpeg)
# ---------------------------------------------------------------------------

def gif_to_mp4(gif_path: Path) -> Path | None:
    """
    Convert a GIF to MP4 using ffmpeg for WhatsApp animated delivery.

    WHY THIS IS NECESSARY:
      WhatsApp does not animate .gif files sent as image attachments via the
      gallery or the Business API 'image' message type. For animated content
      in TeleCRM / WhatsApp Business API, send as 'video' (MP4). The video
      autoplays inline in the chat, plays once, and holds on the last frame.

    MP4 output spec:
      - Codec  : H.264 (libx264), compatible with all WhatsApp versions
      - Pixel  : yuv420p — required for broad device compatibility
      - Audio  : none (-an)
      - Size   : dimensions forced to even numbers (WhatsApp requirement)
      - Start  : faststart flag for instant playback before full download

    Args:
        gif_path : Path to the source .gif file (already rendered)

    Returns:
        Path to the .mp4 file on success, or None if ffmpeg is unavailable.

    Install ffmpeg:
        macOS : brew install ffmpeg
        Ubuntu: sudo apt install ffmpeg
    """
    mp4_path = gif_path.with_suffix(".mp4")
    try:
        subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", str(gif_path),
                "-movflags", "faststart",
                "-pix_fmt", "yuv420p",
                "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                "-an",
                str(mp4_path),
            ],
            check=True,
            capture_output=True,
        )
        return mp4_path
    except FileNotFoundError:
        return None   # ffmpeg not installed
    except subprocess.CalledProcessError:
        return None   # conversion failed

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    logo = load_logo()
    bg   = make_background()
    fonts = {
        "headline": load_font("Bold",    86),
        "body":     load_font("Regular", 40),
        "support":  load_font("Regular", 34),
    }

    total_frames = HOLD_FRAMES + N_FRAMES
    total_secs   = total_frames / FPS
    print(
        f"Rendering {len(SCENARIOS)} creatives  "
        f"({total_frames} frames × {1000//FPS} ms = {total_secs:.1f} s, play-once)  v0.3"
    )

    mp4_available = None   # lazily detected on first GIF render

    for s in SCENARIOS:
        gif_path = OUT_DIR / f"{s['filename']}.gif"
        gif_size = render_gif(s, logo, fonts, gif_path, bg)
        gif_kb   = gif_size / 1024
        gif_flag = "OK " if gif_size < 2 * 1024 * 1024 else "BIG"
        print(f"  [{gif_flag}] {gif_path.name:<42}  {gif_kb:7.1f} KB  (GIF)")

        mp4_path = gif_to_mp4(gif_path)
        if mp4_path is not None:
            mp4_kb = mp4_path.stat().st_size / 1024
            print(f"        {mp4_path.name:<42}  {mp4_kb:7.1f} KB  (MP4 ← use this for WhatsApp)")
            mp4_available = True
        elif mp4_available is None:
            print("        [MP4 skipped — install ffmpeg: brew install ffmpeg]")
            mp4_available = False

    if mp4_available:
        print("\n  WhatsApp delivery: upload the .mp4 files to TeleCRM as 'video' attachments.")
    else:
        print("\n  Install ffmpeg to also generate .mp4 files for WhatsApp animation.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
