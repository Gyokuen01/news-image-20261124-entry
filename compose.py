#!/usr/bin/env python3
"""Compose the 24 November 2026 newspaper front page (1024x1024).

Fresh build for news-image-20261124. Reads the 8 generated photos in
photos/ and lays out a classic front page: masthead, lead story, two
photo rows, and a dense round-up of the day's other headlines.
Output: entry.png (PNG, <= 1 MiB).
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(HERE, "photos")
W, H = 1024, 1024

PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (90, 86, 76)
RULE = (60, 58, 50)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def photo_cover(path, tw, th):
    im = Image.open(path).convert("RGB")
    iw, ih = im.size
    scale = max(tw / iw, th / ih)
    im = im.resize((round(iw * scale), round(ih * scale)), Image.LANCZOS)
    left = (im.width - tw) // 2
    top = (im.height - th) // 2
    return im.crop((left, top, left + tw, top + th))


def caption_block(draw, x, y, w, kicker, headline, summary,
                  head_size, sum_size):
    f_kick = font(SANS_B, 12)
    f_head = font(SERIF_B, head_size)
    f_sum = font(SANS, sum_size)
    draw.text((x, y), kicker, font=f_kick, fill=RED)
    y += 16
    y = draw_lines(draw, wrap(draw, headline, f_head, w), x, y,
                   f_head, INK, head_size + 3)
    y = draw_lines(draw, wrap(draw, summary, f_sum, w), x, y + 2,
                   f_sum, (40, 40, 38), sum_size + 4)
    return y


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---- Masthead: 0-150 ----
    d.text((W // 2, 4), "THE WORLD TODAY", font=font(SERIF_B, 72),
           fill=INK, anchor="ma")
    d.line([(16, 88), (W - 16, 88)], fill=RULE, width=3)
    d.text((W // 2, 94), "TUESDAY 24 NOVEMBER 2026",
           font=font(SANS_B, 25), fill=RED, anchor="ma")
    d.text((W // 2, 124),
           "One day in world news  •  Markets  •  War  •  Climate  •  Justice  •  Sport",
           font=font(SANS, 14), fill=GREY, anchor="ma")
    d.line([(16, 146), (W - 16, 146)], fill=RULE, width=2)

    # ---- Lead story: Nvidia, y 154-394 ----
    lead_y = 154
    page.paste(photo_cover(os.path.join(PHOTOS, "nvidia.jpg"), 600, 240),
               (16, lead_y))
    d.rectangle([16, lead_y, 616, lead_y + 240], outline=RULE, width=2)
    lx = 632
    d.text((lx, lead_y + 2), "MARKETS  •  LEAD STORY",
           font=font(SANS_B, 14), fill=RED)
    f_lead_h = font(SERIF_B, 40)
    y = draw_lines(d, ["HUANG IS BACK"], lx, lead_y + 24, f_lead_h, INK, 44)
    f_lead_s = font(SANS, 18)
    y = draw_lines(
        d,
        wrap(d, "Nvidia reinstates Jensen Huang as chief executive, 11 days "
                "after his resignation — shares soar 31%, gaining $952 billion "
                "in a day, their best since 2003.", f_lead_s, 376),
        lx, y + 4, f_lead_s, (40, 40, 38), 23)
    f_lead_b = font(SANS_B, 16)
    draw_lines(
        d,
        wrap(d, "Nasdaq jumps 6.5% and the S&P 500 4.7% in the best day "
                "since April 2025.", f_lead_b, 376),
        lx, y + 6, f_lead_b, INK, 20)

    # ---- Row 2: three photos, y 402-542, captions 546-642 ----
    row2_y = 402
    row2 = [
        ("libya.jpg", "WAR  •  UKRAINE", "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
         "Kyiv says its strike destroyed the corvette Merkury in Benghazi port."),
        ("cop31.jpg", "CLIMATE  •  COP31", "COP31 ENDS WITH NO DEAL",
         "The climate summit closes without a final deal; talks may resume next year."),
        ("indonesia.jpg", "ASIA  •  INDONESIA", "FACTORY FIRE KILLS 24 IN INDONESIA",
         "A blaze at a candy factory leaves 24 dead and 34 missing."),
    ]
    for (img, kick, head, summ), x in zip(row2, [16, 352, 688]):
        page.paste(photo_cover(os.path.join(PHOTOS, img), 320, 140), (x, row2_y))
        d.rectangle([x, row2_y, x + 320, row2_y + 140], outline=RULE, width=2)
        caption_block(d, x, row2_y + 144, 320, kick, head, summ, 18, 13)

    # ---- Row 3: four photos, y 650-750, captions 754-834 ----
    row3_y = 650
    row3 = [
        ("icj.jpg", "JUSTICE", "MYANMAR GUILTY OF GENOCIDE, COURT RULES",
         "The UN court finds Myanmar guilty of genocide against the Rohingya."),
        ("alcaraz.jpg", "TENNIS", "ALCARAZ WINS FIRST ATP FINALS TITLE",
         "The Spaniard beats Zverev in Turin to lift the season-ending crown."),
        ("chess.jpg", "CHESS", "CHESS CROWN DEFENCE BEGINS IN GENEVA",
         "Champion D Gukesh opens his title defence against Javokhir Sindarov."),
        ("wwc.jpg", "FOOTBALL", "UK TO HOST 2035 WOMEN'S WORLD CUP",
         "FIFA confirms Britain as host of the 2035 tournament."),
    ]
    for (img, kick, head, summ), x in zip(row3, [16, 268, 520, 772]):
        page.paste(photo_cover(os.path.join(PHOTOS, img), 236, 100), (x, row3_y))
        d.rectangle([x, row3_y, x + 236, row3_y + 100], outline=RULE, width=2)
        caption_block(d, x, row3_y + 104, 236, kick, head, summ, 15, 12)

    # ---- Round-up: heading y 842, items from y 864 ----
    ru_y = 842
    d.line([(16, ru_y), (W - 16, ru_y)], fill=RULE, width=2)
    d.text((16, ru_y + 6), "MORE FROM AROUND THE WORLD",
           font=font(SANS_B, 15), fill=RED)
    d.text((W - 16, ru_y + 6), "TUESDAY 24 NOVEMBER 2026",
           font=font(SANS_B, 12), fill=GREY, anchor="ra")

    more = [
        "CrowdStrike to buy Zscaler, $43.9bn.",
        "Trump may erase hush-money verdict.",
        "Democrats win House: 258 seats.",
        "Waymo pulls robotaxis off freeways.",
        "Gaza soil, water poisoned for decades.",
        "Taliban erases women's names in Balkh.",
        "Denmark backs hardline 'ghetto law'.",
        "Arson hits five West Bank villages.",
        "Supermoon meets the Pleiades tonight.",
        "Manchester concert evacuated.",
        "Fiona the hippo dies at US zoo.",
        "Migrant boat sinks off Senegal.",
        "India, Nepal sign eight deals.",
        "Modi opens AI centre at IIT Patna.",
        "India, China hold border talks.",
        "India v NZ Test ends in a draw.",
        "NATO vows space defence.",
        "Trump halts Army azide detonation.",
        "Kim ignores Trump's outreach: WSJ.",
        "Iran vows to counter Hormuz blockade.",
        "Netanyahu: no pause on Iran attacks.",
        "490,000+ Russian troops killed.",
        "Russian strikes kill 14 near Kyiv.",
        "Anthropic slips 1.4% in rally.",
    ]
    f_item = font(SANS, 12)
    col_xs = [16, 268, 520, 772]
    per_col = 6
    for ci in range(4):
        x = col_xs[ci]
        y = ru_y + 28
        for item in more[ci * per_col:(ci + 1) * per_col]:
            lines = wrap(d, "•  " + item, f_item, 236)
            y = draw_lines(d, lines, x, y, f_item, (40, 40, 38), 15)

    # ---- Footer ----
    d.line([(16, H - 18), (W - 16, H - 18)], fill=RULE, width=1)
    d.text((W // 2, H - 14),
           "Stories first reported Tuesday 24 November 2026  •  Sources: Reuters, BBC, CNN, WSJ, AP",
           font=font(SANS, 11), fill=GREY, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    page.save(out, format="PNG", optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out} {page.size} {size} bytes")
    if size > 1048576:
        page.save(out, format="JPEG", quality=88, optimize=True)
        print(f"PNG too big; rewrote as JPEG {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
