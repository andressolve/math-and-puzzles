#!/usr/bin/env python3
"""Saturday Test No. 7 — parity ('odd & even, the hidden tool') thread."""

from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, FrameBreak,
    Paragraph, Spacer,  Table, TableStyle, PageBreak,
)
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import HexColor, black

OUTPUT = "/Users/andresrodriguez/Documents/payday_tests/tests/math_logic_test_07.pdf"

page_w, page_h = letter
left_m = right_m = 0.7 * inch
top_m, bot_m = 0.5 * inch, 0.6 * inch
content_w = page_w - left_m - right_m
content_h = page_h - top_m - bot_m
half_h = content_h / 2

# ---- frames / templates --------------------------------------------------
top_frame = Frame(left_m, bot_m + half_h, content_w, half_h,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
bottom_frame = Frame(left_m, bot_m, content_w, half_h,
                     leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
two_frame_tpl = PageTemplate(id='two', frames=[top_frame, bottom_frame])

single_frame = Frame(left_m, bot_m, content_w, content_h,
                     leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
single_tpl = PageTemplate(id='single', frames=[single_frame])

doc = BaseDocTemplate(OUTPUT, pagesize=letter,
                      leftMargin=left_m, rightMargin=right_m,
                      topMargin=top_m, bottomMargin=bot_m,
                      pageTemplates=[two_frame_tpl, single_tpl])

# ---- styles --------------------------------------------------------------
title_style = ParagraphStyle('title', fontName='Times-Bold', fontSize=22,
                             leading=26, spaceAfter=4, alignment=TA_LEFT)
subtitle_style = ParagraphStyle('subtitle', fontName='Times-Italic', fontSize=12,
                                leading=15, textColor=HexColor('#444444'),
                                spaceAfter=10)
section_style = ParagraphStyle('section', fontName='Times-Bold', fontSize=13.5,
                               leading=17, spaceBefore=2, spaceAfter=9,
                               textColor=HexColor('#222222'))
prob_style = ParagraphStyle('prob', fontName='Times-Roman', fontSize=12.5,
                            leading=16.5, spaceAfter=0)
header_cell = ParagraphStyle('hcell', fontName='Times-Roman', fontSize=11,
                             leading=14, textColor=HexColor('#333333'))
ak_head_style = ParagraphStyle('akhead', fontName='Times-Bold', fontSize=15,
                               leading=19, spaceAfter=12)
ak_item_style = ParagraphStyle('akitem', fontName='Times-Roman', fontSize=11,
                               leading=15, spaceAfter=9)


def work_space(n):
    return Spacer(1, 0.22 * inch * n)


def problem(num, text, lines):
    return [Paragraph(f"<b>{num}.</b>&nbsp;&nbsp;{text}", prob_style), work_space(lines)]


def header_table():
    cells = [[Paragraph("Name: ___________________", header_cell),
              Paragraph("Date: _____________", header_cell),
              Paragraph("Time: 15 min", header_cell)]]
    t = Table(cells, colWidths=[content_w * 0.45, content_w * 0.33, content_w * 0.22])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
    ]))
    return t


# ---- problem text --------------------------------------------------------
A1 = ("Work these out, then look at your answers.<br/>"
      "&nbsp;&nbsp;&nbsp;&nbsp;odd + odd:&nbsp;&nbsp;&nbsp;5 + 7 = _____&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3 + 9 = _____<br/>"
      "&nbsp;&nbsp;&nbsp;&nbsp;even + even:&nbsp;&nbsp;4 + 8 = _____&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6 + 2 = _____<br/>"
      "&nbsp;&nbsp;&nbsp;&nbsp;odd + even:&nbsp;&nbsp;5 + 4 = _____&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;7 + 6 = _____<br/>"
      "When do you get an <i>odd</i> answer? When do you get an <i>even</i> one?")

A2 = ("Two whole numbers add up to 15. Can both of them be even? "
      "Can both of them be odd?")

A3 = ("Without adding them one at a time, decide whether "
      "1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10 is odd or even.")

A4 = ("Can the numbers 1, 2, 3, 4, 5, 6 be split into two groups that have "
      "the same total?")

B5 = ("Seven cups sit upside-down on a table. Each move, you must turn over "
      "exactly two cups. Can you ever get all seven cups right-side up?")

