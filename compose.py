#!/usr/bin/env python3
"""Build the front page for 24 November 2026.

Takes the generated hero illustration (assets/hero.webp), crops it into a
banner, and lays out a one-page newspaper front over it with PIL: masthead,
date, and five short news items researched from the day's reporting.
Writes assets/entry.png, the image main.py later copies to the grader.
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

REPO = "/home/hatch/workspace/news-image-20261124-repo"
HERO = REPO + "/assets/media-generation-hero-0-366c5f44-fe19-450c-a198-9f851444f60d.webp"
OUT = REPO + "/assets/entry.png"

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (18, 18, 18)
RULE = (18, 18, 18)
ACCENT = (176, 32, 24)
MUTED = (90, 84, 74)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrapped(draw, text, fnt, width):
    """Greedy word wrap returning lines that fit inside width pixels."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        line = ""
        for word in words:
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def main():
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)

    # --- Masthead ---
    y = 28
    draw.text((W // 2, y), "THE WORLD IN ONE DAY",
              font=font(BOLD, 26), fill=ACCENT, anchor="ma")
    y += 44
    draw.text((W // 2, y), "TUESDAY 24 NOVEMBER 2026",
              font=font(BOLD, 58), fill=INK, anchor="ma")
    y += 78
    draw.line([(36, y), (W - 36, y)], fill=RULE, width=4)
    y += 12
    draw.text((W // 2, y), "FIVE STORIES THAT DEFINED THE DAY  •  FROM KYIV TO SILICON VALLEY",
              font=font(BOLD, 20), fill=MUTED, anchor="ma")
    y += 36

    # --- Hero banner ---
    hero = Image.open(HERO).convert("RGB")
    banner_h = 400
    scale = max(W / hero.width, banner_h / hero.height)
    hero = hero.resize((int(hero.width * scale) + 1,
                        int(hero.height * scale) + 1), Image.LANCZOS)
    left = (hero.width - W) // 2
    top = (hero.height - banner_h) // 2
    page.paste(hero.crop((left, top, left + W, top + banner_h)), (0, y))
    draw.line([(0, y), (W, y)], fill=RULE, width=3)
    y += banner_h
    draw.line([(0, y), (W, y)], fill=RULE, width=3)
    y += 14

    # --- News items ---
    items = [
        ("TECH", "Huang returns as Nvidia chief",
         "Board reinstates Jensen Huang after a Trump push; shares jump about a third in a day."),
        ("UKRAINE", "Russian war dead near 500,000",
         "Newly hacked data puts Moscow's toll in Ukraine close to half a million."),
        ("LIBYA", "Ukraine strike sinks Russian warship",
         "A corvette is reported destroyed by explosion and fire at Benghazi port."),
        ("SPACE", "NATO warns of Russian space weapon",
         "Allies say Moscow may launch a nuclear-armed satellite killer as soon as next month."),
    ]
    x = 44
    col_w = W - 2 * x
    for kicker, headline, summary in items:
        draw.text((x, y), kicker, font=font(BOLD, 20), fill=ACCENT)
        draw.text((x + 130, y), headline, font=font(BOLD, 27), fill=INK)
        y += 38
        for line in wrapped(draw, summary, font(PLAIN, 21), col_w - 20):
            draw.text((x + 20, y), line, font=font(PLAIN, 21), fill=(52, 48, 44))
            y += 28
        y += 10
        draw.line([(x, y), (W - x, y)], fill=(200, 192, 178), width=1)
        y += 12

    # --- Footer strip (shrink until it fits the page width) ---
    footer = "ALSO: States sue Musk firms over Grok images  •  Storms threaten Thanksgiving travel"
    size = 19
    while size > 12 and draw.textlength(footer, font=font(BOLD, size)) > W - 72:
        size -= 1
    draw.text((W // 2, y), footer, font=font(BOLD, size), fill=MUTED, anchor="ma")

    page.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} ({W}x{H})")


if __name__ == "__main__":
    main()
