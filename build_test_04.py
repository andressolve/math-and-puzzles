"""Build Saturday Test No. 4 — math_logic_test_04.pdf"""

import math
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, FrameBreak,
    Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether,
)
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import black, HexColor
from reportlab.graphics.shapes import Drawing, Line, String, Circle

OUTPUT = "/Users/andresrodriguez/Documents/payday_tests/math_logic_test_04.pdf"

# --- Page geometry ---
page_w, page_h = letter
left_m = right_m = 0.7 * inch
top_m, bot_m = 0.5 * inch, 0.6 * inch
content_w = page_w - left_m - right_m
content_h = page_h - top_m - bot_m
half_h = content_h / 2

top_frame = Frame(left_m, bot_m + half_h, content_w, half_h,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
bottom_frame = Frame(left_m, bot_m, content_w, half_h,
                     leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
two_tpl = PageTemplate(id='two', frames=[top_frame, bottom_frame])

single_frame = Frame(left_m, bot_m, content_w, content_h,
                     leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
single_tpl = PageTemplate(id='single', frames=[single_frame])

doc = BaseDocTemplate(OUTPUT, pagesize=letter,
                      leftMargin=left_m, rightMargin=right_m,
                      topMargin=top_m, bottomMargin=bot_m,
                      pageTemplates=[two_tpl, single_tpl])

# --- Styles ---
title_style = ParagraphStyle('title', fontName='Times-Bold', fontSize=22,
                             leading=26, alignment=TA_CENTER, spaceAfter=4)
sub_style = ParagraphStyle('sub', fontName='Times-Italic', fontSize=12,
                           leading=15, alignment=TA_CENTER, spaceAfter=12)
section_style = ParagraphStyle('section', fontName='Times-Bold', fontSize=14,
                               leading=18, alignment=TA_LEFT,
                               spaceAfter=10, spaceBefore=0)
prob_style = ParagraphStyle('prob', fontName='Times-Roman', fontSize=12,
                            leading=16, alignment=TA_LEFT, spaceAfter=2)
ans_h_style = ParagraphStyle('ah', fontName='Times-Bold', fontSize=16,
                             leading=20, alignment=TA_LEFT, spaceAfter=10)
ans_sec_style = ParagraphStyle('asec', fontName='Times-Bold', fontSize=12,
                               leading=15, alignment=TA_LEFT,
                               spaceAfter=4, spaceBefore=4)
ans_style = ParagraphStyle('ans', fontName='Times-Roman', fontSize=11,
                           leading=15, alignment=TA_LEFT, spaceAfter=10)


def workspace(n):
    return Spacer(1, 0.22 * inch * n)


def header_table():
    cell_style = ParagraphStyle('hcell', fontName='Times-Italic', fontSize=11,
                                alignment=TA_LEFT)
    rows = [[Paragraph("Name: ____________________", cell_style),
             Paragraph("Date: __________", cell_style),
             Paragraph("Time: 15 min", cell_style)]]
    t = Table(rows, colWidths=[content_w * 0.42, content_w * 0.30, content_w * 0.28])
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ('LEFTPADDING', (0, 0), (-1, -1), 0),
                           ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                           ('TOPPADDING', (0, 0), (-1, -1), 0),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
    return t


def clock_drawing():
    """Clock face showing 4:00 — hour hand on 4, minute hand on 12."""
    size = 1.7 * inch
    d = Drawing(size, size)
    cx = cy = size / 2
    r = size / 2 - 8
    # face
    d.add(Circle(cx, cy, r, strokeColor=black, strokeWidth=1.4, fillColor=None))
    # hour ticks (12 of them)
    for h in range(12):
        ang = math.radians(90 - h * 30)
        inner = r - 5
        x1 = cx + inner * math.cos(ang)
        y1 = cy + inner * math.sin(ang)
        x2 = cx + r * math.cos(ang)
        y2 = cy + r * math.sin(ang)
        d.add(Line(x1, y1, x2, y2, strokeColor=black, strokeWidth=1.0))
    # numerals at 12, 3, 6, 9
    for h, label in [(0, '12'), (3, '3'), (6, '6'), (9, '9')]:
        ang = math.radians(90 - h * 30)
        x = cx + (r - 14) * math.cos(ang)
        y = cy + (r - 14) * math.sin(ang) - 4
        d.add(String(x, y, label, fontName='Times-Roman', fontSize=10,
                     textAnchor='middle'))
    # hour hand -> 4 o'clock (120° clockwise from 12)
    ang_h = math.radians(90 - 4 * 30)
    hh_len = r * 0.55
    d.add(Line(cx, cy,
               cx + hh_len * math.cos(ang_h),
               cy + hh_len * math.sin(ang_h),
               strokeColor=black, strokeWidth=2.6))
    # minute hand -> 12 (straight up)
    mm_len = r * 0.82
    d.add(Line(cx, cy, cx, cy + mm_len,
               strokeColor=black, strokeWidth=1.6))
    # center pin
    d.add(Circle(cx, cy, 2.5, strokeColor=black, fillColor=black))
    return d


def lattice_drawing():
    """2x2 grid (3x3 lattice points) with start (BL) and end (TR) marked."""
    sq = 0.55 * inch
    pad = 0.30 * inch
    w = h = 2 * sq + 2 * pad
    d = Drawing(w, h)
    for i in range(3):
        x = pad + i * sq
        y = pad + i * sq
        d.add(Line(x, pad, x, pad + 2 * sq, strokeColor=black, strokeWidth=1.1))
        d.add(Line(pad, y, pad + 2 * sq, y, strokeColor=black, strokeWidth=1.1))
    # start dot (bottom-left)
    d.add(Circle(pad, pad, 4.0, strokeColor=black, fillColor=black))
    # end dot (top-right)
    d.add(Circle(pad + 2 * sq, pad + 2 * sq, 4.0,
                 strokeColor=black, fillColor=black))
    # labels
    d.add(String(pad - 4, pad - 14, "Start",
                 fontName='Times-Italic', fontSize=10,
                 textAnchor='start', fillColor=HexColor('#555555')))
    d.add(String(pad + 2 * sq + 4, pad + 2 * sq + 6, "End",
                 fontName='Times-Italic', fontSize=10,
                 textAnchor='start', fillColor=HexColor('#555555')))
    return d


def centered_drawing(drawing):
    t = Table([[drawing]], colWidths=[content_w])
    t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('LEFTPADDING', (0, 0), (-1, -1), 0),
                           ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                           ('TOPPADDING', (0, 0), (-1, -1), 0),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
    return t


# --- Build story ---
story = []

# Title block + Section A header + P1 (top half of page 1)
story.append(Paragraph("Saturday Test &mdash; No. 4", title_style))
story.append(Paragraph("Take your time. Show your work where it helps.", sub_style))
story.append(header_table())
story.append(Spacer(1, 0.18 * inch))
story.append(Paragraph("Numbers and Shapes", section_style))

# A1 — variables puzzle
a1 = ("<b>1.</b>&nbsp;&nbsp;Suppose <b>A</b> and <b>B</b> stand for two unknown numbers. "
      "If <b>A + A + A = 18</b> and <b>A + B = 11</b>, what is <b>B</b>?")
story.append(Paragraph(a1, prob_style))
story.append(workspace(5))
story.append(FrameBreak())

# A2 — digit-product
a2 = ("<b>2.</b>&nbsp;&nbsp;What is the largest two-digit number whose two digits "
      "multiply together to give 12?")
story.append(Paragraph(a2, prob_style))
story.append(workspace(6))
story.append(FrameBreak())

# A3 — clock angle
a3 = ("<b>3.</b>&nbsp;&nbsp;At exactly 4 o&rsquo;clock, what is the angle between "
      "the hour hand and the minute hand?")
story.append(KeepTogether([
    Paragraph(a3, prob_style),
    Spacer(1, 0.08 * inch),
    centered_drawing(clock_drawing()),
]))
story.append(workspace(3))
story.append(FrameBreak())

# A4 — LCM blink
a4 = ("<b>4.</b>&nbsp;&nbsp;A red light blinks every 6 seconds. A blue light blinks "
      "every 8 seconds. They blink together at time zero. After how many seconds "
      "will they next blink at exactly the same moment?")
story.append(Paragraph(a4, prob_style))
story.append(workspace(5))
story.append(FrameBreak())

# Section B header + P5
story.append(Paragraph("Counting Carefully", section_style))

# B5 — lattice paths
b5 = ("<b>5.</b>&nbsp;&nbsp;On the grid below, walk from <i>Start</i> to <i>End</i> "
      "by moving only <b>right</b> or <b>up</b> along the lines. How many different "
      "paths are there?")
story.append(KeepTogether([
    Paragraph(b5, prob_style),
    Spacer(1, 0.06 * inch),
    centered_drawing(lattice_drawing()),
]))
story.append(workspace(2))
story.append(FrameBreak())

# B6 — Venn / inclusion-exclusion
b6 = ("<b>6.</b>&nbsp;&nbsp;In a class of 20 students, 12 like apples, 9 like "
      "bananas, and 4 like both. How many students like neither apples nor bananas?")
story.append(Paragraph(b6, prob_style))
story.append(workspace(6))
story.append(FrameBreak())

# Section C header + P7
story.append(Paragraph("Reasoning", section_style))

# C7 — knights and knaves
c7 = ("<b>7.</b>&nbsp;&nbsp;On an island, every person is either a <i>knight</i> "
      "(who always tells the truth) or a <i>knave</i> (who always lies). You meet "
      "two islanders, <b>Pat</b> and <b>Quinn</b>.<br/><br/>"
      "&nbsp;&nbsp;&nbsp;&nbsp;Pat says: &ldquo;We are both knights.&rdquo;<br/>"
      "&nbsp;&nbsp;&nbsp;&nbsp;Quinn says: &ldquo;Pat is lying.&rdquo;<br/><br/>"
      "Who is the knight and who is the knave? Explain how you know.")
story.append(Paragraph(c7, prob_style))
story.append(workspace(3))
story.append(FrameBreak())

# C8 — water pouring
c8 = ("<b>8.</b>&nbsp;&nbsp;You have a <b>5-litre jug</b> and a <b>3-litre jug</b>, "
      "both empty, and a tap with all the water you want. Neither jug has any "
      "markings on it. How can you measure out exactly <b>4 litres</b> of water? "
      "Describe the steps.")
story.append(Paragraph(c8, prob_style))
story.append(workspace(7))

# Switch to single-frame for answer key
story.append(NextPageTemplate('single'))
story.append(PageBreak())

# Answer key
story.append(Paragraph("Answer Key &mdash; for parents", ans_h_style))

story.append(Paragraph("Numbers and Shapes", ans_sec_style))
story.append(Paragraph(
    "<b>1.</b>&nbsp;&nbsp;A + A + A = 18 means A = 6. Then A + B = 11, so "
    "B = 11 &minus; 6 = <b>5</b>.", ans_style))
story.append(Paragraph(
    "<b>2.</b>&nbsp;&nbsp;Digit pairs that multiply to 12: 2&times;6, 3&times;4 "
    "(and 6&times;2, 4&times;3). The two-digit numbers are 26, 34, 43, and 62. "
    "The largest is <b>62</b>.", ans_style))
story.append(Paragraph(
    "<b>3.</b>&nbsp;&nbsp;A full turn is 360&deg;, so each of the 12 hour-marks "
    "is 360&deg; &divide; 12 = 30&deg;. At 4 o&rsquo;clock the hour hand is at "
    "the 4 and the minute hand is at the 12, four hour-marks apart: "
    "4 &times; 30&deg; = <b>120&deg;</b>.", ans_style))
story.append(Paragraph(
    "<b>4.</b>&nbsp;&nbsp;The next moment they blink together is the smallest "
    "number that is a multiple of both 6 and 8 (the LCM). Multiples of 8: "
    "8, 16, <b>24</b>, &hellip; and 24 = 6 &times; 4. Answer: <b>24 seconds</b>.",
    ans_style))

story.append(Paragraph("Counting Carefully", ans_sec_style))
story.append(Paragraph(
    "<b>5.</b>&nbsp;&nbsp;Each path uses 2 right-moves and 2 up-moves in some "
    "order &mdash; choose which 2 of the 4 steps are rights. C(4,2) = "
    "<b>6 paths</b>. (RRUU, RURU, RUUR, URRU, URUR, UURR.)", ans_style))
story.append(Paragraph(
    "<b>6.</b>&nbsp;&nbsp;Students who like apples or bananas (or both): "
    "12 + 9 &minus; 4 = 17 (we subtract the 4 to avoid double-counting). "
    "Students who like neither: 20 &minus; 17 = <b>3</b>.", ans_style))

story.append(Paragraph("Reasoning", ans_sec_style))
story.append(Paragraph(
    "<b>7.</b>&nbsp;&nbsp;Suppose Pat were a knight. Then &ldquo;we are both "
    "knights&rdquo; would be true, making Quinn a knight too &mdash; but Quinn "
    "says Pat is lying, which a knight would never say about a fellow knight. "
    "Contradiction, so Pat must be a knave. Then Pat&rsquo;s claim is false, "
    "which is consistent. Quinn&rsquo;s claim &ldquo;Pat is lying&rdquo; is "
    "true, so Quinn is a knight. <b>Pat is the knave; Quinn is the knight.</b>",
    ans_style))
story.append(Paragraph(
    "<b>8.</b>&nbsp;&nbsp;One solution: "
    "(1) Fill the 5-L jug from the tap. "
    "(2) Pour from the 5-L into the 3-L until the 3-L is full &mdash; the 5-L "
    "now holds 2 L. "
    "(3) Empty the 3-L jug. "
    "(4) Pour the 2 L from the 5-L into the 3-L (now the 3-L holds 2 L). "
    "(5) Refill the 5-L from the tap. "
    "(6) Pour from the 5-L into the 3-L until the 3-L is full &mdash; only 1 L "
    "fits, leaving exactly <b>4 L in the 5-L jug</b>.", ans_style))

doc.build(story)
print(f"Wrote {OUTPUT}")