B6 = ("A grasshopper sits at 0 on a number line. It makes exactly nine jumps. "
      "Each jump moves it one step left or one step right. Can it land back "
      "on 0 after the ninth jump?")

C7 = ("Twenty-three children want to split into teams of exactly two for a "
      "game. It doesn't come out evenly. Their teacher offers to join in. "
      "Does adding the teacher fix it — or does she just need a partner too?")

C8 = ("Nine children sit around a round table. You want to give each child a "
      "hat, red or blue, so that no child sits next to someone wearing the "
      "same color. Can it be done?")

# ---- story ---------------------------------------------------------------
story = []

# page 1 top
story += [Paragraph("Saturday Test &mdash; No. 7", title_style),
          Paragraph("Take your time. Show your work where it helps.", subtitle_style),
          header_table(),
          Spacer(1, 0.12 * inch),
          Paragraph("Section A &mdash; Numbers and Patterns", section_style)]
story += problem(1, A1, 2)
story.append(FrameBreak())

# page 1 bottom
story += problem(2, A2, 5)
story.append(FrameBreak())

# page 2 top
story += problem(3, A3, 5)
story.append(FrameBreak())

# page 2 bottom
story += problem(4, A4, 5)
story.append(FrameBreak())

# page 3 top
story += [Paragraph("Section B &mdash; Counting Carefully", section_style)]
story += problem(5, B5, 5)
story.append(FrameBreak())

# page 3 bottom
story += problem(6, B6, 5)
story.append(FrameBreak())

# page 4 top
story += [Paragraph("Section C &mdash; Reasoning", section_style)]
story += problem(7, C7, 5)
story.append(FrameBreak())

# page 4 bottom
story += problem(8, C8, 6)
story.append(NextPageTemplate('single'))
story.append(PageBreak())

# ---- answer key ----------------------------------------------------------
story.append(Paragraph("Answer Key &mdash; for parents", ak_head_style))

answers = [
    ("1.", "<b>odd + odd = even, even + even = even, odd + even = odd.</b> "
           "(12, 12; 12, 8; 9, 13.) A sum is odd <i>only</i> when exactly one of "
           "the two numbers is odd. This is the tool for the whole test."),
    ("2.", "<b>No to both.</b> Two evens add to an even number, and two odds also "
           "add to an even number — but 15 is odd. So one number must be odd "
           "and the other even."),
    ("3.", "<b>Odd.</b> The even numbers (2,4,6,8,10) add to an even total; the odd "
           "numbers are 1,3,5,7,9 — five of them. An odd count of odd numbers "
           "makes the whole sum odd. (It is 55.)"),
    ("4.", "<b>No.</b> The six numbers add to 21, which is odd. Two equal groups "
           "would need each to total 21 ÷ 2, and you can't split an odd number "
           "into two equal whole-number halves."),
    ("5.", "<b>No.</b> Start with 0 cups up — an even number. Flipping exactly "
           "two cups changes the count of upright cups by 2, 0, or −2, so it "
           "stays even forever. 7 is odd, so it's out of reach. (The number of "
           "upright cups is the hidden thing that never turns odd.)"),
    ("6.", "<b>No.</b> To return to 0 it needs the same number of left jumps as "
           "right jumps — so an even number of jumps in total. Nine is odd. "
           "(After an odd number of ±1 steps the grasshopper is always on an "
           "odd number, never on 0.)"),
    ("7.", "<b>It works.</b> 23 is odd, so the children alone always leave one "
           "person without a partner. Adding the teacher makes 24, which is even, "
           "so they form 12 full teams of two. The trap is thinking “she needs "
           "a partner too,” but she's already counted in the 24."),
    ("8.", "<b>No.</b> Around the table the colors must alternate red, blue, red, "
           "blue, … With an even number of seats that works, but 9 is odd: "
           "follow the colors all the way around and the ninth child ends up next "
           "to the first child with the <i>same</i> color. (This is the same odd/"
           "even wall as the others.)"),
]
for num, txt in answers:
    story.append(Paragraph(f"<b>{num}</b>&nbsp;&nbsp;{txt}", ak_item_style))

doc.build(story)
print(f"wrote {OUTPUT}")
