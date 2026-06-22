#!/usr/bin/env python3
"""Be the Judge No. 2 — Judge & Build.
Two judging parts (now-familiar ground, fresh surfaces, one 'always' claim),
then two small Build parts where the kids finish a printed explanation:
last line only, then last two lines. Bridge from recognizing explanations
to producing them.
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
from reportlab.graphics.shapes import Drawing, String, Circle

OUTPUT = "/Users/andresrodriguez/Documents/payday_tests/supplements/be_the_judge_02.pdf"

# ---- page geometry (matches the test playbook) ----
page_w, page_h = letter
left_m = right_m = 0.7 * inch
top_m, bot_m = 0.5 * inch, 0.6 * inch
content_w = page_w - left_m - right_m
content_h = page_h - top_m - bot_m

INK = HexColor("#1a1a1a")
GRAY = HexColor("#666666")
LINE = HexColor("#b8b8b8")
TINT = HexColor("#f4f1ea")     # warm parchment for boxes
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
legend = ParagraphStyle("legend", fontName="Times-Roman", fontSize=12,
                        leading=15.5, textColor=INK)
keyhdr = ParagraphStyle("keyhdr", fontName="Times-Bold", fontSize=15,
                        leading=18, textColor=INK)
expline = ParagraphStyle("expline", fontName="Times-Roman", fontSize=12,
                         leading=16, textColor=INK)


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


def answer_card(letter_, text):
    inner = [
        Paragraph(f"Answer {letter_}", alabel),
        Spacer(1, 2),
        Paragraph(f"“{text}”", answer),
        Spacer(1, 4),
        verdict_row(),
    ]
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


def write_line():
    """One ruled blank line for the kid to write a sentence on."""
    t = Table([[""]], colWidths=[content_w - 0.55 * inch], rowHeights=[0.32 * inch])
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.8, GRAY),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def build_card(lines):
    """The line-by-line explanation box. Each item: (number, text or None).
    None = blank ruled lines for the kid (two ruled lines per blank)."""
    inner = [Paragraph("The explanation — one sentence per line:", alabel),
             Spacer(1, 6)]
    for n, text in lines:
        if text is not None:
            inner.append(Paragraph(f"<b>{n}.</b>&nbsp;&nbsp;{text}", expline))
            inner.append(Spacer(1, 6))
        else:
            num = Paragraph(f"<b>{n}.</b>", expline)
            blanks = [write_line(), Spacer(1, 4), write_line()]
            row = Table([[num, blanks]],
                        colWidths=[0.35 * inch, content_w - 0.35 * inch - 2 * 9])
            row.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]))
            inner.append(row)
            inner.append(Spacer(1, 6))
    return boxed(inner)


story = []

# ---------- PAGE 1 : title + Part 1 (judge) ----------
story.append(Paragraph("Be the Judge — No. 2", title))
story.append(Spacer(1, 3))
story.append(Paragraph("Judge first. Then build one yourself.", subtitle))
story.append(Spacer(1, 8))
story.append(Paragraph("Name: ______________________      "
                       "Date: ______________________", nameline))
story.append(Spacer(1, 8))

leg = ("You know this game. Every answer below is <b>correct</b> — you are "
       "judging the <i>explanations</i>.<br/>"
       "&nbsp;&nbsp;<b>1</b> &nbsp;=&nbsp; Just the answer — no reason.<br/>"
       "&nbsp;&nbsp;<b>2</b> &nbsp;=&nbsp; Gives a reason — but only tries one way.<br/>"
       "&nbsp;&nbsp;<b>3</b> &nbsp;=&nbsp; A real explanation — it works no matter what you try.<br/>"
       "The same score can go to more than one answer.")
story.append(boxed(Paragraph(leg, legend), bg=TINT))
story.append(Spacer(1, 10))

story.append(Paragraph("Part 1 &nbsp;—&nbsp; You be the judge", part))
story.append(Spacer(1, 4))
q1 = ("Three friends pick <b>13 grapes</b>. Can they share them equally — "
      "the same number each, none left over?")
story.append(boxed(Paragraph(q1, qstyle), bg=TINT))
story.append(Spacer(1, 7))

story.append(answer_card(
    "A", "No. Three equal shares means the total is a number you say when "
         "counting by 3s. Counting by 3s goes 12, then 15 — it skips 13. So no "
         "way of sharing can ever come out equal."))
story.append(answer_card(
    "B", "No, they can’t."))
story.append(answer_card(
    "C", "No. I tried it: I gave each friend 4 grapes, one at a time, going "
         "around the circle. That used up 12 grapes, and there was 1 grape left "
         "over with nowhere fair to go. So sharing the 13 grapes equally "
         "doesn’t work."))

story.append(PageBreak())

# ---------- PAGE 2 : Part 2 (judge, an 'always' claim) ----------
story.append(Paragraph("Part 2 &nbsp;—&nbsp; Judge again", part))
story.append(Spacer(1, 4))
story.append(Paragraph("Four answers this time. Same scores: <b>1</b> = just the "
                       "answer, <b>2</b> = a reason but only one try, <b>3</b> = a "
                       "real explanation. Circle one for each.", small))
story.append(Spacer(1, 8))
q2 = ("Tomas says: “If you add 1 to a number, the answer is <b>always</b> bigger "
      "than the number you started with.” Is he right — for <b>every</b> number?")
story.append(boxed(Paragraph(q2, qstyle), bg=TINT))
story.append(Spacer(1, 9))

story.append(answer_card(
    "A", "Yes. I checked: 5 + 1 = 6, and 6 is bigger than 5. So he’s right."))
story.append(answer_card(
    "B", "Yes, Tomas is definitely right. I am completely sure about this — it "
         "always works, every single time, and anyone who has ever added numbers "
         "knows it. It’s just true."))
story.append(answer_card(
    "C", "Yes."))
story.append(answer_card(
    "D", "Yes. Adding 1 means counting up one more step. Whatever number you "
         "start on, you land one step above it — so the answer is always bigger, "
         "no matter which number you pick."))

story.append(PageBreak())

# ---------- PAGE 3 : Parts 3 & 4 (build) ----------
story.append(Paragraph("Part 3 &nbsp;—&nbsp; Build one: finish the last line", part))
story.append(Spacer(1, 4))
story.append(Paragraph("A new game. Here is a question and an explanation that is "
                       "almost finished — every line is <b>one complete sentence</b>. "
                       "The last line is missing. Write it.", small))
story.append(Spacer(1, 8))
q3 = ("Can <b>5 kids</b> split <b>16 marbles</b> equally — the same number each, "
      "none left over?")
story.append(boxed(Paragraph(q3, qstyle), bg=TINT))
story.append(Spacer(1, 8))
story.append(build_card([
    (1, "Equal shares for 5 kids means the total is a number you say when "
        "counting by 5s."),
    (2, "Counting by 5s goes 5, 10, 15, 20 — it skips 16."),
    (3, None),
]))
story.append(Spacer(1, 14))

story.append(Paragraph("Part 4 &nbsp;—&nbsp; Build one: finish the last two lines", part))
story.append(Spacer(1, 4))
story.append(Paragraph("Same game — but now <b>two</b> lines are missing. "
                       "One sentence each.", small))
story.append(Spacer(1, 8))
q4 = ("A ribbon is <b>10 cm</b> long. Maya wants to cut all of it into <b>3 cm</b> "
      "pieces, with nothing left over. Can she?")
story.append(boxed(Paragraph(q4, qstyle), bg=TINT))
story.append(Spacer(1, 8))
story.append(build_card([
    (1, "Every piece uses exactly 3 cm, so the pieces use up 3, 6, 9, 12 … cm "
        "of ribbon."),
    (2, None),
    (3, None),
]))

story.append(PageBreak())

# ---------- PAGE 4 : parent key ----------
story.append(Paragraph("Answer Key — for parents", keyhdr))
story.append(Spacer(1, 8))

k_intro = ("<b>What this sheet does.</b> Two judging rounds on familiar ground, "
           "then the first small step from <i>recognizing</i> a good explanation "
           "to <i>producing</i> one: they finish a printed explanation — last "
           "line only, then last two lines.")
story.append(Paragraph(k_intro, body))
story.append(Spacer(1, 10))

k_scores = ("<b>The scores.</b><br/>"
            "&nbsp;&nbsp;<b>Part 1:</b> A → 3 (counting by 3s skips 13 — rules "
            "out every share at once), B → 1 (no reason), C → 2 (tries one way "
            "of sharing).<br/>"
            "&nbsp;&nbsp;<b>Part 2:</b> A → 2 (checks one number), B → 1 (lots "
            "of words, total confidence, zero reason), C → 1, D → 3 (counting up "
            "one step works for every number).")
story.append(Paragraph(k_scores, body))
story.append(Spacer(1, 10))

k_twist = ("<b>The Part 2 twist.</b> This claim is <i>true</i> — the answer is "
           "yes. That makes “I checked 5 + 1 = 6” extra tempting: the check "
           "works! But one number checked says nothing about every number. A "
           "“yes, always” needs a reason that covers all cases, exactly like a "
           "“no, never” does. If they hesitate over A, ask: does that show it "
           "works for a million too?")
story.append(Paragraph(k_twist, body))
story.append(Spacer(1, 10))

k_build = ("<b>The build parts — what counts.</b> Any sentence in their own "
           "words that lands the conclusion earns it.<br/>"
           "&nbsp;&nbsp;<b>Part 3, line 3:</b> something like “So 16 marbles can "
           "never be split equally among 5 kids.”<br/>"
           "&nbsp;&nbsp;<b>Part 4, line 2:</b> the key step — “That list skips "
           "10: after 9 cm only 1 cm is left, too short for a piece.” "
           "<b>Line 3:</b> “So she can’t cut the whole ribbon into 3 cm pieces.”<br/>"
           "One complete sentence per line, ending with a period — short is "
           "fine, run-ons are the thing to catch.")
story.append(Paragraph(k_build, body))
story.append(Spacer(1, 10))

k_run = ("<b>How to run it.</b> Judging can be out loud as before. Parts 3–4 "
         "they should write themselves — that’s the point of the sheet — but "
         "it’s one sentence at a time, and saying it aloud first before writing "
         "it down is fair play.")
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
