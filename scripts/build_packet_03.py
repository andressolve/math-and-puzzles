#!/usr/bin/env python3
"""Technique Packet No. 3 — The Multiplication Principle.
First packet of the "Art of Counting" (Route C) arc. Named technique = when
you build something by a choice at each stage, multiply the number of choices
at each stage. An array graphic, THREE worked examples spanning the range the
ladder demands (two independent stages / several stages where listing breaks
down / identical repeated slots), then six laddered problems (echo / vary /
hidden), each carrying a "stages" scaffold (boxes joined by x, then = ____) so
the factors must be shown, not just the final number. Parent key in full
sentences.
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

OUTPUT = "/Users/andresrodriguez/Documents/payday_tests/packets/technique_packet_03.pdf"

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
SHADE = HexColor("#dfe6ec")      # filled cells in the array graphic

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
def array_graphic():
    """3 shirts (rows) x 2 shorts (cols) = 6 outfits, as a labelled grid."""
    w, h = content_w, 150
    d = Drawing(w, h)
    cw, ch = 92, 30
    cols = ["black", "tan"]
    rows = ["red", "blue", "green"]
    gx = (w - len(cols) * cw) / 2.0 + 18      # grid left
    gy = 18                                    # grid bottom
    # column headers
    for j, c in enumerate(cols):
        d.add(String(gx + j * cw + cw / 2, gy + len(rows) * ch + 8, c,
                     fontName="Times-Italic", fontSize=10.5, fillColor=GRAY,
                     textAnchor="middle"))
    # cells + row headers (top row drawn last so order is visual top->bottom)
    for i, r in enumerate(rows):
        ry = gy + (len(rows) - 1 - i) * ch
        d.add(String(gx - 8, ry + ch / 2 - 4.2, r, fontName="Times-Italic",
                     fontSize=10.5, fillColor=GRAY, textAnchor="end"))
        for j in range(len(cols)):
            d.add(Rect(gx + j * cw, ry, cw, ch, fillColor=SHADE,
                       strokeColor=INK, strokeWidth=1.0))
    d.add(String(gx + len(cols) * cw + 22, gy + len(rows) * ch / 2 - 5,
                 "3 × 2 = 6", fontName="Times-Bold", fontSize=12,
                 fillColor=INK, textAnchor="start"))
    return d


def stages_scaffold():
    """Boxes joined by x then = ____ : forces the factors to be shown."""
    w, h = content_w, 104
    d = Drawing(w, h)
    d.add(String(0, h - 14, "Count the stages — how many choices at each step:",
                 fontName="Times-Italic", fontSize=10.5, fillColor=GRAY,
                 textAnchor="start"))
    bw, bh, y = 42, 28, 34
    x = 2
    for k in range(4):
        d.add(Rect(x, y, bw, bh, fillColor=None, strokeColor=FAINT,
                   strokeWidth=1.0))
        x += bw
        if k < 3:
            d.add(String(x + 9, y + bh / 2 - 5, "×", fontName="Times-Roman",
                         fontSize=13, fillColor=GRAY, textAnchor="middle"))
            x += 22
    d.add(String(x + 8, y + bh / 2 - 5, "=", fontName="Times-Roman",
                 fontSize=13, fillColor=GRAY, textAnchor="middle"))
    d.add(String(x + 24, y + bh / 2 - 5, "______________",
                 fontName="Times-Roman", fontSize=13, fillColor=FAINT,
                 textAnchor="start"))
    d.add(String(2, 8, "(use only as many boxes as you have stages)",
                 fontName="Times-Italic", fontSize=9.5, fillColor=GRAY,
                 textAnchor="start"))
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
            Spacer(1, 4), stages_scaffold(), Spacer(1, 0.95 * inch)]
    return KeepTogether(flow)


story = []

# ---------- PAGE 1 : title, hook, graphic, technique ----------
story.append(Paragraph("Technique Packet No. 3", title))
story.append(Spacer(1, 3))
story.append(Paragraph("The Multiplication Principle — how to count without "
                       "counting.", subtitle))
story.append(Spacer(1, 8))
story.append(Paragraph("Name: ______________________      "
                       "Date: ______________________", nameline))
story.append(Spacer(1, 10))

hook = ("Sam is getting dressed. He has 3 clean shirts — red, blue, green — and "
        "2 pairs of shorts — black and tan. How many different outfits can he "
        "put together?<br/><br/>"
        "You could try to list them all and hope you don’t miss any. Or you "
        "could notice something. For each of his 3 shirts, he has 2 choices of "
        "shorts — so the outfits come in 3 groups of 2. That is 3 × 2 = 6, and "
        "you didn’t have to list a single one. This is the whole trick: <b>when "
        "you build something by making a choice at each stage, you don’t count "
        "the results one by one — you multiply the number of choices at each "
        "stage.</b>")
story.append(boxed(Paragraph(hook, body), bg=TINT))
story.append(Spacer(1, 8))

story.append(array_graphic())
story.append(Spacer(1, 2))
story.append(Paragraph(
    "Every shirt (a row) can meet every pair of shorts (a column). "
    "3 rows × 2 columns = 6 boxes — six outfits.", caption))
story.append(Spacer(1, 8))

tool = ("<b>THE TECHNIQUE — The Multiplication Principle.</b><br/>"
        "When you build something by making a choice at each stage:<br/>"
        "&nbsp;&nbsp;<b>1.</b> Break the job into stages — first this, then "
        "this, then this.<br/>"
        "&nbsp;&nbsp;<b>2.</b> Count how many choices you have at each stage.<br/>"
        "&nbsp;&nbsp;<b>3.</b> Multiply those numbers together. That product is "
        "the total.<br/>"
        "<i>When to reach for it:</i> any “how many different ___ can you make, "
        "arrange, or choose” question that you build step by step — outfits, "
        "meals, codes, license plates, routes. Don’t list them all — multiply.")
story.append(boxed(Paragraph(tool, body), bg=TOOL_BG))

story.append(PageBreak())

# ---------- PAGE 2 : worked examples 1 & 2 ----------
story.append(Paragraph("Watch how it works", part))
story.append(Spacer(1, 6))

story.append(worked(
    "WORKED EXAMPLE 1",
    "Sam has 3 shirts and 2 pairs of shorts. How many different outfits can he "
    "make?",
    ["There are two stages: first pick a shirt, then pick a pair of shorts.",
     "Stage 1 — the shirt — has 3 choices. Stage 2 — the shorts — has 2 "
     "choices.",
     "Multiply the stages: 3 × 2 = <b>6 outfits</b>.",
     "(The grid above shows all six. Notice you never had to list them to know "
     "there were six.)"]))
story.append(Spacer(1, 11))

story.append(worked(
    "WORKED EXAMPLE 2 — more stages, where listing would be painful",
    "A kids’ menu lets you pick 1 of 4 main dishes, then 1 of 3 drinks, then "
    "1 of 2 desserts. How many different meals are possible?",
    ["Three stages this time: main, then drink, then dessert.",
     "Count the choices at each: 4 mains, 3 drinks, 2 desserts.",
     "Multiply all three stages: 4 × 3 × 2 = <b>24 meals</b>.",
     "Listing all 24 would fill the page; multiplying the stages takes one "
     "line. That is exactly when this technique earns its keep."]))

story.append(PageBreak())

# ---------- PAGE 3 : worked example 3 ----------
story.append(Paragraph("Watch how it works (one more)", part))
story.append(Spacer(1, 6))

story.append(worked(
    "WORKED EXAMPLE 3 — when every stage has the same choices",
    "A treasure chest opens with a 3-symbol code. Each symbol can be any one of "
    "5 shapes, and shapes may repeat. How many different codes are there?",
    ["Three stages: the first symbol, the second symbol, the third symbol.",
     "Each stage has the same 5 choices — and because shapes may repeat, "
     "picking one does not use it up. The choices don’t run out.",
     "So every stage still has 5 choices: 5 × 5 × 5 = <b>125 codes</b>.",
     "Watch for that word “repeat.” If shapes could <i>not</i> repeat, the "
     "stages would shrink to 5 × 4 × 3 — but here they don’t."]))
story.append(Spacer(1, 14))
story.append(Paragraph(
    "All three are the same move: split the job into stages, count the choices "
    "at each stage, and multiply.", note))

story.append(PageBreak())

# ---------- PAGE 4 : problems 1–3 ----------
story.append(Paragraph("Now you", part))
story.append(Spacer(1, 3))
story.append(Paragraph("Show the stages and the multiplication — not just the "
                       "final number.", note))
story.append(Spacer(1, 8))
story.append(problem(1, "An ice-cream stand has 4 flavors and 3 kinds of cone. "
                        "How many different single-scoop cones can you order?"))
story.append(problem(2, "For breakfast you choose 1 of 3 cereals, then 1 of 2 "
                        "fruits, then 1 of 3 juices. How many different "
                        "breakfasts are possible?"))
story.append(problem(3, "A 3-digit code uses the digits 1, 2, 3, 4, 5, and "
                        "digits may repeat. How many different codes are there?"))

story.append(PageBreak())

# ---------- PAGE 5 : problems 4–6 ----------
story.append(problem(4, "At a sandwich shop you pick 1 of 3 breads, 1 of 4 "
                        "fillings, 1 of 2 sauces, and then decide toasted or not "
                        "toasted. How many different sandwiches are possible?"))
story.append(problem(5, "To get to school, Mia first walks to the park by one "
                        "of 2 paths, then walks from the park to school by one "
                        "of 3 paths. How many different ways can she get to "
                        "school?"))
story.append(problem(6, "How many two-digit numbers have an even tens digit and "
                        "an odd ones digit? (Think of choosing the tens digit, "
                        "then the ones digit.)"))

story.append(PageBreak())

# ---------- PAGE 6 : parent key ----------
story.append(Paragraph("Answer Key — for parents", keyhdr))
story.append(Spacer(1, 8))

k_intro = ("<b>What this packet teaches.</b> One named technique — when you "
           "build something by a choice at each stage, multiply the number of "
           "choices at each stage — shown first (the outfit hook, the grid "
           "picture, and three worked examples), then applied six times. The "
           "three worked examples are deliberately different <i>kinds</i> of the "
           "same move: two independent stages (1), several stages where listing "
           "would be hopeless (2), and stages that all share the same choices "
           "with repeats allowed (3) — so every kind of problem below has been "
           "modeled before they meet it. Each problem has a “stages” box printed "
           "under it: the goal is to see the factors, not just the total.")
story.append(Paragraph(k_intro, body))
story.append(Spacer(1, 10))

k_ans = ("<b>Answers.</b><br/>"
         "&nbsp;&nbsp;<b>1.</b>&nbsp; Two stages: 4 flavors × 3 cones = "
         "<b>12</b>. (Echoes Worked Example 1.)<br/>"
         "&nbsp;&nbsp;<b>2.</b>&nbsp; Three stages: 3 × 2 × 3 = <b>18</b>. "
         "(Echoes Worked Example 2.)<br/>"
         "&nbsp;&nbsp;<b>3.</b>&nbsp; Each of the 3 digits has 5 choices and "
         "they may repeat: 5 × 5 × 5 = <b>125</b>. (Echoes Worked Example 3 — "
         "watch they don’t shrink it to 5 × 4 × 3.)<br/>"
         "&nbsp;&nbsp;<b>4.</b>&nbsp; Four stages, and “toasted or not” is just "
         "a stage with 2 choices: 3 × 4 × 2 × 2 = <b>48</b>.<br/>"
         "&nbsp;&nbsp;<b>5.</b>&nbsp; It doesn’t say “how many ways,” but it is "
         "the same idea: 2 paths to the park, then 3 to school, 2 × 3 = "
         "<b>6 ways</b>.<br/>"
         "&nbsp;&nbsp;<b>6.</b>&nbsp; Choosing a two-digit number is two stages. "
         "The tens digit must be even <i>and</i> can’t be 0 (or it wouldn’t be a "
         "two-digit number), so it is 2, 4, 6, 8 — 4 choices. The ones digit is "
         "odd: 1, 3, 5, 7, 9 — 5 choices. So 4 × 5 = <b>20</b>.")
story.append(Paragraph(k_ans, body))
story.append(Spacer(1, 10))

k_watch = ("<b>What to watch for.</b> Three slips. First, <b>adding instead of "
           "multiplying</b> (“4 and 3, that’s 7”) — point back to the grid: each "
           "of the 4 flavors pairs with <i>all</i> 3 cones, so it’s 4 groups of "
           "3. Second, <b>shrinking the choices when they shouldn’t</b> — on "
           "problem 3 the digits repeat, so every stage stays at 5; only drop "
           "the count when a thing gets used up. Third, the old habit of writing "
           "just the final number: the “stages” box is there to be filled — ask "
           "to see the factors and the × signs, the way the worked examples show "
           "them. Problems 5 and 6 are the stretch: 5 hides the stages inside a "
           "journey, and 6 hides a sneaky restriction (the tens digit can’t be "
           "0) inside an ordinary-looking question.")
story.append(Paragraph(k_watch, body))
story.append(Spacer(1, 10))

k_run = ("<b>How to run it.</b> Read the hook, the grid picture, and all three "
         "worked examples out loud together before they touch problem 1. The "
         "problems they do solo, in one sitting or two. This is a learning "
         "packet, not a test: helping on a stuck problem is fine, but help by "
         "pointing back at the matching worked example — and at the stages box — "
         "not at the answer.")
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
