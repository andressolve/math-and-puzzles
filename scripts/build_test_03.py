"""Saturday Test — No. 3. Builds math_logic_test_03.pdf."""

import math
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, FrameBreak,
    Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether,
)
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import black, HexColor, white
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String, Circle, Path
from reportlab.platypus.flowables import Flowable

OUTPUT = "/Users/andresrodriguez/Documents/payday_tests/tests/math_logic_test_03.pdf"

# Page geometry
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
two_frame_tpl = PageTemplate(id='two', frames=[top_frame, bottom_frame])

single_frame = Frame(left_m, bot_m, content_w, content_h,
                     leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
single_tpl = PageTemplate(id='single', frames=[single_frame])

doc = BaseDocTemplate(OUTPUT, pagesize=letter,
                      leftMargin=left_m, rightMargin=right_m,
                      topMargin=top_m, bottomMargin=bot_m,
                      pageTemplates=[two_frame_tpl, single_tpl])

# Styles
title_style = ParagraphStyle('title', fontName='Times-Bold', fontSize=22,
                             leading=26, alignment=TA_CENTER, spaceAfter=4)
subtitle_style = ParagraphStyle('subtitle', fontName='Times-Italic', fontSize=12,
                                leading=16, alignment=TA_CENTER, spaceAfter=10,
                                textColor=HexColor('#444444'))
section_style = ParagraphStyle('section', fontName='Times-Bold', fontSize=13,
                               leading=16, alignment=TA_LEFT, spaceBefore=0,
                               spaceAfter=8, textColor=HexColor('#222222'))
body_style = ParagraphStyle('body', fontName='Times-Roman', fontSize=12.5,
                            leading=17, alignment=TA_LEFT)
ans_style = ParagraphStyle('ans', fontName='Times-Roman', fontSize=11.5,
                           leading=15.5, alignment=TA_LEFT)
ans_h_style = ParagraphStyle('ansH', fontName='Times-Bold', fontSize=15,
                             leading=18, alignment=TA_LEFT, spaceAfter=8)

# Header table: Name | Date | Time
def header_table():
    data = [["Name __________________________",
             "Date ____________",
             "Time: 15 min"]]
    t = Table(data, colWidths=[content_w*0.50, content_w*0.30, content_w*0.20])
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,-1), 11.5),
        ('TEXTCOLOR', (0,0), (-1,-1), HexColor('#333333')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    return t

def working_space(n_lines=5):
    return Spacer(1, 0.22 * inch * n_lines)

# Diagrams ---------------------------------------------------------------

def equilateral_triangle(side=2.0*inch, stroke_w=1.6):
    pad = 0.12 * inch
    h = side * math.sqrt(3) / 2
    w = side
    d = Drawing(w + 2*pad, h + 2*pad)
    p1 = (pad, pad)
    p2 = (pad + w, pad)
    p3 = (pad + w/2, pad + h)
    d.add(Polygon([p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]],
                  strokeColor=black, strokeWidth=stroke_w, fillColor=None))
    return d

def midpoint_triangle(side=2.2*inch, stroke_w=1.5):
    pad = 0.12 * inch
    h = side * math.sqrt(3) / 2
    d = Drawing(side + 2*pad, h + 2*pad)
    p1 = (pad, pad)
    p2 = (pad + side, pad)
    p3 = (pad + side/2, pad + h)
    # midpoints
    m12 = ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)
    m23 = ((p2[0]+p3[0])/2, (p2[1]+p3[1])/2)
    m13 = ((p1[0]+p3[0])/2, (p1[1]+p3[1])/2)
    # outer triangle
    d.add(Polygon([p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]],
                  strokeColor=black, strokeWidth=stroke_w, fillColor=None))
    # inner triangle (midpoints connected)
    d.add(Line(m12[0], m12[1], m23[0], m23[1], strokeColor=black, strokeWidth=stroke_w))
    d.add(Line(m23[0], m23[1], m13[0], m13[1], strokeColor=black, strokeWidth=stroke_w))
    d.add(Line(m13[0], m13[1], m12[0], m12[1], strokeColor=black, strokeWidth=stroke_w))
    return d

