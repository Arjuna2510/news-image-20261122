#!/usr/bin/env python3
"""Draw the front page for Sunday 22 November 2026.

Build-time generator (run on the author's machine; the submitted
entrypoint main.ts simply copies the entry.png this script produces).
Every headline below is a real story reported on 22 November 2026
(or late on 21 November in the Americas, i.e. 22 November in Asia),
checked against Reuters, AFP, AP, BBC, Al Jazeera, Euronews, UKMTO
and the wires. See README.md for the story list with sources.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 233)
INK = (18, 18, 18)
NAVY = (13, 26, 51)
RED = (172, 30, 30)
RULE = (120, 110, 94)
GREY = (94, 90, 82)
LAND = (203, 194, 172)
SEA = (214, 226, 232)
GULF_SEA = (196, 214, 222)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap_lines(draw, text, fnt, width):
    """Greedy word wrap to a pixel width."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def fit(draw, text, fnt, width, max_lines):
    """Wrap, then trim words (with ellipsis) until it fits max_lines."""
    lines = wrap_lines(draw, text, fnt, width)
    while len(lines) > max_lines and len(lines) > 1:
        words = " ".join(lines).split()
        # Drop any ellipsis the previous trim added: trimming it and
        # re-adding it would rebuild the identical text forever.
        while words and words[-1] == "...":
            words.pop()
        if not words:
            return ["..."]
        words = words[:-1]
        lines = wrap_lines(draw, " ".join(words) + " ...", fnt, width)
    return lines


