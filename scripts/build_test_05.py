"""Build Saturday Test No. 5 — math_logic_test_05.pdf"""

from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, FrameBreak,
    Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether,
)
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import black, HexColor
from reportlab.graphics.shapes import Drawing, Line, String, Polygon, PolyLine

OUTPUT = "/Users/andresrodriguez/Documents/payday_tests/tests/math_logic_test_05.pdf"

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


def centered_drawing(drawing):
    t = Table([[drawing]], colWidths=[content_w])
    t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('LEFTPADDING', (0, 0), (-1, -1), 0),
                           ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                           ('TOPPADDING', (0, 0), (-1, -1), 0),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
    return t


def parallelogram_drawing():
    """Parallelogram with base 6 cm and height 4 cm. Dashed perpendicular cut
    from the top-left vertex down to the base; ghost triangle on the right
    slot showing where the cut piece would slide to complete the rectangle.

    Coordinates (reportlab y-up, 25 pt per cm):
      BL=(0,0)  BR=(150,0)  TR=(190,100)  TL=(40,100)
      perpendicular foot: (40, 0)
      ghost triangle:    (150,0)-(190,0)-(190,100)
    """
    from reportlab.graphics.shapes import Group
    import math as _m
    pad_left = 32
    pad_right = 14
    pad_top = 10
    pad_bot = 32
    fig_w = 190
    fig_h = 100
    w = fig_w + pad_left + pad_right
    h = fig_h + pad_top + pad_bot
    d = Drawing(w, h)

    def X(x): return x + pad_left
    def Y(y): return y + pad_bot

    # Ghost triangle (rearrangement destination).
    d.add(Polygon(
        points=[X(150), Y(0), X(190), Y(0), X(190), Y(100)],
        fillColor=HexColor('#eeeeea'),
        strokeColor=HexColor('#999999'),
        strokeWidth=1.0,
        strokeDashArray=[3, 3],
    ))

    # Parallelogram outline (solid black).
    d.add(Polygon(
        points=[X(0), Y(0), X(150), Y(0), X(190), Y(100), X(40), Y(100)],
        fillColor=None,
        strokeColor=black,
        strokeWidth=1.6,
    ))

    # Dashed perpendicular cut.
    d.add(Line(X(40), Y(100), X(40), Y(0),
               strokeColor=HexColor('#888888'),
               strokeWidth=1.0,
               strokeDashArray=[4, 4]))

    # Right-angle marker.
    d.add(PolyLine(
        points=[X(40), Y(8), X(48), Y(8), X(48), Y(0)],
        strokeColor=HexColor('#888888'),
        strokeWidth=1.0,
    ))

    # Base bracket + "6 cm" label.
    d.add(Line(X(0), Y(-12), X(150), Y(-12),
               strokeColor=HexColor('#666666'), strokeWidth=0.8))
    d.add(Line(X(0), Y(-16), X(0), Y(-8),
               strokeColor=HexColor('#666666'), strokeWidth=0.8))
    d.add(Line(X(150), Y(-16), X(150), Y(-8),
               strokeColor=HexColor('#666666'), strokeWidth=0.8))
    d.add(String(X(75), Y(-26), "6 cm",
                 fontName='Times-Italic', fontSize=11,
                 fillColor=HexColor('#444444'), textAnchor='middle'))

    # Height bracket.
    d.add(Line(X(-12), Y(0), X(-12), Y(100),
               strokeColor=HexColor('#666666'), strokeWidth=0.8))
    d.add(Line(X(-16), Y(0), X(-8), Y(0),
               strokeColor=HexColor('#666666'), strokeWidth=0.8))
    d.add(Line(X(-16), Y(100), X(-8), Y(100),
               strokeColor=HexColor('#666666'), strokeWidth=0.8))

    # Rotated "4 cm" label along the height bracket (90° CCW around its anchor).
    label = String(0, 0, "4 cm",
                   fontName='Times-Italic', fontSize=11,
                   fillColor=HexColor('#444444'), textAnchor='middle')
    g = Group(label)
    cos_t = _m.cos(_m.radians(90))
    sin_t = _m.sin(_m.radians(90))
    g.transform = (cos_t, sin_t, -sin_t, cos_t, X(-22), Y(50))
    d.add(g)

    return d


# --- Build story ---
story = []

