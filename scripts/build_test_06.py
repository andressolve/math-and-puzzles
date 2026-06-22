"""Saturday Test No. 6 — doubling 'Staircase' (A & B) + a 'Find the Angle' finish (C)."""
import math
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, FrameBreak,
    Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether,
)
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import black, HexColor
from reportlab.graphics.shapes import Drawing, Line, String, Wedge

OUTPUT = "/Users/andresrodriguez/Documents/payday_tests/tests/math_logic_test_06.pdf"
GREY = HexColor('#555555')
INK = black

# ----- angle-diagram helpers (Section C) -------------------------------------

def arc(d, cx, cy, r, a0, a1):
    w = Wedge(cx, cy, r, a0, a1)
    w.fillColor = None
    w.strokeColor = GREY
    w.strokeWidth = 1.0
    d.add(w)

def lbl(d, x, y, t, size=15, bold=True):
    d.add(String(x, y - size * 0.36, t, fontName='Times-Bold' if bold else 'Times-Roman',
                 fontSize=size, fillColor=INK, textAnchor='middle'))

def L(d, x1, y1, x2, y2, w=1.5):
    d.add(Line(x1, y1, x2, y2, strokeColor=INK, strokeWidth=w))

# C7 — two lines crossing, give 50, find opposite & adjacent
def d_cross():
    d = Drawing(300, 150)
    O = (150, 72)
    L(d, 60, 72, 240, 72, 1.6)
    L(d, 92, 3, 208, 141, 1.6)
    arc(d, O[0], O[1], 20, 0, 50)
    arc(d, O[0], O[1], 20, 180, 230)
    arc(d, O[0], O[1], 20, 50, 180)
    lbl(d, 186, 89, "50°")
    lbl(d, 114, 55, "?")
    lbl(d, 133, 108, "?")
    return d

# C8 — parallelogram from four lines (Style 1, extended), give 70, find all
def d_parallelogram():
    A, B = (150, 130), (400, 130)
    V = (48, 132)
    slo, shi = -0.55, 1.6
    xmin, ymin, sc, pad = 70, 57.4, 0.62, 9

    def m(x, y):
        return ((x - xmin) * sc + pad, (y - ymin) * sc + pad)

    d = Drawing((530 - xmin) * sc + 2 * pad, (341.2 - ymin) * sc + 2 * pad)

    def pt(P, s):
        return (P[0] + s * V[0], P[1] + s * V[1])

    L(d, *m(xmin, 130), *m(530, 130), 1.5)
    L(d, *m(xmin, 262), *m(530, 262), 1.5)
    L(d, *m(*pt(A, slo)), *m(*pt(A, shi)), 1.5)
    L(d, *m(*pt(B, slo)), *m(*pt(B, shi)), 1.5)

    def chev(px, py, dx, dy, n):
        s = 6.5
        nx, ny = -dy, dx
        for i in range(n):
            bx, by = px - i * 6 * dx, py - i * 6 * dy
            L(d, *m(bx - s*dx + s*nx, by - s*dy + s*ny), *m(bx, by), 1.2)
            L(d, *m(bx - s*dx - s*nx, by - s*dy - s*ny), *m(bx, by), 1.2)

    uv = (V[0] / 140.3, V[1] / 140.3)
    chev(300, 130, 1, 0, 1)
    chev(300, 262, 1, 0, 1)
    chev(174, 196, uv[0], uv[1], 2)
    chev(424, 196, uv[0], uv[1], 2)

    gx, gy = m(179.8, 143.2); lbl(d, gx, gy, "70°", size=14)
    for (x, y) in [(379.8, 143.2), (418.2, 248.8), (218.2, 248.8),
                   (118, 104), (470, 96), (176, 296), (430, 296)]:
        px, py = m(x, y); lbl(d, px, py, "?", size=14, bold=False)
    return d

# ----- document --------------------------------------------------------------

styles = getSampleStyleSheet()
title_st = ParagraphStyle('t', parent=styles['Title'], fontName='Times-Bold',
                          fontSize=20, spaceAfter=4, alignment=TA_CENTER)
sub_st = ParagraphStyle('s', parent=styles['Normal'], fontName='Times-Italic',
                        fontSize=11.5, alignment=TA_CENTER, textColor=HexColor('#333333'),
                        spaceAfter=12)
sec_st = ParagraphStyle('sec', parent=styles['Normal'], fontName='Times-Bold',
                        fontSize=13, spaceBefore=2, spaceAfter=10)
prob_st = ParagraphStyle('p', parent=styles['Normal'], fontName='Times-Roman',
                         fontSize=12.5, leading=16, spaceAfter=6)
hdr_st = ParagraphStyle('h', parent=styles['Normal'], fontName='Times-Roman', fontSize=11)
ak_title = ParagraphStyle('akt', parent=styles['Title'], fontName='Times-Bold',
                          fontSize=16, alignment=TA_CENTER, spaceAfter=12)
ak_st = ParagraphStyle('ak', parent=styles['Normal'], fontName='Times-Roman',
                       fontSize=11.5, leading=15, spaceAfter=7)