def text_block(draw, x, y, lines, fnt, color, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


# ------------------------------------------------------------------ stories
# (headline, deck)
LEAD = (
    "IRAN HITS U.S. BASES IN BAHRAIN AGAIN",
    "Tehran's Revolutionary Guards say they struck two American bases on "
    "Saturday night \u2014 Sheikh Isa air base and the Navy's Juffair facility, "
    "home of the Fifth Fleet \u2014 as a tanker is hit off Oman and shipping "
    "through the Strait of Hormuz stays under fire.",
)

FEATURES = [
    ("NATO: EVERY INCH OF POLAND",
     "Rutte, in Warsaw after Russian missiles fell in Poland, vows NATO "
     "will defend every inch. The council meets on Monday."),
    ("COP31: A GOOD DEAL OR NO DEAL",
     "Talks in Antalya spill into overtime, nearly 200 nations deadlocked "
     "over fossil fuels and finance. The EU warns of no deal."),
    ("TRUMP AND XI MEET IN SHENZHEN",
     "The leaders sit down at the APEC summit, a trilateral with Putin "
     "planned. Trump says an Iran deal could last 20 years."),
]

ASIA = [
    ("EU and Indonesia sign trade deal",
     "Ten years of talks; tariffs on 98.5% of goods to go."),
    ("Hong Kong votes for Election Committee",
     "Some 5,700 voters choose the committee's members."),
    ("Japanese troops to train in India",
     "A first: Japanese forces will use Indian facilities."),
    ("Cyclone Akvan disrupts Ranchi flights",
     "Fourteen flights cancelled at Ranchi airport."),
    ("Modi opens Nitish Setu in Bihar",
     "New bridge links Patna and Vaishali across the Ganges."),
    ("India face New Zealand in Wellington",
     "Confident India meet the hosts in windy Wellington."),
    ("Cummins keeps Australia captaincy",
     "Cricket Australia backs him unanimously as captain."),
    ("Australia edge England in T20 thriller",
     "Hosts win the first T20 of the series at the MCG."),
    ("Snow traps 1,500 in Fukushima",
     "Heavy snow strands travellers in Fukushima region."),
    ("Seoul offers $75,000 exam-cheating bounty",
     "Seoul repeats its reward for reporting exam cheating."),
    ("India's ICMR hits 100 tech transfers",
     "Health body signs 20 licensing deals at its summit."),
]

EUROPE = [
    ("Estonia to shut Russia border",
     "Road crossings close for six months from 1 December."),
    ("Lviv counts its dead after strike",
     "Two killed, ten hurt as missiles hit a station."),
    ("Drones hit Russian ship in Baltic",
     "Sparta II catches fire in the Gulf of Finland."),
    ("France turns to UN over Myanmar",
     "Paris seeks UN Security Council action over Myanmar."),
    ("UK and EU strike new deals",
     "Youth mobility, food trade and carbon deals agreed."),
    ("EU floats 3% levy on big tech",
     "Costa proposes a big-tech tax; France rejects the plan."),
    ("Four killed in Gaza ceasefire breaches",
     "Palestinians die in Israeli strikes across the Strip."),
    ("Saudi shoots down Houthi missiles",
     "Three missiles headed for Riyadh are intercepted."),
    ("Houthi strikes hit Riyadh",
     "Missiles reach the Saudi capital after an operation."),
    ("Denmark blames Russia for murder plot",
     "Denmark says Moscow plotted to kill a US-Ukrainian."),
    ("Zelensky floats G20 peace talks",
     "Kyiv suggests new peace talks could be held at G20."),
]

AMERICAS = [
    ("6.7 quake shakes Peru's Andes",
     "Tremor rattles central Peru and is felt in Lima."),
    ("Bolsonaro taken to intensive care",
     "Jailed ex-president is stable with a bowel obstruction."),
    ("Mexico seizes cartel boss \u2018El Chapo Isidro\u2019",
     "FBI most-wanted fugitive seized in Sinaloa; 11 killed."),
    ("One in four women \u2018cannot refuse sex\u2019",
     "UN report: share rises to one in three in Arab states."),
    ("England thrash the All Blacks",
     "Record-margin win over New Zealand at Twickenham."),
    ("US airlines warned of terror threat",
     "Al-Qaeda-linked attacks flagged before Thanksgiving."),
    ("Bed bugs shut FEMA's HQ office",
     "Over 1,000 emergency staff told to work from home."),
    ("Trump curbs contractors' Congress contact",
     "Federal contractors must clear Congress requests first."),
    ("Third US carrier reaches Middle East",
     "Another US carrier arrives as the Gulf crisis deepens."),
    ("Hegseth redraws US-Canada defence ties",
     "US defence chief sets fresh limits on the partnership."),
    ("Melania Trump seeks more ceasefires",
     "First lady wants more ceasefires before Christmas."),
]

# (number, lon, lat, place, dx, dy) — dx/dy nudge crowded dots apart.
DOTS = [
    (1, 50.6, 26.2, "Bahrain", -8, 2),
    (2, 47.9, 29.3, "Kuwait", 8, -9),
    (3, 56.3, 26.6, "Hormuz", 11, 7),
    (4, 24.0, 49.8, "Lviv", -9, -3),
    (5, 21.0, 52.2, "Warsaw", 9, -9),
    (6, 30.7, 36.9, "Antalya", 3, 11),
    (7, 114.1, 22.5, "Shenzhen", -5, -9),
    (8, 114.2, 22.3, "Hong Kong", 11, 7),
    (9, 106.8, -6.2, "Jakarta", 0, 0),
    (10, -77.0, -12.0, "Lima", 0, 0),
    (11, -47.9, -15.8, "Brasilia", 0, 0),
    (12, -107.4, 24.8, "Sinaloa", 0, 0),
    (13, 24.7, 59.4, "Tallinn", -4, -11),
]

# Rough continent outlines (lon, lat), equirectangular.
N_AMERICA = [(-168, 66), (-158, 58), (-148, 60), (-140, 60), (-132, 56), (-125, 49),
             (-124, 42), (-120, 34), (-114, 29), (-110, 24), (-105, 20), (-97, 16),
             (-92, 15), (-86, 12), (-83, 9), (-79, 8), (-77, 7), (-80, 3), (-81, -4),
             (-77, -12), (-72, -18), (-70, -23), (-72, -37), (-73, -44), (-74, -52),
             (-70, -54), (-66, -55), (-68, -50), (-62, -41), (-58, -34), (-52, -32),
             (-48, -28), (-41, -23), (-35, -9), (-40, -3), (-44, -3), (-50, 0),
             (-52, 4), (-58, 6), (-62, 9), (-68, 11), (-72, 12), (-76, 10), (-80, 9),
             (-83, 9), (-86, 13), (-90, 14), (-92, 15), (-97, 16), (-105, 20),
             (-114, 29), (-120, 34), (-125, 40), (-124, 48), (-130, 55), (-135, 58),
             (-145, 60), (-155, 58), (-162, 58), (-168, 66)]
AFRICA = [(-17, 15), (-17, 21), (-10, 31), (-5, 35), (0, 36), (10, 37), (11, 34),
          (20, 32), (25, 32), (30, 31), (32, 31), (34, 28), (37, 22), (39, 18),
          (43, 12), (48, 11), (51, 12), (44, 5), (41, 0), (40, -5), (40, -10),
          (39, -15), (36, -20), (33, -26), (28, -33), (20, -35), (17, -32),
          (15, -27), (12, -18), (12, -10), (9, -1), (9, 4), (-8, 4), (-13, 8),
          (-17, 12), (-17, 15)]
EURASIA = [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-1, 49),
           (2, 51), (5, 53), (8, 55), (8, 57), (10, 58), (5, 60), (5, 62), (10, 64),
           (13, 66), (18, 69), (25, 71), (30, 70), (35, 68), (40, 68), (45, 68),
           (50, 69), (55, 69), (60, 69), (65, 69), (70, 72), (75, 72), (80, 73),
           (85, 74), (90, 75), (95, 76), (100, 77), (105, 77), (110, 76), (115, 73),
           (120, 73), (125, 72), (130, 72), (135, 72), (140, 72), (145, 72),
           (150, 70), (155, 69), (160, 69), (162, 66), (160, 62), (158, 58),
           (156, 52), (150, 59), (142, 55), (140, 50), (138, 46), (135, 43),
           (132, 43), (130, 42), (128, 38), (127, 35), (126, 33), (122, 31),
           (120, 28), (118, 25), (112, 22), (108, 18), (106, 10), (104, 9),
           (101, 7), (100, 6), (98, 8), (97, 10), (95, 15), (93, 18), (91, 22),
           (89, 22), (87, 21), (85, 19), (82, 17), (80, 15), (80, 13), (77, 8),
           (76, 10), (74, 13), (72, 20), (70, 22), (66, 25), (62, 25), (58, 25),
           (56, 27), (54, 27), (52, 26), (50, 26), (48, 29), (48, 30), (50, 29),
           (52, 28), (54, 26), (56, 26), (58, 24), (59, 22), (55, 17), (52, 15),
           (48, 14), (44, 13), (43, 12), (40, 15), (38, 18), (36, 21), (35, 24),
           (34, 28), (35, 31), (36, 36), (34, 36), (30, 36), (27, 37), (26, 38),
           (23, 36), (22, 37), (19, 40), (18, 42), (14, 45), (12, 44), (8, 44),
           (3, 43), (0, 40), (-2, 37), (-6, 36), (-9, 37), (-10, 36)]
