#!/usr/bin/env python3
"""Technique Packet No. 4 — Count the Opposite (complementary counting).
Second packet of the "Art of Counting" (Route C) arc, building straight on the
Multiplication Principle (Packet #3). Named technique = when what you want is
hard to count head-on, count EVERYTHING and subtract the part you don't want:
Wanted = Total - Opposite. An "everything minus the opposite" rectangle graphic,
THREE worked examples spanning the range the ladder demands (at-least-one with
multiplication / "not a special kind" over a plain set / "not all the same"
where the opposite takes a moment to name), then six laddered problems (echo /
vary / hidden), each carrying a three-row Total - Opposite = Answer scaffold so
the total and the opposite must both be shown, not just the final number. Parent
key in full sentences.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
    Table, TableStyle, PageBreak, KeepTogether,
)
from reportlab.graphics.shapes import Drawing, String, Line, Rect

OUTPUT = "/Users/andresrodriguez/Documents/payday_tests/packets/technique_packet_04.pdf"

# ---- page geometry (matches the test playbook) ----
page_w, page_h = letter
left_m = right_m = 0.7 * inch
top_m, bot_m = 0.5 * inch, 0.6 * inch
content_w = page_w - left_m - right_m
content_h = page_h - top_m - bot_m

INK = HexColor("#1a1a1a")
GRAY = HexColor("#666666")
LINE = HexColor("#b8b8b8")
FAINT = HexColor("#cfcfcf")      # scaffold outlines
TINT = HexColor("#f4f1ea")       # warm parchment
TOOL_BG = HexColor("#eef1f4")    # cool tint for the technique box
SHADE = HexColor("#dfe6ec")      # "kept" part of the everything-bar
BAD = HexColor("#e7cfcf")        # the "don't want" chunk

# ---- styles ----
title = ParagraphStyle("title", fontName="Times-Bold", fontSize=22,
                       leading=25, textColor=INK, alignment=TA_CENTER)
subtitle = ParagraphStyle("subtitle", fontName="Times-Italic", fontSize=12.5,
                          leading=16, textColor=GRAY, alignment=TA_CENTER)
nameline = ParagraphStyle("nameline", fontName="Times-Roman", fontSize=11,
                          leading=16, textColor=INK)
body = ParagraphStyle("body", fontName="Times-Roman", fontSize=12,
                      leading=15.5, textColor=INK)
part = ParagraphStyle("part", fontName="Times-Bold", fontSize=14.5,
                      leading=18, textColor=INK, spaceBefore=2, spaceAfter=2)
note = ParagraphStyle("note", fontName="Times-Italic", fontSize=11.5,
                      leading=15, textColor=GRAY)
qstyle = ParagraphStyle("qstyle", fontName="Times-Bold", fontSize=12.5,
                        leading=16, textColor=INK)
alabel = ParagraphStyle("alabel", fontName="Times-Bold", fontSize=11.5,
                        leading=14, textColor=GRAY)
expline = ParagraphStyle("expline", fontName="Times-Roman", fontSize=12,
                         leading=16, textColor=INK)
prob = ParagraphStyle("prob", fontName="Times-Roman", fontSize=12,
                      leading=15.5, textColor=INK)
keyhdr = ParagraphStyle("keyhdr", fontName="Times-Bold", fontSize=15,
                        leading=18, textColor=INK)
caption = ParagraphStyle("caption", fontName="Times-Italic", fontSize=10.5,
                         leading=13.5, textColor=GRAY, alignment=TA_CENTER)


# ---------------------------------------------------------------- drawing bits
def everything_graphic():
    """A full bar = EVERYTHING; a chunk shaded as the part you don't want;
    the rest is what you keep. Total - Opposite = Wanted."""
    w, h = content_w, 150
    d = Drawing(w, h)
    bar_w, bar_h = 360, 46
    bx = (w - bar_w) / 2.0
    by = 72
    keep_w = bar_w * 0.62
    bad_w = bar_w - keep_w
    # the "everything" bracket label
    d.add(String(bx + bar_w / 2, by + bar_h + 20, "EVERYTHING (the total)",
                 fontName="Times-Italic", fontSize=11, fillColor=GRAY,
                 textAnchor="middle"))
    d.add(Line(bx, by + bar_h + 8, bx + bar_w, by + bar_h + 8,
               strokeColor=GRAY, strokeWidth=0.8))
    d.add(Line(bx, by + bar_h + 8, bx, by + bar_h + 3,
               strokeColor=GRAY, strokeWidth=0.8))
    d.add(Line(bx + bar_w, by + bar_h + 8, bx + bar_w, by + bar_h + 3,
               strokeColor=GRAY, strokeWidth=0.8))
    # kept part
    d.add(Rect(bx, by, keep_w, bar_h, fillColor=SHADE, strokeColor=INK,
               strokeWidth=1.0))
    d.add(String(bx + keep_w / 2, by + bar_h / 2 - 5, "what you WANT",
                 fontName="Times-Bold", fontSize=10.5, fillColor=INK,
                 textAnchor="middle"))
    # bad part
    d.add(Rect(bx + keep_w, by, bad_w, bar_h, fillColor=BAD, strokeColor=INK,
               strokeWidth=1.0))
    d.add(String(bx + keep_w + bad_w / 2, by + bar_h / 2 - 5, "DON'T want",
                 fontName="Times-Bold", fontSize=9.5, fillColor=INK,
                 textAnchor="middle"))
    # equation underneath
    d.add(String(w / 2, 34,
                 "what you WANT  =  EVERYTHING  −  the part you DON'T want",
                 fontName="Times-Bold", fontSize=12.5, fillColor=INK,
                 textAnchor="middle"))
    d.add(String(w / 2, 14,
                 "Count the opposite when it is the easier thing to count.",
                 fontName="Times-Italic", fontSize=10.5, fillColor=GRAY,
                 textAnchor="middle"))
    return d


def complement_scaffold():
    """Three rows: total / opposite / subtract = answer. Forces both counts."""
    w, h = content_w, 96
    d = Drawing(w, h)
    lab_x = 4
    line_x = 220
    line_end = w - 6
    rows = [
        (h - 14, "Everything (the total):"),
        (h - 40, "The ones I DON'T want:"),
    ]
    for y, text in rows:
        d.add(String(lab_x, y, text, fontName="Times-Italic", fontSize=11,
                     fillColor=GRAY, textAnchor="start"))
        d.add(Line(line_x, y - 3, line_end, y - 3, strokeColor=FAINT,
                   strokeWidth=1.0))
    # subtract row: ____  -  ____  =  ____
    sy = h - 70
    d.add(String(lab_x, sy, "Subtract:", fontName="Times-Italic", fontSize=11,
                 fillColor=GRAY, textAnchor="start"))
    seg = 86
    x = line_x
    d.add(Line(x, sy - 3, x + seg, sy - 3, strokeColor=FAINT, strokeWidth=1.0))
    x += seg + 8
    d.add(String(x, sy, "−", fontName="Times-Roman", fontSize=13,
                 fillColor=GRAY, textAnchor="middle"))
    x += 14
    d.add(Line(x, sy - 3, x + seg, sy - 3, strokeColor=FAINT, strokeWidth=1.0))
    x += seg + 8
    d.add(String(x, sy, "=", fontName="Times-Roman", fontSize=13,
                 fillColor=GRAY, textAnchor="middle"))
    x += 14
    d.add(Line(x, sy - 3, line_end, sy - 3, strokeColor=FAINT, strokeWidth=1.0))
    return d


# ---------------------------------------------------------------- flowable bits
def boxed(flowables, bg=None, border=LINE, pad=9):
    if not isinstance(flowables, list):
        flowables = [flowables]
    t = Table([[flowables]], colWidths=[content_w])
    style = [
        ("BOX", (0, 0), (-1, -1), 0.8, border),
        ("LEFTPADDING", (0, 0), (-1, -1), pad),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]
    if bg:
        style.append(("BACKGROUND", (0, 0), (-1, -1), bg))
    t.setStyle(TableStyle(style))
    return t


def worked(label, q, lines, drawing=None):
    inner = [Paragraph(label, alabel), Spacer(1, 3), Paragraph(q, qstyle),
             Spacer(1, 5)]
    if drawing is not None:
        inner += [drawing, Spacer(1, 4)]
    for i, text in enumerate(lines, 1):
        inner.append(Paragraph(f"<b>{i}.</b>&nbsp;&nbsp;{text}", expline))
        inner.append(Spacer(1, 4))
    return KeepTogether(boxed(inner))


def problem(n, text):
    flow = [Paragraph(f"<b>{n}.</b>&nbsp;&nbsp;{text}", prob),
            Spacer(1, 4), complement_scaffold(), Spacer(1, 0.85 * inch)]
    return KeepTogether(flow)


story = []

# ---------- PAGE 1 : title, hook, graphic, technique ----------
story.append(Paragraph("Technique Packet No. 4", title))
story.append(Spacer(1, 3))
story.append(Paragraph("Count the Opposite — when the thing you want is hard to "
                       "count, count the rest.", subtitle))
story.append(Spacer(1, 8))
story.append(Paragraph("Name: ______________________      "
                       "Date: ______________________", nameline))
story.append(Spacer(1, 10))

hook = ("A clubhouse door has a secret code: two symbols, and each one is a star, "
        "a moon, or a sun. (You may use a symbol twice.) The door opens only if "
        "the code has <b>at least one star</b>. How many codes open the door?"
        "<br/><br/>"
        "You could hunt for every code with a star in it and hope you catch them "
        "all. Or you could notice that the <i>opposite</i> is much easier to "
        "count: the codes with <b>no star at all</b>. There are 3 × 3 = 9 "
        "codes in total, and the ones with no star use only moon or sun — "
        "2 × 2 = 4 of them. So the codes with at least one star are simply "
        "9 − 4 = 5. This is the whole trick: <b>when what you want is hard "
        "to count head-on, count everything, then subtract the part you "
        "don’t want.</b>")
story.append(boxed(Paragraph(hook, body), bg=TINT))
story.append(Spacer(1, 8))

story.append(everything_graphic())
story.append(Spacer(1, 2))
story.append(Paragraph(
    "Count the whole bar, shade off the part you don’t want, and what is "
    "left is your answer — no hunting required.", caption))
story.append(Spacer(1, 8))

tool = ("<b>THE TECHNIQUE — Count the Opposite.</b><br/>"
        "When counting what you want directly would mean lots of separate "
        "cases:<br/>"
        "&nbsp;&nbsp;<b>1.</b> Count <i>everything</i> — the whole total, "
        "ignoring the condition.<br/>"
        "&nbsp;&nbsp;<b>2.</b> Count the <i>opposite</i> — just the ones "
        "you don’t want. (This is usually the easy part.)<br/>"
        "&nbsp;&nbsp;<b>3.</b> Subtract: total − opposite = what you "
        "want.<br/>"
        "<i>When to reach for it:</i> watch for “at least one,” "
        "“not,” “none,” “no —”, or “not "
        "all the same.” If counting it directly splits into many cases but "
        "the opposite is one tidy group, count the opposite and subtract.")
story.append(boxed(Paragraph(tool, body), bg=TOOL_BG))

story.append(PageBreak())

# ---------- PAGE 2 : worked examples 1 & 2 ----------
story.append(Paragraph("Watch how it works", part))
story.append(Spacer(1, 6))

story.append(worked(
    "WORKED EXAMPLE 1",
    "The clubhouse code is two symbols, each a star, moon, or sun (repeats "
    "allowed). How many codes have at least one star?",
    ["First count <i>everything</i>: two symbols, 3 choices each, so by the "
     "multiplication principle 3 × 3 = 9 codes in all.",
     "Now the opposite — codes with <b>no star</b>. Each symbol can only be "
     "moon or sun, 2 choices each: 2 × 2 = 4 codes.",
     "Subtract: 9 − 4 = <b>5 codes</b> have at least one star.",
     "(Check by listing the good ones: star-star, star-moon, star-sun, "
     "moon-star, sun-star — five, just as promised.)"]))
story.append(Spacer(1, 11))

story.append(worked(
    "WORKED EXAMPLE 2 — the opposite is “the special few”",
    "How many of the numbers 1, 2, 3, …, 30 are NOT multiples of 4?",
    ["Everything first: there are 30 numbers in the list.",
     "The opposite is the easy group — the multiples of 4: 4, 8, 12, 16, "
     "20, 24, 28. That is 7 of them.",
     "Subtract: 30 − 7 = <b>23 numbers</b> are not multiples of 4.",
     "Counting the “not multiples” one by one would be a slog; the "
     "multiples are few and easy to list. Always count whichever side is "
     "smaller."]))

story.append(PageBreak())

# ---------- PAGE 3 : worked example 3 ----------
story.append(Paragraph("Watch how it works (one more)", part))
story.append(Spacer(1, 6))

story.append(worked(
    "WORKED EXAMPLE 3 — when you have to name the opposite yourself",
    "Three friends each spin a spinner with 4 colors: red, green, blue, yellow. "
    "In how many ways do they NOT all land on the same color?",
    ["Everything first: three spins, 4 colors each, so 4 × 4 × 4 = 64 "
     "results in all.",
     "Here the opposite needs a moment of thought. The opposite of “not all "
     "the same” is “all the same” — all red, all green, all "
     "blue, or all yellow.",
     "That opposite is tiny: just <b>4</b> results (one for each color).",
     "Subtract: 64 − 4 = <b>60 ways</b>. The hard-sounding question becomes "
     "one subtraction once you spot what the opposite really is."]))
story.append(Spacer(1, 14))
story.append(Paragraph(
    "All three are the same move: count everything, count the opposite, "
    "subtract. The skill is spotting which group is the easy one.", note))

story.append(PageBreak())

# ---------- PAGE 4 : problems 1-3 ----------
story.append(Paragraph("Now you", part))
story.append(Spacer(1, 3))
story.append(Paragraph("Show the total and the opposite — not just the "
                       "final number.", note))
story.append(Spacer(1, 8))
story.append(problem(1, "A 2-letter tag uses the letters X, Y, Z, and a letter "
                        "may repeat. How many tags have at least one Z?"))
story.append(problem(2, "How many of the numbers 1, 2, 3, …, 25 are NOT "
                        "multiples of 5?"))
story.append(problem(3, "A 3-digit code uses the digits 1, 2, 3, 4, and digits "
                        "may repeat. How many codes have at least one 1?"))

story.append(PageBreak())

# ---------- PAGE 5 : problems 4-6 ----------
story.append(problem(4, "You flip a coin 4 times in a row, writing down heads or "
                        "tails each time. In how many ways do you get at least "
                        "one head?"))
story.append(problem(5, "How many two-digit numbers have at least one digit that "
                        "is a 3? (Remember a two-digit number can’t start "
                        "with 0.)"))
story.append(problem(6, "Three friends each spin a spinner with 4 colors: red, "
                        "green, blue, yellow. In how many ways do they NOT all "
                        "land on the same color?"))

story.append(PageBreak())

# ---------- PAGE 6 : parent key ----------
story.append(Paragraph("Answer Key — for parents", keyhdr))
story.append(Spacer(1, 8))

k_intro = ("<b>What this packet teaches.</b> One named technique — when what "
           "you want is hard to count head-on, count everything and subtract the "
           "part you don’t want (Wanted = Total − Opposite) — shown "
           "first (the clubhouse hook, the bar picture, and three worked "
           "examples), then applied six times. It builds directly on Packet #3: "
           "the total and the opposite are each found with the multiplication "
           "principle. The three worked examples are deliberately different "
           "<i>kinds</i> of the same move: “at least one” where the "
           "opposite is “none” (1), “not a special kind” where "
           "the opposite is the easy handful (2), and “not all the same” "
           "where you must name the opposite yourself (3) — so every kind of "
           "problem below has been modeled before they meet it. Each problem has "
           "a three-row box printed under it: the goal is to see the total and "
           "the opposite, not just the total.")
story.append(Paragraph(k_intro, body))
story.append(Spacer(1, 10))

k_ans = ("<b>Answers.</b><br/>"
         "&nbsp;&nbsp;<b>1.</b>&nbsp; Total 3 × 3 = 9 tags; opposite (no Z, "
         "so only X or Y) 2 × 2 = 4; so 9 − 4 = <b>5</b>. (Echoes "
         "Worked Example 1.)<br/>"
         "&nbsp;&nbsp;<b>2.</b>&nbsp; Total 25 numbers; opposite (multiples of "
         "5: 5, 10, 15, 20, 25) = 5; so 25 − 5 = <b>20</b>. (Echoes Worked "
         "Example 2.)<br/>"
         "&nbsp;&nbsp;<b>3.</b>&nbsp; Total 4 × 4 × 4 = 64 codes; "
         "opposite (no 1, so 3 choices each) 3 × 3 × 3 = 27; so "
         "64 − 27 = <b>37</b>.<br/>"
         "&nbsp;&nbsp;<b>4.</b>&nbsp; Total 2 × 2 × 2 × 2 = 16 "
         "results; the opposite of “at least one head” is <i>no heads "
         "at all</i> — all four tails, just <b>1</b> result; so 16 − 1 "
         "= <b>15</b>. (The opposite can be a single case.)<br/>"
         "&nbsp;&nbsp;<b>5.</b>&nbsp; Total two-digit numbers: 90 (10 through "
         "99). Opposite (no 3 anywhere): the tens digit is 1–9 but not 3, so "
         "8 choices, and the ones digit is 0–9 but not 3, so 9 choices — "
         "8 × 9 = 72. So 90 − 72 = <b>18</b>. (The no-0-in-the-tens "
         "restriction is the trap, just like Packet #3’s last problem.)<br/>"
         "&nbsp;&nbsp;<b>6.</b>&nbsp; Total 4 × 4 × 4 = 64; opposite "
         "(“all the same”: all red, all green, all blue, all yellow) "
         "= 4; so 64 − 4 = <b>60</b>. (Echoes Worked Example 3 — the "
         "opposite must be named.)")
story.append(Paragraph(k_ans, body))
story.append(Spacer(1, 10))

k_watch = ("<b>What to watch for.</b> Three slips. First, <b>counting the hard "
           "side anyway</b> — if they start listing every code that has a "
           "star, steer them to the opposite (“which is easier to count, the "
           "ones with a star or the ones with none?”). Second, <b>forgetting "
           "to subtract</b> — they find the total and the opposite, then "
           "write one of those as the answer; the box’s third row is there "
           "to force the subtraction. Third, <b>mis-naming the opposite</b> — "
           "on problem 6 the opposite of “not all the same” is “all "
           "the same” (not “all different”), and on problem 4 it is "
           "“all tails” (a single outcome). Problems 5 and 6 are the "
           "stretch: 5 hides the no-0 restriction inside the opposite count, and "
           "6 makes them figure out what the opposite even is.")
story.append(Paragraph(k_watch, body))
story.append(Spacer(1, 10))

k_run = ("<b>How to run it.</b> Read the hook, the bar picture, and all three "
         "worked examples out loud together before they touch problem 1. The "
         "problems they do solo, in one sitting or two. This is a learning "
         "packet, not a test: helping on a stuck problem is fine, but help by "
         "pointing back at the matching worked example — and at the "
         "Total − Opposite box — not at the answer.")
story.append(Paragraph(k_run, body))

# ---------- build ----------
frame = Frame(left_m, bot_m, content_w, content_h,
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
tpl = PageTemplate(id="main", frames=[frame])
doc = BaseDocTemplate(OUTPUT, pagesize=letter,
                      leftMargin=left_m, rightMargin=right_m,
                      topMargin=top_m, bottomMargin=bot_m,
                      pageTemplates=[tpl])
doc.build(story)
print("wrote", OUTPUT)
