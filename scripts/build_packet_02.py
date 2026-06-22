#!/usr/bin/env python3
"""Technique Packet No. 2 — Working Backwards.
Second contest-prep packet: named technique + when to reach for it, a
forward/undo chain graphic, THREE worked examples that span the range the
ladder demands (vanilla number-machine, a disguised repeated-undo, and a
reverse-order trap), then six laddered problems (echo / vary / hidden) and a
parent key in full sentences. Calibrated a touch more accessible than #1.
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
from reportlab.graphics.shapes import Drawing, String, Line, Rect, Polygon

OUTPUT = "/Users/andresrodriguez/Documents/payday_tests/packets/technique_packet_02.pdf"

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
ARC = HexColor("#4a5a6a")       # muted slate for the backward chain

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


def chain_drawing():
    """Forward chain (left->right, doing the steps) above the undo chain
    (right->left, undoing them last-first) — the technique made visible."""
    w, h = content_w, 152
    d = Drawing(w, h)
    bw, bh = 64, 30
    gap = 78
    total = 3 * bw + 2 * gap
    lm = (w - total) / 2.0
    xs = [lm + i * (bw + gap) for i in range(3)]  # left edges
    y_top, y_bot = 100, 28

    def box(x, y, label, fill=None, txt=INK, stroke=INK):
        d.add(Rect(x, y, bw, bh, fillColor=fill, strokeColor=stroke,
                   strokeWidth=1.1))
        d.add(String(x + bw / 2, y + bh / 2 - 4.3, label, fontName="Times-Bold",
                     fontSize=11, fillColor=txt, textAnchor="middle"))

    def arrow(x1, x2, y, color, label, direction="right"):
        d.add(Line(x1, y, x2, y, strokeColor=color, strokeWidth=1.2))
        if direction == "right":
            tip = x2
            d.add(Polygon([tip, y, tip - 6, y + 3.5, tip - 6, y - 3.5],
                          fillColor=color, strokeColor=color))
        else:
            tip = x1
            d.add(Polygon([tip, y, tip + 6, y + 3.5, tip + 6, y - 3.5],
                          fillColor=color, strokeColor=color))
        d.add(String((x1 + x2) / 2, y + 6.5, label, fontName="Times-Italic",
                     fontSize=9.5, fillColor=color, textAnchor="middle"))

    # forward row
    box(xs[0], y_top, "START", fill=None)
    box(xs[1], y_top, "", fill=None)
    box(xs[2], y_top, "END", fill=TINT)
    my_t = y_top + bh / 2
    arrow(xs[0] + bw, xs[1], my_t, GRAY, "step 1", "right")
    arrow(xs[1] + bw, xs[2], my_t, GRAY, "step 2", "right")
    d.add(String(xs[0], y_top + bh + 9, "Forward — do the steps",
                 fontName="Times-Italic", fontSize=10, fillColor=GRAY,
                 textAnchor="start"))

    # backward row
    box(xs[0], y_bot, "START", fill=TINT, txt=ARC, stroke=ARC)
    box(xs[1], y_bot, "", fill=None, stroke=ARC)
    box(xs[2], y_bot, "END", fill=TINT, txt=ARC, stroke=ARC)
    my_b = y_bot + bh / 2
    arrow(xs[1] + bw, xs[2], my_b, ARC, "undo step 2", "left")
    arrow(xs[0] + bw, xs[1], my_b, ARC, "undo step 1", "left")
    d.add(String(xs[0], y_bot - 13, "Backwards — undo them, last step first",
                 fontName="Times-Italic", fontSize=10, fillColor=ARC,
                 textAnchor="start"))
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


def problem(n, text, space=2.6):
    flow = [Paragraph(f"<b>{n}.</b>&nbsp;&nbsp;{text}", prob),
            Spacer(1, space * inch)]
    return KeepTogether(flow)


story = []

# ---------- PAGE 1 : title, hook, graphic, technique ----------
story.append(Paragraph("Technique Packet No. 2", title))
story.append(Spacer(1, 3))
story.append(Paragraph("Working Backwards — how to read a mind, and other tricks.",
                       subtitle))
story.append(Spacer(1, 8))
story.append(Paragraph("Name: ______________________      "
                       "Date: ______________________", nameline))
story.append(Spacer(1, 10))

hook = ("Here is a trick you can play on a friend. Tell them: think of a secret "
        "number — don’t tell me. Add 6 to it. Now double what you have. What did "
        "you get? They say “20,” and after a moment you announce their secret "
        "number: <b>4</b>. They will be amazed. How did you know?<br/><br/>"
        "You didn’t guess. You walked their steps <b>backwards</b>. They ended "
        "at 20. The last thing they did was double, so undo it — halve 20 to get "
        "10. Before that they added 6, so undo that too — subtract 6 to get 4. "
        "That is their number. The secret behind every “I can read your mind” "
        "number trick is the same: <b>when you know where someone ended up but "
        "not where they began, run the steps in reverse and undo each one.</b>")
story.append(boxed(Paragraph(hook, body), bg=TINT))
story.append(Spacer(1, 10))

story.append(chain_drawing())
story.append(Spacer(1, 2))
story.append(Paragraph(
    "Same chain, two directions: doing the steps runs left to right; "
    "undoing them runs right to left, last step first.", caption))
story.append(Spacer(1, 10))

tool = ("<b>THE TECHNIQUE — Working Backwards.</b><br/>"
        "When a problem tells you the END but not the START:<br/>"
        "&nbsp;&nbsp;<b>1.</b> Write down the steps that were done, in order.<br/>"
        "&nbsp;&nbsp;<b>2.</b> Undo the <b>last</b> step first, using the "
        "opposite operation (undo + with −, × with ÷, and so on).<br/>"
        "&nbsp;&nbsp;<b>3.</b> Keep undoing, one step at a time, until you reach "
        "the start.<br/>"
        "<i>When to reach for it:</i> whenever you know how something finished "
        "but not how it began — “find the number I started with,” a process run "
        "in reverse, an amount before some changes were made. Don’t guess and "
        "check — undo.")
story.append(boxed(Paragraph(tool, body), bg=TOOL_BG))

story.append(PageBreak())

# ---------- PAGE 2 : three worked examples ----------
story.append(Paragraph("Watch how it works", part))
story.append(Spacer(1, 6))

story.append(worked(
    "WORKED EXAMPLE 1",
    "I think of a number, add 6, then double it, and get 20. What was my number?",
    ["The steps, in order: start with the number, add 6, then double.",
     "Undo the last step first. The last step was doubling, so halve: "
     "20 ÷ 2 = 10.",
     "Undo the step before — it was adding 6 — so subtract: 10 − 6 = 4.",
     "So my number was <b>4</b>. (Check forwards: 4 + 6 = 10, doubled is 20. ✓)"]))
story.append(Spacer(1, 11))

story.append(worked(
    "WORKED EXAMPLE 2 — when it doesn’t look like a “start” problem",
    "A candle burns down to half its height every hour. After 3 hours it is "
    "4 cm tall. How tall was it to begin with?",
    ["This is working backwards in disguise: we know the end (4 cm, after "
     "3 hours) and want the start.",
     "Each hour the height was halved, so to undo one hour, double.",
     "Undo hour 3: 4 × 2 = 8. Undo hour 2: 8 × 2 = 16. Undo hour 1: "
     "16 × 2 = 32.",
     "So the candle started at <b>32 cm</b>. (Check: 32 → 16 → 8 → 4. ✓)"]))
story.append(Spacer(1, 11))

story.append(worked(
    "WORKED EXAMPLE 3 — undo in reverse order",
    "A girl gives away half her stickers, then gives away 3 more, and has 5 "
    "left. How many did she start with?",
    ["The steps, in order: start, give away half, then give away 3 more, "
     "leaving 5.",
     "Undo the last step first. The last thing she did was give away 3, so add "
     "them back: 5 + 3 = 8.",
     "Before that she gave away half — so 8 is the half she kept. Undo by "
     "doubling: 8 × 2 = 16.",
     "So she started with <b>16</b>. (Undoing in the wrong order — doubling "
     "first — would give the wrong answer.)"]))

story.append(PageBreak())

# ---------- PAGE 3 : problems 1–3 ----------
story.append(Paragraph("Now you", part))
story.append(Spacer(1, 3))
story.append(Paragraph("Show your undo steps — not just the final number.", note))
story.append(Spacer(1, 8))
story.append(problem(1, "I think of a number, subtract 4, then multiply by 3, "
                        "and get 18. What was my number?", space=2.55))
story.append(problem(2, "A jug of juice: you pour out half of it, then drink 1 "
                        "more cup, and 2 cups are left. How many cups were in "
                        "the jug at the start?", space=2.55))
story.append(problem(3, "A sourdough starter doubles its weight every day. "
                        "After 4 days it weighs 80 grams. How much did it weigh "
                        "at the start?", space=2.55))

story.append(PageBreak())

# ---------- PAGE 4 : problems 4–6 ----------
story.append(problem(4, "I think of a number, add 5, then double it, then "
                        "subtract 4, and get 20. What was my number?", space=2.55))
story.append(problem(5, "A bus has some people on it. At the next stop 4 people "
                        "get off and 7 people get on. Now there are 19 people. "
                        "How many were on the bus before the stop?", space=2.55))
story.append(problem(6, "Maya won a bet that tripled her money. Then she spent "
                        "$8. Now she has $40. How much money did she start with?",
                     space=2.55))

story.append(PageBreak())

# ---------- PAGE 5 : parent key ----------
story.append(Paragraph("Answer Key — for parents", keyhdr))
story.append(Spacer(1, 8))

k_intro = ("<b>What this packet teaches.</b> One named technique — working "
           "backwards — shown first (a mind-reading hook, the chain picture, and "
           "three worked examples), then applied six times. The three worked "
           "examples are deliberately different <i>kinds</i> of the same move: a "
           "plain number-machine (1), a disguised problem that doesn’t announce "
           "itself and undoes the same step three times (2), and one where the "
           "order of undoing matters (3) — so every kind of problem below has "
           "been modeled before they meet it. The lines are written one sentence "
           "each on purpose: they double as models of a written explanation.")
story.append(Paragraph(k_intro, body))
story.append(Spacer(1, 10))

k_ans = ("<b>Answers.</b><br/>"
         "&nbsp;&nbsp;<b>1.</b>&nbsp; Undo last-first: 18 ÷ 3 = 6, then 6 + 4 = "
         "<b>10</b>. (Echoes Worked Example 1.)<br/>"
         "&nbsp;&nbsp;<b>2.</b>&nbsp; Add the cup back: 2 + 1 = 3; that 3 is "
         "half the jug, so double: <b>6 cups</b>. (Echoes Worked Example 3 — "
         "reverse order.)<br/>"
         "&nbsp;&nbsp;<b>3.</b>&nbsp; Doubling four times is undone by halving "
         "four times: 80 → 40 → 20 → 10 → <b>5 grams</b>. (Like Worked Example "
         "2, repeated undo — just doubling instead of halving.)<br/>"
         "&nbsp;&nbsp;<b>4.</b>&nbsp; A longer chain: 20 + 4 = 24, 24 ÷ 2 = 12, "
         "12 − 5 = <b>7</b>.<br/>"
         "&nbsp;&nbsp;<b>5.</b>&nbsp; Nobody says “find the start,” but that’s "
         "the question. Undo last-first: 7 got on, so 19 − 7 = 12; 4 got off, so "
         "12 + 4 = <b>16 people</b>.<br/>"
         "&nbsp;&nbsp;<b>6.</b>&nbsp; Undo last-first: add the $8 back, 40 + 8 = "
         "48; tripling is undone by dividing by 3, 48 ÷ 3 = <b>$16</b>. Adding "
         "the 8 back <i>before</i> dividing is the whole game.")
story.append(Paragraph(k_ans, body))
story.append(Spacer(1, 10))

k_watch = ("<b>What to watch for.</b> Two slips. First, <b>undoing in the wrong "
           "order</b> — on problems 2 and 6, doing the multiply/divide before "
           "the add/subtract gives a wrong answer; point back to Worked Example "
           "3. Second, <b>guess-and-check instead of undoing</b> — it can stumble "
           "onto the answer on problem 1, but it bogs down on 3, 4 and 6, which "
           "is exactly where the technique earns its keep. And a bare number is "
           "not the finished answer here: ask them to show the undo chain, the "
           "way the worked examples do.")
story.append(Paragraph(k_watch, body))
story.append(Spacer(1, 10))

k_run = ("<b>How to run it.</b> Read the hook, the chain picture, and all three "
         "worked examples out loud together before they touch problem 1. The "
         "problems they do solo, in one sitting or two. This is a learning "
         "packet, not a test: helping on a stuck problem is fine, but help by "
         "pointing back at the matching worked example, not at the answer.")
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