AUSTRALIA = [(114, -22), (114, -30), (115, -35), (118, -35), (124, -33), (129, -32),
             (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
             (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
             (137, -12), (135, -12), (132, -11), (130, -13), (126, -14), (122, -17),
             (118, -20), (114, -22)]
GREENLAND = [(-58, 64), (-52, 60), (-45, 60), (-40, 64), (-32, 68), (-22, 70),
             (-20, 74), (-30, 76), (-45, 76), (-58, 74), (-60, 70), (-58, 64)]
BRITAIN = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
           (-3, 50), (-5, 50)]
JAPAN = [(130, 31), (132, 33), (135, 34), (137, 35), (139, 36), (140, 38),
         (141, 40), (142, 42), (143, 44), (141, 45), (140, 44), (139, 42),
         (137, 39), (135, 36), (133, 34), (130, 31)]


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 30
    CW = W - 2 * M  # 964

    # ---------------------------------------------------------- masthead
    title = "THE WORLD TODAY"
    tf = F(SERIF_B, 68)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 18), title, font=tf, fill=NAVY)
    d.line([(M, 96), (W - M, 96)], fill=INK, width=3)
    d.line([(M, 101), (W - M, 101)], fill=INK, width=1)
    sf = F(SANS_B, 15)
    d.text((M, 108), "SUNDAY, 22 NOVEMBER 2026", font=sf, fill=INK)
    mid = "THE DAY'S WORLD NEWS \u2014 IN ONE PAGE"
    d.text(((W - d.textlength(mid, font=sf)) / 2, 108), mid, font=sf, fill=GREY)
    right = "No. 326  \u00b7  FREE"
    d.text((W - M - d.textlength(right, font=sf), 108), right, font=sf, fill=INK)

    # ---------------------------------------------------------- lead story
    y = 136
    lead_w = 600
    kf = F(SANS_B, 14)
    d.text((M, y), "LEAD \u2014 THE GULF", font=kf, fill=RED)
    y += 20
    hf = F(SERIF_B, 38)
    lines = fit(d, LEAD[0], hf, lead_w, 2)
    y = text_block(d, M, y, lines, hf, INK, 43)
    y += 4
    df = F(SERIF, 17)
    lines = fit(d, LEAD[1], df, lead_w, 4)
    y = text_block(d, M, y, lines, df, INK, 22)

    # Gulf flashpoint mini-map, right of the lead
    gx, gy, gw, gh = M + lead_w + 24, 136, CW - lead_w - 24, 196
    d.rectangle([gx, gy, gx + gw, gy + gh], fill=GULF_SEA, outline=RULE, width=1)
    # stylised Arabian peninsula + Gulf coastline
    pen = [(gx + 150, gy + 18), (gx + 210, gy + 22), (gx + 250, gy + 48),
           (gx + 262, gy + 92), (gx + 238, gy + 140), (gx + 196, gy + 158),
           (gx + 150, gy + 138), (gx + 128, gy + 96), (gx + 132, gy + 52)]
    d.polygon(pen, fill=LAND, outline=RULE)
    d.text((gx + 168, gy + 78), "ARABIA", font=F(SANS_B, 11), fill=GREY)
    gdots = [("KUWAIT", gx + 178, gy + 30), ("BAHRAIN", gx + 218, gy + 44),
             ("QESHM", gx + 252, gy + 66), ("HORMUZ", gx + 238, gy + 92),
             ("OMAN", gx + 250, gy + 128)]
    for name, px, py in gdots:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED, outline=PAPER, width=1)
        d.text((px + 7, py - 6), name, font=F(SANS_B, 10), fill=INK)
    d.text((gx + 8, gy + 6), "FLASHPOINT: THE GULF", font=F(SANS_B, 12), fill=NAVY)
    d.text((gx + 8, gy + gh - 18), "Tankers hit off Oman; strait traffic far below normal.",
           font=F(SANS, 10), fill=GREY)

    # ---------------------------------------------------------- features
    y = 340
    d.line([(M, y), (W - M, y)], fill=INK, width=2)
    y += 10
    col_w = (CW - 2 * 18) / 3
    fx = M
    for head, deck in FEATURES:
        d.text((fx, y), "FEATURE", font=F(SANS_B, 12), fill=RED)
        hh = fit(d, head, F(SERIF_B, 20), col_w, 2)
        yy = text_block(d, fx, y + 17, hh, F(SERIF_B, 20), INK, 23)
        dd = fit(d, deck, F(SANS, 13), col_w, 3)
        text_block(d, fx, yy + 3, dd, F(SANS, 13), INK, 17)
        fx += col_w + 18
    y += 130

    # ---------------------------------------------------------- locator map
    d.line([(M, y), (W - M, y)], fill=INK, width=2)
    y += 8
    d.text((M, y), "WHERE THE NEWS HAPPENED", font=F(SANS_B, 13), fill=NAVY)
    y += 20
    mx, my, mw, mh = M, y, CW, 86
    d.rectangle([mx, my, mx + mw, my + mh], fill=SEA, outline=RULE, width=1)

    def proj(lon, lat):
        px = mx + (lon + 180) / 360.0 * mw
        py = my + (80 - lat) / 135.0 * mh
        return px, py

    for poly in (N_AMERICA, AFRICA, EURASIA, AUSTRALIA, GREENLAND, BRITAIN, JAPAN):
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND, outline=RULE)
    for num, lon, lat, _place, dx, dy in DOTS:
        px, py = proj(lon, lat)
        px, py = px + dx, py + dy
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=PAPER, width=1)
        d.text((px, py), str(num), font=F(SANS_B, 9), fill=(255, 255, 255),
               anchor="mm")
    y = my + mh + 6
    lf = F(SANS, 11)
    key = ("1 Bahrain  2 Kuwait  3 Hormuz  4 Lviv  5 Warsaw  6 Antalya  "
           "7 Shenzhen  8 Hong Kong  9 Jakarta  10 Lima  11 Bras\u00edlia  "
           "12 Sinaloa  13 Tallinn")
    d.text((M, y), key, font=lf, fill=GREY)

    # ---------------------------------------------------------- region grid
    y += 22
    d.line([(M, y), (W - M, y)], fill=INK, width=2)
    y += 8
    headers = ["ASIA & THE PACIFIC", "EUROPE & THE MIDDLE EAST",
               "AFRICA & THE AMERICAS"]
    regions = [ASIA, EUROPE, AMERICAS]
    col_x = [M, M + col_w + 18, M + 2 * (col_w + 18)]
    for cx, head in zip(col_x, headers):
        d.rectangle([cx, y, cx + col_w, y + 24], fill=NAVY)
        d.text((cx + 8, y + 4), head, font=F(SANS_B, 13), fill=(255, 255, 255))
    y += 32
    hf2 = F(SERIF_B, 13)
    df2 = F(SANS, 11)
    row_h = 30
    for i in range(11):
        for cx, region in zip(col_x, regions):
            head, deck = region[i]
            hh = fit(d, head, hf2, col_w - 4, 1)
            yy = text_block(d, cx, y, hh, hf2, INK, 15)
            dd = fit(d, deck, df2, col_w - 4, 1)
            text_block(d, cx, yy, dd, df2, GREY, 13)
        y += row_h
        if i < 10:
            for cx in col_x:
                d.line([(cx, y - 5), (cx + col_w, y - 5)], fill=(206, 198, 184), width=1)

    # ---------------------------------------------------------- footer
    y += 2
    d.line([(M, y), (W - M, y)], fill=INK, width=2)
    y += 7
    ff = F(SANS, 10)
    d.text((M, y), "Sources: Reuters, AFP, AP, BBC, Al Jazeera, Euronews, UKMTO, "
                   "national wires. Drawn in code \u2014 no photographs.",
           font=ff, fill=GREY)
    y += 14
    d.text((M, y), "Stories reported on Sunday 22 November 2026, or late on "
                   "21 November in the Americas. All figures as reported; "
                   "claims not independently verified are labelled as claims.",
           font=ff, fill=GREY)
    print("final y:", y)
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    draw().save(out, optimize=True)
    print("wrote", out)