def balance_scale(width=2.0*inch):
    """Simple balance scale icon: triangular fulcrum, horizontal beam, two pans."""
    pad = 0.1 * inch
    w = width
    h = 1.5 * inch
    d = Drawing(w + 2*pad, h + 2*pad)
    cx = pad + w/2
    base_y = pad + 0.05*inch
    # Fulcrum (triangle)
    fh = 0.65 * inch
    fw = 0.6 * inch
    d.add(Polygon([cx - fw/2, base_y,
                   cx + fw/2, base_y,
                   cx, base_y + fh],
                  strokeColor=black, strokeWidth=1.4, fillColor=HexColor('#dddddd')))
    # Base line under fulcrum
    d.add(Line(cx - 0.5*inch, base_y, cx + 0.5*inch, base_y,
               strokeColor=black, strokeWidth=1.6))
    # Beam
    beam_y = base_y + fh + 0.05*inch
    half_beam = 0.85 * inch
    d.add(Line(cx - half_beam, beam_y, cx + half_beam, beam_y,
               strokeColor=black, strokeWidth=1.6))
    # Suspension strings
    string_h = 0.32 * inch
    d.add(Line(cx - half_beam, beam_y, cx - half_beam - 0.18*inch, beam_y - string_h,
               strokeColor=black, strokeWidth=0.9))
    d.add(Line(cx - half_beam, beam_y, cx - half_beam + 0.18*inch, beam_y - string_h,
               strokeColor=black, strokeWidth=0.9))
    d.add(Line(cx + half_beam, beam_y, cx + half_beam - 0.18*inch, beam_y - string_h,
               strokeColor=black, strokeWidth=0.9))
    d.add(Line(cx + half_beam, beam_y, cx + half_beam + 0.18*inch, beam_y - string_h,
               strokeColor=black, strokeWidth=0.9))
    # Pans (shallow arcs drawn as polygons)
    pan_y = beam_y - string_h
    pan_w = 0.5 * inch
    for px in (cx - half_beam, cx + half_beam):
        # Pan: a shallow bowl shape using a polygon
        d.add(Polygon([px - pan_w, pan_y,
                       px + pan_w, pan_y,
                       px + pan_w*0.7, pan_y - 0.18*inch,
                       px - pan_w*0.7, pan_y - 0.18*inch],
                      strokeColor=black, strokeWidth=1.2, fillColor=HexColor('#f0f0f0')))
        # Pan top line
        d.add(Line(px - pan_w, pan_y, px + pan_w, pan_y,
                   strokeColor=black, strokeWidth=1.2))
    # Top knob on fulcrum
    d.add(Circle(cx, beam_y, 0.045*inch, strokeColor=black,
                 strokeWidth=1.0, fillColor=black))
    return d

def magic_square(cell=0.65*inch, given=None):
    """3x3 grid. given is dict mapping (col, row) -> str ('row 0' is top).
    Coordinates: col 0..2 left-to-right, row 0..2 top-to-bottom."""
    if given is None:
        given = {}
    pad = 0.1 * inch
    w = 3*cell + 2*pad
    h = 3*cell + 2*pad
    d = Drawing(w, h)
    for r in range(3):
        for c in range(3):
            x = pad + c*cell
            y = pad + (2 - r)*cell  # flip so row 0 is top
            d.add(Rect(x, y, cell, cell, strokeColor=black, strokeWidth=1.4,
                       fillColor=white))
            if (c, r) in given:
                txt = given[(c, r)]
                d.add(String(x + cell/2, y + cell/2 - 6, txt,
                             fontName='Times-Bold', fontSize=20,
                             textAnchor='middle', fillColor=black))
    return d

# Helper for centered drawing
def centered(drawing):
    t = Table([[drawing]], colWidths=[content_w])
    t.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    return t

# Story ------------------------------------------------------------------

story = []

# Page 1 top: Title block + A1
story.append(Paragraph("Saturday Test &mdash; No.&nbsp;3", title_style))
story.append(Paragraph("Take your time. Show your work where it helps.", subtitle_style))
story.append(header_table())
story.append(Spacer(1, 0.18*inch))
story.append(Paragraph("Numbers and Shapes", section_style))
story.append(Paragraph(
    "<b>1.</b>&nbsp;&nbsp;Fill in the missing numbers in the sequence:",
    body_style))
story.append(Spacer(1, 0.10*inch))
story.append(Paragraph(
    "&nbsp;&nbsp;&nbsp;&nbsp;3,&nbsp;&nbsp;7,&nbsp;&nbsp;11,&nbsp;&nbsp;______,&nbsp;&nbsp;______,&nbsp;&nbsp;23",
    ParagraphStyle('seq', parent=body_style, fontSize=14, leading=20)))
story.append(working_space(4))
story.append(FrameBreak())

# Page 1 bottom: A2
story.append(Paragraph(
    "<b>2.</b>&nbsp;&nbsp;How many lines of symmetry does an equilateral triangle have? "
    "Draw them on the figure below.",
    body_style))
story.append(Spacer(1, 0.10*inch))
story.append(centered(equilateral_triangle(side=1.9*inch)))
story.append(Spacer(1, 0.10*inch))
story.append(Paragraph("Answer: ____________", body_style))
story.append(FrameBreak())

# Page 2 top: A3
story.append(Paragraph(
    "<b>3.</b>&nbsp;&nbsp;A rectangle has whole-number side lengths and a "
    "perimeter of 20&nbsp;cm. What dimensions give the largest possible area? "
    "What is that area?",
    body_style))
story.append(working_space(7))
story.append(FrameBreak())

# Page 2 bottom: A4
story.append(Paragraph(
    "<b>4.</b>&nbsp;&nbsp;List every prime number between 20 and 40.",
    body_style))
story.append(working_space(7))
story.append(FrameBreak())

# Page 3 top: Section B header + B5
story.append(Paragraph("Counting Carefully", section_style))
story.append(Paragraph(
    "<b>5.</b>&nbsp;&nbsp;Write down the whole numbers from 1 to 20. "
    "How many times does the digit \u20181\u2019 appear in your list?",
    body_style))
