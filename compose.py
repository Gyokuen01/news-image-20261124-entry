#!/usr/bin/env python3
"""Lay out the 24 November 2026 front page (1024x1024) for v2.

Fresh build for news-image-20261124 v2: 70 verified stories (8 with
photos + 62 one-line round-up items across 9 regions) on one page.
Reads the 8 generated photos from photos/ and writes entry.png
(PNG, target <= 1 MiB; JPEG fallback if the PNG runs too big).
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
BODY = (40, 40, 38)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def put_lines(draw, lines, x, y, fnt, fill, step):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += step
    return y


def cover(path, tw, th):
    """Centre-crop the photo to exactly tw x th (cover fit)."""
    im = Image.open(path).convert("RGB")
    iw, ih = im.size
    scale = max(tw / iw, th / ih)
    im = im.resize((round(iw * scale), round(ih * scale)), Image.LANCZOS)
    left = (im.width - tw) // 2
    top = (im.height - th) // 2
    return im.crop((left, top, left + tw, top + th))


def captioned_photo(page, draw, path, x, y, tw, th,
                    kicker, head, summ, head_size, sum_size):
    """Photo with a kicker + headline + summary block beneath it."""
    page.paste(cover(path, tw, th), (x, y))
    draw.rectangle([x, y, x + tw, y + th], outline=RULE, width=2)
    cy = y + th + 5
    draw.text((x, cy), kicker, font=load(SANS_B, 11), fill=RED)
    cy += 15
    f_head = load(SERIF_B, head_size)
    cy = put_lines(draw, wrap_text(draw, head, f_head, tw), x, cy,
                   f_head, INK, head_size + 3)
    f_sum = load(SANS, sum_size)
    cy = put_lines(draw, wrap_text(draw, summ, f_sum, tw), x, cy + 2,
                   f_sum, BODY, sum_size + 4)
    return cy


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---- Masthead: 0-128 ----
    d.text((W // 2, 0), "THE WORLD TODAY", font=load(SERIF_B, 58),
           fill=INK, anchor="ma")
    d.line([(14, 74), (W - 14, 74)], fill=RULE, width=3)
    d.text((W // 2, 80), "TUESDAY 24 NOVEMBER 2026",
           font=load(SANS_B, 21), fill=RED, anchor="ma")
    d.text((W // 2, 106),
           "One day in world news  •  Markets  •  War  •  Climate  •  Energy  •  Sport",
           font=load(SANS, 13), fill=GREY, anchor="ma")
    d.line([(14, 128), (W - 14, 128)], fill=RULE, width=2)

    # ---- Lead story: Nvidia, photo 560x196 at y 136 ----
    lead_y = 136
    page.paste(cover(os.path.join(PHOTOS, "nvidia.jpg"), 560, 196),
               (14, lead_y))
    d.rectangle([14, lead_y, 574, lead_y + 196], outline=RULE, width=2)
    lx = 590
    d.text((lx, lead_y + 2), "MARKETS  •  LEAD STORY",
           font=load(SANS_B, 13), fill=RED)
    y = put_lines(d, ["HUANG IS BACK"], lx, lead_y + 22,
                  load(SERIF_B, 34), INK, 38)
    f_ls = load(SANS, 16)
    y = put_lines(
        d,
        wrap_text(d, "Nvidia reinstates Jensen Huang as chief executive, "
                     "11 days after his resignation — shares soar 31%, "
                     "gaining $952 billion in a day, their best since 2003.",
                  f_ls, 420),
        lx, y + 4, f_ls, BODY, 21)
    put_lines(
        d,
        wrap_text(d, "Nasdaq jumps 6.5% and the S&P 500 4.7% in the best "
                     "day since April 2025.", load(SANS_B, 14), 420),
        lx, y + 6, load(SANS_B, 14), INK, 18)

    # ---- Row 2: three photos, y 344-460, captions to ~554 ----
    row2 = [
        ("libya.jpg", "WAR  •  UKRAINE",
         "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
         "Kyiv says seven naval drones sank the corvette Merkury "
         "in Benghazi port."),
        ("cop31.jpg", "CLIMATE  •  COP31",
         "COP31 ENDS WITH NO DEAL",
         "The Antalya summit closes without a final pact; focus "
         "shifts to COP32."),
        ("indonesia.jpg", "ASIA  •  INDONESIA",
         "FACTORY FIRE KILLS 24 IN INDONESIA",
         "A blaze at a candy factory in Cikande, Java, leaves 24 "
         "dead and dozens missing."),
    ]
    for (img, kick, head, summ), x in zip(row2, [14, 352, 690]):
        captioned_photo(page, d, os.path.join(PHOTOS, img), x, 344,
                        320, 116, kick, head, summ, 16, 12)

    # ---- Row 3: four photos, y 560-642, captions to ~727 ----
    row3 = [
        ("hormuz.jpg", "MIDDLE EAST  •  HORMUZ",
         "FOURTH TANKER HITS MINE IN HORMUZ",
         "Iran says a fourth oil tanker exploded after striking a "
         "naval mine east of the strait."),
        ("alcaraz.jpg", "TENNIS",
         "ALCARAZ WINS FIRST ATP FINALS TITLE",
         "The Spaniard beats Zverev 6–2, 7–6 in Turin to lift the "
         "season-ending crown."),
        ("chess.jpg", "CHESS",
         "CHESS CROWN DEFENCE BEGINS IN GENEVA",
         "Champion Gukesh opens his title defence against Sindarov "
         "in Game 1."),
        ("wwc.jpg", "FOOTBALL",
         "UK TO HOST 2035 WOMEN'S WORLD CUP",
         "FIFA confirms Britain as host of the 2035 tournament; "
         "USA-led bid gets 2031."),
    ]
    for (img, kick, head, summ), x in zip(row3, [14, 266, 518, 770]):
        captioned_photo(page, d, os.path.join(PHOTOS, img), x, 560,
                        236, 82, kick, head, summ, 13, 11)

    # ---- Round-up: 62 one-liners, 4 columns, heading y 734 ----
    ru_y = 734
    d.line([(14, ru_y), (W - 14, ru_y)], fill=RULE, width=2)
    d.text((14, ru_y + 6), "MORE FROM AROUND THE WORLD — 62 STORIES, 9 REGIONS",
           font=load(SANS_B, 14), fill=RED)
    d.text((W - 14, ru_y + 6), "TUESDAY 24 NOVEMBER 2026",
           font=load(SANS_B, 11), fill=GREY, anchor="ra")

    more = [
        # North America (7)
        "Trump gets new path to erase verdict.",
        "Democrats win House: 258 seats.",
        "Waymo recalls 4,500 robotaxis.",
        "Court clears Iowa azide blast.",
        "Trump set to unveil new tariffs.",
        "'Chapo Isidro' to be tried in Mexico.",
        "Trump: US will sink blockade runners.",
        # Latin America & Caribbean (7)
        "Lula backs second fiscal package.",
        "Car bomb hits governor's office.",
        "Brazil's real weakens on growth cut.",
        "Maduro spends birthday behind bars.",
        "Nicaragua posts record $8.9bn exports.",
        "Costa Rica surgery staff threaten strike.",
        "4 soldiers, 7 gunmen die in cartel arrest.",
        # Europe (7)
        "Allies warn of Russian space nuke.",
        "Leaked data reveals Russian war deaths.",
        "Russia warns Estonia: risk of open war.",
        "Sweden to vote on Kristersson as PM.",
        "Two hurt in Serbia school shooting.",
        "Merz regrets 2008 NATO refusal.",
        "Spain heads to snap election 29 Nov.",
        # Middle East (7)
        "Gaza soil, water poisoned for decades.",
        "Arson hits five West Bank villages.",
        "Riyadh tower targeted in 'terror attack'.",
        "Iraq seizes Kurdistan crossings, oilfields.",
        "UK sanctions Houthis over aggression.",
        "Six Palestinians killed in Gaza strikes.",
        "Israel coalition talks collapse.",
        # Africa (7)
        "175 migrants missing off Senegal.",
        "24 civilians killed in South Sudan.",
        "Boat capsizes in Nigeria, 24 dead.",
        "Senegal reinstated as AFCON champions.",
        "MSF suspends work in South Sudan.",
        "RSF defectors join Sudanese army.",
        "South Africa HIV progress stalled.",
        # South Asia (7)
        "India, Nepal sign eight deals.",
        "Modi opens AI centre at IIT Patna.",
        "India v NZ Test ends in a draw.",
        "Sensex crashes 1,484 points.",
        "Delhi may go BS6-only, court signals.",
        "Bangladesh garment workers clash.",
        "Dhaka: Hasina must come in handcuffs.",
        # East Asia (6)
        "China probes Politburo member Chen.",
        "Huang returns to cheers in China.",
        "Kim ignores Trump's outreach.",
        "India, China hold border talks.",
        "US blacklists Alibaba unit.",
        "Second Chinese official probed.",
        # Southeast Asia & Oceania (7)
        "Solomons to end China security pact.",
        "Australia–Vanuatu treaty blocked.",
        "Fiji closes all schools as drought bites.",
        "Remote Pacific island evacuated.",
        "Pacific elders accuse Australia.",
        "Pacific islands get no COP31 relief.",
        "Wong: US–China rivalry strains peace.",
        # Global / Markets / Tech / Science / Sport (7)
        "Anthropic breaks below $83 IPO price.",
        "CrowdStrike to buy Zscaler, $43.9bn.",
        "Nvidia gives back gains after surge.",
        "Supermoon meets the Pleiades tonight.",
        "Davis Cup finals begin in Bologna.",
        "Brentford hit Everton for four.",
        "US eyes Iran in ship cyberattacks.",
    ]
    assert len(more) == 62, f"round-up must be 62 items, got {len(more)}"
    f_item = load(SANS, 10)
    col_xs = [14, 266, 518, 770]
    sizes = [16, 16, 15, 15]
    end_y = 0
    off = 0
    for ci in range(4):
        x = col_xs[ci]
        y = ru_y + 28
        for item in more[off:off + sizes[ci]]:
            lines = wrap_text(d, "•  " + item, f_item, 236)
            y = put_lines(d, lines, x, y, f_item, BODY, 13)
        end_y = max(end_y, y)
        off += sizes[ci]
    print(f"round-up ends at y={end_y} (page height {H})")

    # ---- Footer ----
    d.line([(14, H - 26), (W - 14, H - 26)], fill=RULE, width=1)
    d.text((W // 2, H - 20),
           "Stories first reported Tuesday 24 November 2026  •  Sources: Reuters, AP, CNN, WSJ, AFP, Al Jazeera",
           font=load(SANS, 11), fill=GREY, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    page.save(out, format="PNG", optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out} {page.size} {size} bytes")
    if size > 1048576:
        page.save(out, format="JPEG", quality=88, optimize=True)
        print(f"PNG too big; rewrote as JPEG {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