def prob(n, text, drawing=None, lines=5):
    flow = [Paragraph(f"<b>{n}.</b>&nbsp;&nbsp;{text}", prob_st)]
    if drawing is not None:
        flow += [Spacer(1, 6), drawing]
    if lines:
        flow.append(Spacer(1, 0.22 * inch * lines))
    return KeepTogether(flow)

page_w, page_h = letter
left_m = right_m = 0.7 * inch
top_m, bot_m = 0.5 * inch, 0.6 * inch
content_w = page_w - left_m - right_m
content_h = page_h - top_m - bot_m
half_h = content_h / 2

top_frame = Frame(left_m, bot_m + half_h, content_w, half_h, 0, 0, 0, 0)
bottom_frame = Frame(left_m, bot_m, content_w, half_h, 0, 0, 0, 0)
two_tpl = PageTemplate(id='two', frames=[top_frame, bottom_frame])
single = Frame(left_m, bot_m, content_w, content_h, 0, 0, 0, 0)
single_tpl = PageTemplate(id='single', frames=[single])

doc = BaseDocTemplate(OUTPUT, pagesize=letter, leftMargin=left_m, rightMargin=right_m,
                      topMargin=top_m, bottomMargin=bot_m,
                      pageTemplates=[two_tpl, single_tpl])

story = []
story.append(Paragraph("Saturday Test &mdash; No. 6", title_st))
story.append(Paragraph("Take your time. Show your work where it helps.", sub_st))
hdr = Table([[Paragraph("Name: ____________________", hdr_st),
              Paragraph("Date: ____________", hdr_st),
              Paragraph("Time: 15 min", hdr_st)]],
            colWidths=[content_w * 0.45, content_w * 0.30, content_w * 0.25])
hdr.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0),
                         ('BOTTOMPADDING', (0, 0), (-1, -1), 10)]))
story.append(hdr)

story.append(Paragraph("Numbers and Shapes", sec_st))
story.append(prob(1, "You fold a strip of paper in half, then in half again, then again. Each fold doubles the number of layers: 2, then 4, then 8. How many layers are there after 6 folds?"))
story.append(FrameBreak())
story.append(prob(2, "You cut a square in half. Then you cut one of those pieces in half. Then one of <i>those</i> pieces in half — and so on. After 4 cuts in all, what fraction of the whole square is the smallest piece?"))
story.append(FrameBreak())
story.append(prob(3, "A patch of lily pads doubles in size every day. It covers the whole pond on day 30. On which day was the pond exactly half covered?"))
story.append(FrameBreak())
story.append(prob(4, "Look at this pattern: 1, 3, 7, 15, 31, &hellip; &nbsp;Each number is double the one before, plus one. What are the next two numbers?"))
story.append(FrameBreak())

story.append(Paragraph("Counting Carefully", sec_st))
story.append(prob(5, "On day 1, one kid knows a secret. Each day, every kid who already knows it tells exactly one new kid. How many kids know the secret on day 6?"))
story.append(FrameBreak())
story.append(prob(6, "Sixteen kids enter a tennis tournament. In each game two kids play, and the loser is out &mdash; they go home. The winners keep playing new games until just one champion is left. How many games are played in all?"))
story.append(FrameBreak())

story.append(Paragraph("Find the Angle", sec_st))
story.append(prob(7, "Two straight lines cross. One of the angles is 50°. Find the angle directly across from it, and the angle right next to it.", d_cross(), lines=2))
story.append(FrameBreak())
story.append(prob(8, "These four lines cross to form a parallelogram. The arrows show which sides run parallel. One angle is 70°. Find all of the other angles.", d_parallelogram(), lines=1))

story.append(NextPageTemplate('single'))
story.append(PageBreak())

# Answer key
story.append(Paragraph("Answer Key &mdash; for parents", ak_title))
answers = [
    ("1.", "<b>64.</b> Each fold doubles the layers: 2, 4, 8, 16, 32, 64."),
    ("2.", "<b>1/16.</b> Each cut halves the smallest piece: 1/2, 1/4, 1/8, 1/16."),
    ("3.", "<b>Day 29.</b> It doubles every day, so the day before the pond is full it must be half full &mdash; one day before day 30."),
    ("4.", "<b>63 and 127.</b> Double and add one: 31 → 63 → 127."),
    ("5.", "<b>32.</b> The number of kids who know it doubles each day: 1, 2, 4, 8, 16, 32."),
    ("6.", "<b>15 games.</b> Every game sends exactly one kid home. To go from 16 kids down to 1 champion, 15 kids must leave &mdash; so 15 games. (No need to add up the rounds.)"),
    ("7.", "<b>Opposite = 50°, next to it = 130°.</b> The angle straight across is equal (vertical angles). The neighbour sits with the 50° on a straight line, so 180 − 50 = 130."),
    ("8.", "<b>Every angle is 70° or 110°.</b> Opposite corners of a parallelogram are equal (the corner across from 70° is also 70°); neighbouring corners add to 180° (so the other two are 110°). At each crossing the X repeats those same two numbers — across is equal, beside makes 180° — so 70° and 110° fill the whole picture."),
]
for n, a in answers:
    story.append(Paragraph(f"<b>{n}</b>&nbsp;&nbsp;{a}", ak_st))

doc.build(story)
print("wrote", OUTPUT)
