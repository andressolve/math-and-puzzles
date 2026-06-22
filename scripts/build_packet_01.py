#!/usr/bin/env python3
"""Technique Packet No. 1 — Pairing (the Gauss move).
First of the contest-prep packet series: named technique + when to reach
for it, two worked examples written line-by-line (the explanation genre
from the Judge sheets), then six laddered problems (echo / vary / hidden),
and a parent key in full sentences.
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
from reportlab.graphics.shapes import Drawing, String, Path

OUTPUT = "/Users/andresrodriguez/Documents/payday_tests/packets/technique_packet_01.pdf"

# ---- page geometry (matches the test playbook) ----
page_w, page_h = letter
left_m = right_m = 0.7 * inch
top_m, bot_m = 0.5 * inch, 0.6 * inch
content_w = page_w - left_m - right_m
content_h = page_h - top_m - bot_m

INK = HexColor("#1a1a1a")
GRAY = HexColor("#666666")
LINE = HexColor("#b8b8b8")
TINT = HexColor("#f4f1ea")      # warm parchment
TOOL_BG = HexColor("#eef1f4")   # cool tint for the technique box
ARC = HexColor("#4a5a6a")       # muted slate for the pairing arcs

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


def pairing_drawing():
    """Row 1 2 3 ··· 98 99 100 with three nested arcs pairing the ends,
    each labelled 101 — the Gauss move made visible."""
    w, h = content_w, 142
    d = Drawing(w, h)
    labels = ["1", "2", "3", "···", "98", "99", "100"]
    n = len(labels)
    margin = 36
    usable = w - 2 * margin
    xs = [margin + usable * i / (n - 1) for i in range(n)]
    y_num = 10
    for x, lab in zip(xs, labels):
        d.add(String(x, y_num, lab, fontName="Times-Roman", fontSize=13.5,
                     fillColor=INK, textAnchor="middle"))
    for x1, x2 in zip(xs, xs[1:]):
        d.add(String((x1 + x2) / 2.0, y_num, "+", fontName="Times-Roman",
                     fontSize=13.5, fillColor=GRAY, textAnchor="middle"))
    y0 = 34
    for li, ri, apex in [(0, 6, 118), (1, 5, 90), (2, 4, 62)]:
        x1, x2 = xs[li], xs[ri]
        c = (apex - y0) * 4.0 / 3.0
        p = Path(strokeColor=ARC, strokeWidth=1.4, fillColor=None)
        p.moveTo(x1, y0)
        p.curveTo(x1, y0 + c, x2, y0 + c, x2, y0)
        d.add(p)
        d.add(String((x1 + x2) / 2.0, apex + 4, "101", fontName="Times-Italic",
                     fontSize=11, fillColor=ARC, textAnchor="middle"))
    return d


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


def worked(label, q, lines):
    inner = [Paragraph(label, alabel), Spacer(1, 3),
             Paragraph(q, qstyle), Spacer(1, 7)]
    for i, text in enumerate(lines, 1):
        inner.append(Paragraph(f"<b>{i}.</b>&nbsp;&nbsp;{text}", expline))
        inner.append(Spacer(1, 5))
    return KeepTogether(boxed(inner))


def problem(n, text, space=1.3):
    flow = [Paragraph(f"<b>{n}.</b>&nbsp;&nbsp;{text}", prob),
            Spacer(1, space * inch)]
    return KeepTogether(flow)


story = []

# ---------- PAGE 1 : title, story, technique, worked example 1 ----------
story.append(Paragraph("Technique Packet No. 1", title))
story.append(Spacer(1, 3))
story.append(Paragraph("Pairing — the trick a nine-year-old used to beat his teacher.",
                       subtitle))
story.append(Spacer(1, 8))
story.append(Paragraph("Name: ______________________      "
                       "Date: ______________________", nameline))
story.append(Spacer(1, 10))

hook = ("Almost 250 years ago in Germany, a schoolteacher wanted a few minutes "
        "of peace. So he handed his class what sounded like a punishment: add up "
        "every whole number from 1 to 100. Heads went down and chalk started "
        "scratching — 1, then 1 + 2 = 3, then 3 + 3 = 6, then 6 + 4 = 10 — a "
        "long, slow march toward 100.<br/><br/>"
        "But one boy just sat and thought. A few seconds later he walked up and "
        "set his slate on the desk. On it was a single number: <b>5050</b>. The "
        "teacher was sure he had cheated — he hadn’t. The boy was nine-year-old "
        "<b>Carl Gauss</b>, and he had seen something the marchers missed: pair "
        "the first number with the last, and <b>1 + 100 = 101</b>. Pair the next "
        "two in from the ends, and <b>2 + 99 = 101</b>. And <b>3 + 98 = 101</b>. "
        "Every pair makes the same total, 101 — and there are 50 of them, so the "
        "whole sum is just <b>50 × 101 = 5050</b>. Gauss grew up to become one of "
        "the greatest mathematicians who ever lived, and this little move still "
        "carries his name.")
story.append(boxed(Paragraph(hook, body), bg=TINT))
story.append(Spacer(1, 10))

story.append(pairing_drawing())
story.append(Spacer(1, 2))
story.append(Paragraph(
    "Every pair from the outside in makes 101 — and there are 50 pairs, "
    "so 50 × 101 = 5050.", caption))
story.append(Spacer(1, 10))

tool = ("<b>THE TECHNIQUE — Pairing.</b><br/>"
        "To add a long, evenly spaced run of numbers:<br/>"
        "&nbsp;&nbsp;<b>1.</b> Pair the first number with the last, the second "
        "with the second-to-last, and so on.<br/>"
        "&nbsp;&nbsp;<b>2.</b> Check: every pair adds to the <b>same total</b>.<br/>"
        "&nbsp;&nbsp;<b>3.</b> Count the pairs and multiply.<br/>"
        "&nbsp;&nbsp;<b>4.</b> Odd count of numbers? The middle one has no "
        "partner — add it at the end.<br/>"
        "<i>When to reach for it:</i> whenever a problem asks you to add a long, "
        "evenly spaced run of numbers — don’t march, pair.")
story.append(boxed(Paragraph(tool, body), bg=TOOL_BG))
story.append(Spacer(1, 10))

story.append(PageBreak())

# ---------- PAGE 2 : worked examples 1 & 2 ----------
story.append(worked(
    "WORKED EXAMPLE 1",
    "Find 1 + 2 + 3 + … + 20.",
    ["Pair the ends: 1 + 20 = 21, &nbsp;2 + 19 = 21, &nbsp;3 + 18 = 21 — every "
     "pair makes 21.",
     "The 20 numbers form 10 pairs.",
     "So the sum is 10 × 21 = <b>210</b>."]))
story.append(Spacer(1, 12))

story.append(worked(
    "WORKED EXAMPLE 2 — when the count is odd",
    "Find 1 + 2 + 3 + … + 9.",
    ["Pair the ends: 1 + 9 = 10, &nbsp;2 + 8 = 10, &nbsp;3 + 7 = 10, "
     "&nbsp;4 + 6 = 10.",
     "Nine numbers make 4 pairs — and the 5 in the middle has no partner.",
     "The pairs give 4 × 10 = 40, and the leftover 5 brings it to 45.",
     "So 1 + 2 + … + 9 = <b>45</b>."]))

story.append(PageBreak())

# ---------- PAGE 3 : problems 1–3 ----------
story.append(Paragraph("Now you", part))
story.append(Spacer(1, 6))
story.append(problem(1, "Find 1 + 2 + 3 + … + 40.", space=2.9))
story.append(problem(2, "Find 5 + 6 + 7 + … + 14.", space=2.9))
story.append(problem(3, "Find 2 + 4 + 6 + … + 20.", space=2.9))

story.append(PageBreak())

# ---------- PAGE 4 : problems 4–6 ----------
story.append(problem(4, "Find 1 + 2 + 3 + … + 99.", space=2.9))
story.append(problem(
    5, "A staircase is made of blocks. The first step is 1 block tall, the "
       "second is 2 blocks tall, the third is 3 blocks, and so on up to the "
       "12th step. How many blocks does the whole staircase use?", space=2.9))
story.append(problem(
    6, "Mia adds 1 + 2 + 3 + … and stops the moment her total reaches exactly "
       "45. What is the last number she adds?", space=2.9))

story.append(PageBreak())

# ---------- PAGE 4 : parent key ----------
story.append(Paragraph("Answer Key — for parents", keyhdr))
story.append(Spacer(1, 8))

k_intro = ("<b>What this packet teaches.</b> One named technique — pairing — "
           "shown first (story + two worked examples), then applied six times. "
           "The early problems look like the examples; the later ones hide the "
           "technique inside a situation, which is what contests do. The worked "
           "examples are written one sentence per line on purpose — they double "
           "as models of written explanations.")
story.append(Paragraph(k_intro, body))
story.append(Spacer(1, 10))

k_ans = ("<b>Answers.</b><br/>"
         "&nbsp;&nbsp;<b>1.</b>&nbsp; 1–40: 20 pairs, each adding to 41 → "
         "20 × 41 = <b>820</b>.<br/>"
         "&nbsp;&nbsp;<b>2.</b>&nbsp; 5–14 is ten numbers: 5 pairs of 19 "
         "(5+14, 6+13, …) → <b>95</b>. The run not starting at 1 changes "
         "nothing — pairing only needs even spacing.<br/>"
         "&nbsp;&nbsp;<b>3.</b>&nbsp; 2, 4, … 20 is ten numbers: 5 pairs of 22 "
         "→ <b>110</b>.<br/>"
         "&nbsp;&nbsp;<b>4.</b>&nbsp; 1–99 is ninety-nine numbers — odd count, "
         "like Worked Example 2: 49 pairs of 100 plus the middle 50 → "
         "<b>4950</b>.<br/>"
         "&nbsp;&nbsp;<b>5.</b>&nbsp; The blocks are 1 + 2 + … + 12: 6 pairs "
         "of 13 → <b>78</b>. Nobody says “add a run of numbers” — they have to "
         "see the staircase <i>is</i> one.<br/>"
         "&nbsp;&nbsp;<b>6.</b>&nbsp; Backwards: 45 is exactly Worked Example "
         "2’s total, so her last number is <b>9</b>. Reaching 45 by pairing "
         "guesses (try 1–10 = 55, too big; 1–9 = 45) is just as good.")
story.append(Paragraph(k_ans, body))
story.append(Spacer(1, 10))

k_watch = ("<b>What to watch for.</b> The marching habit — adding 1 + 2 = 3, "
           "+ 3 = 6, + 4 = 10 … — gets the right answer on 1 and 2 and then "
           "collapses on 4. If you see marching, don’t correct it; wait for "
           "problem 4 to make the argument for you. On problem 2, the common "
           "slip is counting eleven numbers from 5 to 14 (it’s ten — count on "
           "fingers once).")
story.append(Paragraph(k_watch, body))
story.append(Spacer(1, 10))

k_run = ("<b>How to run it.</b> Read the story and the technique box together, "
         "out loud — then walk through both worked examples before they touch "
         "problem 1. The problems they do solo, in one sitting or two. This is "
         "a learning packet, not a test: helping on a stuck problem is fine, "
         "but help by pointing back at the worked examples, not at the answer.")
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