story.append(working_space(6))
story.append(FrameBreak())

# Page 3 bottom: B6
story.append(Paragraph(
    "<b>6.</b>&nbsp;&nbsp;In the figure below, the three midpoints of an "
    "equilateral triangle have been connected. How many triangles can you find "
    "in the figure? Count triangles of every size.",
    body_style))
story.append(Spacer(1, 0.08*inch))
story.append(centered(midpoint_triangle(side=2.0*inch)))
story.append(Spacer(1, 0.06*inch))
story.append(Paragraph("Answer: ____________", body_style))
story.append(FrameBreak())

# Page 4 top: Section C header + C7 (with balance scale)
story.append(Paragraph("Reasoning", section_style))
story.append(centered(balance_scale(width=1.8*inch)))
story.append(Spacer(1, 0.04*inch))
story.append(Paragraph(
    "<b>7.</b>&nbsp;&nbsp;You have 9 coins that look identical, but one is "
    "slightly heavier than the rest. Using a balance scale, find the heavier "
    "coin in just 2 weighings. Describe your strategy.",
    body_style))
story.append(working_space(4))
story.append(FrameBreak())

# Page 4 bottom: C8 (magic square)
story.append(Paragraph(
    "<b>8.</b>&nbsp;&nbsp;Fill in the empty cells of the grid below so that "
    "every row, every column, and both diagonals add to 15. "
    "Use each of the digits 1 through 9 exactly once.",
    body_style))
story.append(Spacer(1, 0.10*inch))
story.append(centered(magic_square(cell=0.7*inch,
                                   given={(0,0): "2", (1,0): "9", (1,1): "5"})))
story.append(NextPageTemplate('single'))
story.append(PageBreak())

# Page 5: Answer key
story.append(Paragraph("Answer Key &mdash; for parents", ans_h_style))
story.append(Paragraph(
    "<b>1.</b>&nbsp;&nbsp;<b>15, 19.</b> Constant difference of 4.", ans_style))
story.append(Spacer(1, 0.06*inch))
story.append(Paragraph(
    "<b>2.</b>&nbsp;&nbsp;<b>3 lines of symmetry.</b> One through each vertex "
    "to the midpoint of the opposite side.", ans_style))
story.append(Spacer(1, 0.06*inch))
story.append(Paragraph(
    "<b>3.</b>&nbsp;&nbsp;<b>5&nbsp;cm &times; 5&nbsp;cm, area = 25&nbsp;cm<super>2</super>.</b> "
    "Among rectangles with a fixed perimeter, the square has the largest area. "
    "Other options: 1&times;9 (9), 2&times;8 (16), 3&times;7 (21), 4&times;6 (24).", ans_style))
story.append(Spacer(1, 0.06*inch))
story.append(Paragraph(
    "<b>4.</b>&nbsp;&nbsp;<b>23, 29, 31, 37.</b> "
    "(21=3&times;7, 25=5&times;5, 27=3<super>3</super>, 33=3&times;11, 35=5&times;7, 39=3&times;13.)",
    ans_style))
story.append(Spacer(1, 0.06*inch))
story.append(Paragraph(
    "<b>5.</b>&nbsp;&nbsp;<b>12.</b> Ones place: 1, 11 contribute 2 ones. "
    "Tens place: 10\u201319 contribute 10 ones. Total 12. "
    "Common slip: forgetting that 11 has two 1s.", ans_style))
story.append(Spacer(1, 0.06*inch))
story.append(Paragraph(
    "<b>6.</b>&nbsp;&nbsp;<b>5 triangles.</b> Three small upright triangles at "
    "the corners, one small inverted triangle in the centre, and the original "
    "large triangle.", ans_style))
story.append(Spacer(1, 0.06*inch))
story.append(Paragraph(
    "<b>7.</b>&nbsp;&nbsp;<b>Split into three groups of 3.</b> "
    "<i>Weighing 1:</i> weigh group A against group B. If they balance, the "
    "heavy coin is in group C; otherwise it is in the heavier of A or B. "
    "Take that group of 3. <i>Weighing 2:</i> weigh one coin against another, "
    "set the third aside. Same logic identifies the coin. "
    "The key insight: a balance has three outcomes, so divide into thirds, not halves.",
    ans_style))
story.append(Spacer(1, 0.10*inch))
story.append(Paragraph("<b>8.</b>&nbsp;&nbsp;Magic square solution:", ans_style))
story.append(Spacer(1, 0.05*inch))
solved = magic_square(cell=0.55*inch, given={
    (0,0): "2", (1,0): "9", (2,0): "4",
    (0,1): "7", (1,1): "5", (2,1): "3",
    (0,2): "6", (1,2): "1", (2,2): "8",
})
# Left-align the solution grid
sol_table = Table([[solved]], colWidths=[content_w])
sol_table.setStyle(TableStyle([
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
]))
story.append(sol_table)

doc.build(story)
print(f"Built: {OUTPUT}")
