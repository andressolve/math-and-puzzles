#!/usr/bin/env python3
"""Be the Judge No. 3 — retry of the Judge & Build bridge after #2 stumbled.
Fix: model -> echo -> vary. The Judge voice works a skip-counting question
first (#2 had no model and the structure switch from parity broke transfer),
the kids echo on a near-identical one, then vary. The build mechanic likewise
gets a fully worked model before they finish a twin.
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

OUTPUT = "/Users/andresrodriguez/Documents/payday_tests/supplements/be_the_judge_03.pdf"

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
note = ParagraphStyle("note", fontName="Times-Italic", fontSize=11,
                      leading=14.5, textColor=HexColor("#3a4a5a"))
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


def write_line(width):
    t = Table([[""]], colWidths=[width], rowHeights=[0.3 * inch])
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.8, GRAY),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def build_card(lines, header="The explanation — one sentence per line:"):
    """Each item: (number, text[, starter]). text=None means ruled blank(s);
    a starter is printed inline at the start of the first ruled line."""
    from reportlab.pdfbase.pdfmetrics import stringWidth
    inner = [Paragraph(header, alabel), Spacer(1, 6)]
    inner_w = content_w - 2 * 9
    for item in lines:
        n, text = item[0], item[1]
        starter = item[2] if len(item) > 2 else None
        if text is not None:
            inner.append(Paragraph(f"<b>{n}.</b>&nbsp;&nbsp;{text}", expline))
            inner.append(Spacer(1, 6))
        else:
            if starter:
                lead = f"<b>{n}.</b>&nbsp;&nbsp;<i>{starter}</i>"
                lead_w = (0.32 * inch + 8
                          + stringWidth(starter, "Times-Italic", 12))
                blanks = [write_line(inner_w - lead_w)]
            else:
                lead = f"<b>{n}.</b>"
                lead_w = 0.32 * inch
                blanks = [write_line(inner_w - lead_w), Spacer(1, 4),
                          write_line(inner_w - lead_w)]
            row = Table([[Paragraph(lead, expline), blanks]],
                        colWidths=[lead_w, inner_w - lead_w])
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

# ---------- PAGE 1 : title + Part 1 (judge MODEL) ----------
story.append(Paragraph("Be the Judge — No. 3", title))
story.append(Spacer(1, 3))
story.append(Paragraph("Watch first. Then judge. Then build.", subtitle))
story.append(Spacer(1, 8))
story.append(Paragraph("Name: ______________________      "
                       "Date: ______________________", nameline))
story.append(Spacer(1, 8))

leg = ("Same scores as always — every answer is <b>correct</b>; you judge the "
       "<i>explanations</i>.<br/>"
       "&nbsp;&nbsp;<b>1</b> &nbsp;=&nbsp; Just the answer — no reason.<br/>"
       "&nbsp;&nbsp;<b>2</b> &nbsp;=&nbsp; Gives a reason — but only tries one way.<br/>"
       "&nbsp;&nbsp;<b>3</b> &nbsp;=&nbsp; A real explanation — it works no matter what you try.")
story.append(boxed(Paragraph(leg, legend), bg=TINT))
story.append(Spacer(1, 10))

story.append(Paragraph("Part 1 &nbsp;—&nbsp; Watch the judge at work", part))
story.append(Spacer(1, 4))
q1 = ("Four friends share <b>14 cookies</b> — the same number each, none left "
      "over. Can they?")
story.append(boxed(Paragraph(q1, qstyle), bg=TINT))
story.append(Spacer(1, 7))

story.append(answer_card(
    "A", "No.",
    marked=1,
    judge="True — but no reason. Not an explanation yet."))
story.append(answer_card(
    "B", "No. I tried 3 cookies each — that uses 12, and 2 are left over. So it "
         "doesn’t work.",
    marked=2,
    judge=("A real reason — but only <i>one</i> try. Maybe a different share "
           "works? Showing one try fail doesn’t show every try must fail.")))
story.append(answer_card(
    "C", "No. Four equal shares means the total is a number you say when "
         "counting by 4s. Counting by 4s goes 12, then 16 — it skips 14. So no "
         "way of sharing can ever work.",
    marked=3,
    judge=("The winner. It never tries a single share — the counting-by-4s list "
           "skips 14, and that rules out <i>every</i> try at once. Nothing could "
           "talk you out of it.")))

story.append(PageBreak())

# ---------- PAGE 2 : Part 2 (echo) + Part 3 (vary) ----------
story.append(Paragraph("Part 2 &nbsp;—&nbsp; Your turn — just like that one", part))
story.append(Spacer(1, 4))
story.append(Paragraph("Circle a score for each. The same score can go to more "
                       "than one answer.", small))
story.append(Spacer(1, 8))
q2 = ("Three kids share <b>16 crayons</b> — the same number each, none left "
      "over. Can they?")
story.append(boxed(Paragraph(q2, qstyle), bg=TINT))
story.append(Spacer(1, 9))

story.append(answer_card(
    "A", "No. I tried it out: I dealt 5 crayons to each kid, one at a time, and "
         "that used up 15 of them, so there was 1 crayon left over with no fair "
         "place to go. So it doesn’t work."))
story.append(answer_card(
    "B", "No, they can’t."))
story.append(answer_card(
    "C", "No. Three equal shares means the total is on the counting-by-3s list. "
         "That list goes 15, then 18 — it skips 16. So no share can ever come "
         "out equal."))

story.append(PageBreak())

story.append(Paragraph("Part 3 &nbsp;—&nbsp; Judge once more — bigger numbers", part))
story.append(Spacer(1, 4))
q3 = ("Seven kids share <b>30 candies</b> — the same number each, none left "
      "over. Can they?")
story.append(boxed(Paragraph(q3, qstyle), bg=TINT))
story.append(Spacer(1, 9))

story.append(answer_card(
    "A", "No. I gave each kid 4 candies — that’s 28, with 2 left over. So it "
         "doesn’t work."))
story.append(answer_card(
    "B", "No, and I’m completely sure about it. I thought about this one really "
         "carefully, for a long time, and there is just no possible way it could "
         "ever happen, trust me."))
story.append(answer_card(
    "C", "No. Seven equal shares means the total is on the counting-by-7s list, "
         "and that list goes 28, then 35 — it skips 30."))
story.append(answer_card("D", "No."))

story.append(PageBreak())

# ---------- PAGE 3 : builds — model, echo, echo with starters ----------
story.append(Paragraph("Part 4 &nbsp;—&nbsp; Watch one get built", part))
story.append(Spacer(1, 4))
story.append(Paragraph("Here is a whole explanation, built line by line. Every "
                       "line is <b>one complete sentence</b>, and the last line "
                       "always starts with <b>So</b> and answers the question.", small))
story.append(Spacer(1, 8))
q4 = ("Can <b>4 kids</b> share <b>13 marbles</b> equally — the same number "
      "each, none left over?")
story.append(boxed(Paragraph(q4, qstyle), bg=TINT))
story.append(Spacer(1, 8))
story.append(build_card([
    (1, "Equal shares for 4 kids means the total is on the counting-by-4s list."),
    (2, "Counting by 4s goes 12, then 16 — it skips 13."),
    (3, "So 13 marbles can never be shared equally by 4 kids."),
]))
story.append(Spacer(1, 10))

story.append(Paragraph("Part 5 &nbsp;—&nbsp; Your turn — write the last line", part))
story.append(Spacer(1, 4))
story.append(Paragraph("Same kind of question, same kind of explanation. Lines 1 "
                       "and 2 are done. Write line 3 — one sentence, starting "
                       "with <b>So</b>.", small))
story.append(Spacer(1, 8))
q5 = ("Can <b>6 kids</b> share <b>20 stickers</b> equally — the same number "
      "each, none left over?")
story.append(boxed(Paragraph(q5, qstyle), bg=TINT))
story.append(Spacer(1, 8))
story.append(build_card([
    (1, "Equal shares for 6 kids means the total is on the counting-by-6s list."),
    (2, "Counting by 6s goes 18, then 24 — it skips 20."),
    (3, None),
]))
story.append(Spacer(1, 10))

q6 = ("Can <b>5 kids</b> share <b>22 apples</b> equally — the same number "
      "each, none left over?")
story.append(KeepTogether([
    Paragraph("Part 6 &nbsp;—&nbsp; One more — two lines, with a head start", part),
    Spacer(1, 4),
    Paragraph("Line 1 is done. Lines 2 and 3 are started for you — "
              "finish each one. One sentence per line.", small),
    Spacer(1, 8),
    boxed(Paragraph(q6, qstyle), bg=TINT),
    Spacer(1, 8),
    build_card([
        (1, "Equal shares for 5 kids means the total is on the counting-by-5s list."),
        (2, None, "Counting by 5s goes …"),
        (3, None, "So …"),
    ]),
]))

story.append(PageBreak())

# ---------- PAGE 4 : parent key ----------
story.append(Paragraph("Answer Key — for parents", keyhdr))
story.append(Spacer(1, 8))

k_intro = ("<b>What changed since sheet No. 2.</b> That one stumbled because it "
           "skipped the model: it asked them to judge a new kind of reason "
           "(skip-counting instead of odd/even) and to build sentences — both "
           "without ever seeing one done. This sheet fixes the step size: watch "
           "the judge work one (Part 1), do a near-twin (Part 2), then vary "
           "(Part 3). Same for building: a finished explanation to read "
           "(Part 4), a twin needing only its last line (Part 5), then two "
           "lines with head-start words (Part 6).")
story.append(Paragraph(k_intro, body))
story.append(Spacer(1, 10))

k_scores = ("<b>The scores.</b> Part 1 is worked on the sheet (A → 1, B → 2, "
            "C → 3).<br/>"
            "&nbsp;&nbsp;<b>Part 2:</b> A → 2 (deals one share and stops — "
            "longest answer, but length isn’t reasoning), B → 1, C → 3 (the "
            "counting-by-3s list skips 16 — rules out every share).<br/>"
            "&nbsp;&nbsp;<b>Part 3:</b> A → 2, B → 1 (very sure, zero reason), "
            "C → 3, D → 1.")
story.append(Paragraph(k_scores, body))
story.append(Spacer(1, 10))

k_build = ("<b>The build parts — what counts.</b> Their own words, one sentence, "
           "a period at the end.<br/>"
           "&nbsp;&nbsp;<b>Part 5, line 3:</b> anything like “So 20 stickers can "
           "never be shared equally by 6 kids.”<br/>"
           "&nbsp;&nbsp;<b>Part 6, line 2:</b> “Counting by 5s goes 20, then 25 "
           "— it skips 22.” <b>Line 3:</b> “So 22 apples can’t be shared equally "
           "by 5 kids.”<br/>"
           "If a line comes out as a run-on, have them read it aloud and find "
           "where the breath goes — that’s where the period goes.")
story.append(Paragraph(k_build, body))
story.append(Spacer(1, 10))

k_run = ("<b>How to run it.</b> Part 1 and Part 4 are for reading <i>together, "
         "out loud</i> — they are the lesson; don’t skip past them to the "
         "scoring. The rest they do solo. Saying a build line aloud before "
         "writing it is fair play.")
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