# Title + header + Section A header + A1 (top of page 1)
story.append(Paragraph("Saturday Test &mdash; No. 5", title_style))
story.append(Paragraph("Take your time. Show your work where it helps.", sub_style))
story.append(header_table())
story.append(Spacer(1, 0.18 * inch))
story.append(Paragraph("Numbers and Shapes", section_style))

# A1 — smallest 4-digit number
a1 = ("<b>1.</b>&nbsp;&nbsp;Using each of the digits <b>5, 0, 8, 3</b> exactly once, "
      "write the <b>smallest</b> four-digit number you can.")
story.append(Paragraph(a1, prob_style))
story.append(workspace(5))
story.append(FrameBreak())

# A2 — perfect squares 1..30
a2 = ("<b>2.</b>&nbsp;&nbsp;List every <b>perfect square</b> between 1 and 30. "
      "(A perfect square is a number you get by multiplying a whole number by itself.)")
story.append(Paragraph(a2, prob_style))
story.append(workspace(5))
story.append(FrameBreak())

# A3 — divisibility 612
a3 = ("<b>3.</b>&nbsp;&nbsp;Take <b>612</b>.<br/>"
      "&nbsp;&nbsp;&nbsp;&nbsp;(a)&nbsp; Is it divisible by 3?<br/>"
      "&nbsp;&nbsp;&nbsp;&nbsp;(b)&nbsp; Now add up its digits. Is <i>that sum</i> divisible by 3?")
story.append(Paragraph(a3, prob_style))
story.append(workspace(5))
story.append(FrameBreak())

# A4 — divisibility 514
a4 = ("<b>4.</b>&nbsp;&nbsp;Take <b>514</b>.<br/>"
      "&nbsp;&nbsp;&nbsp;&nbsp;(a)&nbsp; Is it divisible by 3?<br/>"
      "&nbsp;&nbsp;&nbsp;&nbsp;(b)&nbsp; Now add up its digits. Is <i>that sum</i> divisible by 3?")
story.append(Paragraph(a4, prob_style))
story.append(workspace(5))
story.append(FrameBreak())

# A5 — parallelogram area (top of page 3)
a5 = ("<b>5.</b>&nbsp;&nbsp;Find the area of this parallelogram.")
story.append(KeepTogether([
    Paragraph(a5, prob_style),
    Spacer(1, 0.10 * inch),
    centered_drawing(parallelogram_drawing()),
]))
story.append(workspace(2))
story.append(FrameBreak())

# Section B header + B5 (bottom of page 3)
story.append(Paragraph("Counting Carefully", section_style))

b5 = ("<b>6.</b>&nbsp;&nbsp;You have only <b>3&cent;</b> stamps and <b>5&cent;</b> stamps "
      "(as many of each as you want). Which amounts from <b>1&cent; to 15&cent;</b> can you "
      "<b>not</b> make? List them all.")
story.append(Paragraph(b5, prob_style))
story.append(workspace(5))
story.append(FrameBreak())

# B6 — sock drawer (top of page 4)
b6 = ("<b>7.</b>&nbsp;&nbsp;A drawer holds <b>10 red socks</b> and <b>10 blue socks</b>, "
      "all mixed up. You reach in without looking and pull socks out one at a time. "
      "What is the <b>smallest</b> number of socks you must pull out to be <i>sure</i> "
      "you have <b>two red socks</b>?")
story.append(Paragraph(b6, prob_style))
story.append(workspace(4))
story.append(FrameBreak())

# Section C header + C7 (bottom of page 4)
story.append(Paragraph("Reasoning", section_style))

c7 = ("<b>8.</b>&nbsp;&nbsp;<b>10!</b> means "
      "1 &times; 2 &times; 3 &times; 4 &times; 5 &times; 6 &times; 7 &times; 8 &times; 9 &times; 10. "
      "<br/>How many <b>zeros</b> are at the end of this number?")
story.append(Paragraph(c7, prob_style))
story.append(workspace(5))

# Switch to single-frame for answer key.
story.append(NextPageTemplate('single'))
story.append(PageBreak())

# --- Answer key ---
story.append(Paragraph("Answer Key &mdash; for parents", ans_h_style))

