#!/usr/bin/env python3
"""Be the Judge — sheet 1 of the explanation-writing thread.
Kids judge three answers to the same easy question (all correct) and
score how well each one *explains*. Part 1 is a worked model; Part 2 is theirs.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
    Table, TableStyle, PageBreak, KeepTogether,
)
from reportlab.graphics.shapes import Drawing, String, Circle

OUTPUT = "/Users/andresrodriguez/Documents/payday_tests/supplements/be_the_judge_01.pdf"

# ---- page geometry (matches the test playbook) ----
page_w, page_h = letter
left_m = right_m = 0.7 * inch
top_m, bot_m = 0.5 * inch, 0.6 * inch
content_w = page_w - left_m - right_m
content_h = page_h - top_m - bot_m

INK = HexColor("#1a1a1a")
GRAY = HexColor("#666666")
LINE = HexColor("#b8b8b8")
TINT = HexColor("#f4f1ea")   # warm parchment for boxes
NOTE_BG = HexColor("#eef1f4")  # cool tint for the judge's voice

# ---- styles ----
title = ParagraphStyle("title", fontName="Times-Bold", fontSize=22,
                       leading=25, textColor=INK, alignment=TA_CENTER)
subtitle = ParagraphStyle("subtitle", fontName="Times-Italic", fontSize=12.5,
                          leading=16, textColor=GRAY, alignment=TA_CENTER)
nameline = ParagraphStyle("nameline", fontName="Times-Roman", fontSize=11,
                          leading=16, textColor=INK)
body = ParagraphStyle("body", fontName="Times-Roman", fontSize=12,
                      leading=15, textColor=INK)
bodyc = ParagraphStyle("bodyc", parent=body, alignment=TA_CENTER)
part = ParagraphStyle("part", fontName="Times-Bold", fontSize=14.5,
                      leading=18, textColor=INK, spaceBefore=2, spaceAfter=2)
qstyle = ParagraphStyle("qstyle", fontName="Times-Bold", fontSize=12.5,
                        leading=16, textColor=INK)
alabel = ParagraphStyle("alabel", fontName="Times-Bold", fontSize=11.5,
                        leading=14, textColor=GRAY)
answer = ParagraphStyle("answer", fontName="Times-Roman", fontSize=12,
                        leading=14.5, textColor=INK)
small = ParagraphStyle("small", fontName="Times-Roman", fontSize=10.5,
                       leading=13, textColor=GRAY)
note = ParagraphStyle("note", fontName="Times-Italic", fontSize=11,
                      leading=14.5, textColor=HexColor("#3a4a5a"))
legend = ParagraphStyle("legend", fontName="Times-Roman", fontSize=12,
                        leading=15.5, textColor=INK)
keyhdr = ParagraphStyle("keyhdr", fontName="Times-Bold", fontSize=15,
                        leading=18, textColor=INK)


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


def score_strip(marked=None):
    """A '1  2  3' row; if marked, draw a ring around that digit."""
    d = Drawing(120, 24)
    xs = {1: 16, 2: 60, 3: 104}
    for n, x in xs.items():
        if marked == n:
            d.add(Circle(x, 11, 12, strokeColor=INK, strokeWidth=1.6,
                         fillColor=None))
        d.add(String(x, 6, str(n), fontName="Times-Bold", fontSize=15,
                     fillColor=INK, textAnchor="middle"))
    return d


def verdict_row(marked=None):
    label = Paragraph("Score it (circle one):", small)
    row = Table([[label, score_strip(marked)]],
                colWidths=[1.7 * inch, 2.0 * inch])
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return row


def answer_card(letter_, text, marked=None, judge=None):
    inner = [
        Paragraph(f"Answer {letter_}", alabel),
        Spacer(1, 2),
        Paragraph(f"“{text}”", answer),
        Spacer(1, 4),
        verdict_row(marked),
    ]
    if judge:
        inner.append(Spacer(1, 4))
        jt = Table([[Paragraph(f"<b>Judge:</b> {judge}", note)]],
                   colWidths=[content_w - 2 * 9 - 14])
        jt.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), NOTE_BG),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        inner.append(jt)
    card = Table([[inner]], colWidths=[content_w])
    card.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.8, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return KeepTogether([card, Spacer(1, 7)])


story = []

# ---------- PAGE 1 : title + model ----------
story.append(Paragraph("Be the Judge", title))
story.append(Spacer(1, 3))
story.append(Paragraph("Judging explanations — not answers.", subtitle))
story.append(Spacer(1, 8))
story.append(Paragraph("Name: ______________________      "
                       "Date: ______________________", nameline))
story.append(Spacer(1, 8))

intro = ("A right answer and a good explanation are not the same thing. "
         "Below, three people answer the same question. <b>All three get the "
         "right answer</b> — so you can’t judge them on that. You have to "
         "judge something harder: how well each one explains <i>why</i>.")
leg = ("<b>Give each answer a score from 1 to 3:</b><br/>"
       "&nbsp;&nbsp;<b>1</b> &nbsp;=&nbsp; Just the answer — no reason.<br/>"
       "&nbsp;&nbsp;<b>2</b> &nbsp;=&nbsp; Gives a reason — but only tries one way.<br/>"
       "&nbsp;&nbsp;<b>3</b> &nbsp;=&nbsp; A real explanation — it works no matter what you try.")
story.append(boxed([Paragraph(intro, body), Spacer(1, 6),
                    Paragraph(leg, legend)], bg=TINT))
story.append(Spacer(1, 10))

story.append(Paragraph("Part 1 &nbsp;—&nbsp; Watch a judge at work", part))
story.append(Spacer(1, 4))
q1 = ("Maya has <b>7 socks</b>. Can she split them into two equal piles — "
      "the same number in each?")
story.append(boxed(Paragraph(q1, qstyle), bg=TINT))
story.append(Spacer(1, 7))

story.append(answer_card(
    "A", "No.",
    marked=1,
    judge=("True — but it tells us nothing. <i>How</i> does she know? "
           "An answer with no reason isn’t an explanation yet.")))
story.append(answer_card(
    "B", "No. I tried 3 in one pile and 4 in the other, and they weren’t equal.",
    marked=2,
    judge=("Better — it gives a real reason. But she only tried <i>one</i> way. "
           "Maybe a different split works? This shows one try failing; it doesn’t "
           "show that <i>every</i> try must fail.")))
story.append(answer_card(
    "C", "No. If the two piles were equal, each would hold the same number — so "
         "the total would be that number doubled, and a doubled number is always "
         "even. But 7 is odd. So equal piles are impossible — there’s no split to try.",
    marked=3,
    judge=("This one wins. Notice it never tries a single split — it shows that "
           "two equal piles would <i>always</i> need an even total, and 7 is odd. "
           "That rules out every way at once. Read it, and no one could talk you "
           "out of it.")))

story.append(PageBreak())

# ---------- PAGE 2 : their turn ----------
story.append(Paragraph("Part 2 &nbsp;—&nbsp; Now you be the judge", part))
story.append(Spacer(1, 4))
story.append(Paragraph("Same scores: <b>1</b> = just the answer, "
                       "<b>2</b> = a reason but only one try, "
                       "<b>3</b> = a real explanation. Circle one for each.", small))
story.append(Spacer(1, 8))
q2 = ("Sam has <b>9 stickers</b>. Can he give the same number to each of his "
      "2 cousins, with none left over?")
story.append(boxed(Paragraph(q2, qstyle), bg=TINT))
story.append(Spacer(1, 9))

story.append(answer_card(
    "A", "No. I gave 4 to one cousin and 5 to the other, and that’s not the same."))
story.append(answer_card(
    "B", "No. If both cousins ended up with the same number, the total would be "
         "that number doubled — always an even number. But 9 is odd. So it can "
         "never split into two equal shares."))
story.append(answer_card("C", "No."))

story.append(PageBreak())

# ---------- PAGE 3 : their turn, fresh surface ----------
story.append(Paragraph("Part 3 &nbsp;—&nbsp; You be the judge again", part))
story.append(Spacer(1, 4))
story.append(Paragraph("A brand-new question — and <b>four</b> answers this time. "
                       "Score each one <b>1</b>, <b>2</b>, or <b>3</b> — the same "
                       "score can go to more than one answer.", small))
story.append(Spacer(1, 8))
q3 = ("When you add two numbers — <b>any</b> two numbers — does the order ever "
      "change the total?")
story.append(boxed(Paragraph(q3, qstyle), bg=TINT))
story.append(Spacer(1, 9))

story.append(answer_card(
    "A", "No. I’m completely sure, because I’ve added tons of numbers before and "
         "I thought about it very carefully, and swapping them around just doesn’t "
         "do anything that could ever make the total come out different."))
story.append(answer_card(
    "B", "No. Adding means putting two groups together into one pile, and the "
         "pile is the same size whichever group you start with. So the order "
         "can never change the total, for any two numbers."))
story.append(answer_card(
    "C", "No. I checked 6 + 9 = 15 and 9 + 6 = 15 — same answer both times."))
story.append(answer_card("D", "No."))

story.append(PageBreak())

# ---------- PAGE 4 : parent key ----------
story.append(Paragraph("Answer Key — for parents", keyhdr))
story.append(Spacer(1, 8))

k_intro = ("<b>What this sheet teaches.</b> The difference between getting the "
           "right answer and explaining it. Every answer here is correct — the "
           "whole exercise is judging the <i>explanations</i>, so the boys have to "
           "look at reasoning instead of results.")
story.append(Paragraph(k_intro, body))
story.append(Spacer(1, 10))

k_scores = ("<b>The scores.</b> Part 1 is worked on the sheet (A → 1, B → 2, "
            "C → 3). From Part 2 on the order is <i>shuffled</i> — if they score "
            "by length or position instead of reading, it will show immediately.<br/>"
            "&nbsp;&nbsp;<b>Part 2:</b> A → 2 (tries one split), B → 3 (the real "
            "explanation: equal shares need an even total, 9 is odd), C → 1 (no "
            "reason).<br/>"
            "&nbsp;&nbsp;<b>Part 3:</b> A → 1, B → 3 (adding is combining two "
            "groups — same pile either way), C → 2 (checks one example), D → 1. "
            "Yes, A gets a 1 despite all those words: it never gives a reason, it "
            "just repeats the answer with confidence.")
story.append(Paragraph(k_scores, body))
story.append(Spacer(1, 10))

k_b = ("<b>Two to dwell on.</b> The one-example answers (Part 2 A, Part 3 C) are "
       "the mistake from the last test — showing that one particular attempt "
       "fails and thinking that settles it. A real explanation has to rule out "
       "<i>every</i> attempt, not just one. And Part 3 A is the other trap: lots "
       "of words, total confidence, zero reason. Sounding sure isn’t explaining.")
story.append(Paragraph(k_b, body))
story.append(Spacer(1, 10))

k_last = ("<b>What you’re listening for.</b> When they say why the winner wins, "
          "you want some version of “it gives a reason that covers every case, "
          "not just one try.” If they say that — in any words — they’ve got it.")
story.append(Paragraph(k_last, body))
story.append(Spacer(1, 10))

k_run = ("<b>How to run it.</b> However you like — out loud together, or on paper. "
         "If writing is a slog, let them <i>say</i> the verdicts and you scribe; the "
         "judging is the point, not the handwriting.")
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