story.append(Paragraph("Numbers and Shapes", ans_sec_style))
story.append(Paragraph(
    "<b>1.</b>&nbsp;&nbsp;The smallest four-digit number must start with the smallest "
    "non-zero digit available (the leading digit can&rsquo;t be 0). That&rsquo;s <b>3</b>. "
    "After placing 3, arrange the remaining digits 0, 5, 8 in ascending order: 058. "
    "Answer: <b>3058</b>.", ans_style))
story.append(Paragraph(
    "<b>2.</b>&nbsp;&nbsp;1&times;1=1, 2&times;2=4, 3&times;3=9, 4&times;4=16, 5&times;5=25. "
    "Next would be 6&times;6=36, which is past 30. Answer: "
    "<b>1, 4, 9, 16, 25</b>.", ans_style))
story.append(Paragraph(
    "<b>3.</b>&nbsp;&nbsp;(a) 612 &divide; 3 = 204 with no remainder, so <b>yes</b>, 612 is "
    "divisible by 3. (b) 6 + 1 + 2 = 9, and 9 &divide; 3 = 3 with no remainder, so "
    "<b>yes</b>, the digit-sum is also divisible by 3.", ans_style))
story.append(Paragraph(
    "<b>4.</b>&nbsp;&nbsp;(a) 514 &divide; 3 = 171 remainder 1, so <b>no</b>, 514 is not "
    "divisible by 3. (b) 5 + 1 + 4 = 10, and 10 &divide; 3 = 3 remainder 1, so "
    "<b>no</b>, the digit-sum is also not divisible by 3.<br/>"
    "<i>Pattern to point out:</i> the two methods agree on both numbers, and they always do. "
    "A whole number is divisible by 3 exactly when the sum of its digits is divisible by 3 &mdash; "
    "a real shortcut that works for any number, no matter how large.", ans_style))
story.append(Paragraph(
    "<b>5.</b>&nbsp;&nbsp;If you cut along the dashed line and slide the triangle from the "
    "left side over to the slot on the right, the parallelogram becomes a 6&times;4 rectangle "
    "&mdash; same area. So the area is base &times; height = 6 &times; 4 = "
    "<b>24 cm<super>2</super></b>. The lesson: for <i>any</i> parallelogram, "
    "area = base &times; perpendicular height (the slant doesn&rsquo;t matter).", ans_style))

story.append(Paragraph("Counting Carefully", ans_sec_style))
story.append(Paragraph(
    "<b>6.</b>&nbsp;&nbsp;Reachable amounts: 3, 5, 6 (=3+3), 8 (=3+5), 9 (=3+3+3), "
    "10 (=5+5), 11 (=3+3+5), 12 (=3+3+3+3), 13 (=3+5+5), 14 (=3+3+3+5), 15 (=5+5+5 or 3&times;5). "
    "Cannot be made: <b>1&cent;, 2&cent;, 4&cent;, 7&cent;</b>. "
    "<i>Worth noticing:</i> once you reach 8&cent;, you can also get 9&cent; and 10&cent;, "
    "and after that you can keep adding 3&cent; forever &mdash; so every amount from 8&cent; "
    "upward is reachable. 7&cent; is the last impossible amount.", ans_style))
story.append(Paragraph(
    "<b>7.</b>&nbsp;&nbsp;Worst case: you pull out every blue sock first (all 10), then "
    "the next two pulls must be red. So you need <b>12</b> socks to be sure. "
    "(With 11 socks you might have all 10 blues plus 1 red &mdash; still only one red.)",
    ans_style))

story.append(Paragraph("Reasoning", ans_sec_style))
story.append(Paragraph(
    "<b>8.</b>&nbsp;&nbsp;A zero at the end of a number comes from a factor of 10, and "
    "10 = 2 &times; 5. So the number of trailing zeros equals the number of (2,5) pairs you "
    "can pull out of the product. Factors of 5 in 1&times;2&times;&hellip;&times;10: only "
    "<b>5</b> and <b>10</b> contribute (one 5 each). Factors of 2: plenty &mdash; 2, 4, 6, 8, 10 "
    "give more than enough 2s to pair with. So exactly <b>2</b> trailing zeros. "
    "(Check: 10! = 3,628,800.) <i>The big idea:</i> you didn&rsquo;t need to compute 10! at all "
    "&mdash; the 5s are the bottleneck.", ans_style))

doc.build(story)
print(f"Wrote {OUTPUT}")
