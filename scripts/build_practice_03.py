"""Build Practice Set No. 3 — Dominoes and the Checkerboard."""

from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, FrameBreak,
    Paragraph, Spacer, PageBreak, KeepTogether,
)
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.graphics.shapes import Drawing, Rect, Line
from reportlab.lib.colors import HexColor, white

OUTPUT = "/Users/andresrodriguez/Documents/payday_tests/practice_sets/practice_set_03.pdf"

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
                             leading=26, alignment=TA_CENTER, spaceAfter=2)
sub_style = ParagraphStyle('sub', fontName='Times-Italic', fontSize=13,
                           leading=16, alignment=TA_CENTER, spaceAfter=4)
frame_line_style = ParagraphStyle('frame', fontName='Times-Italic', fontSize=12,
                                  leading=15, alignment=TA_CENTER, spaceAfter=14)
prob_style = ParagraphStyle('prob', fontName='Times-Roman', fontSize=12,
                            leading=16, alignment=TA_LEFT, spaceAfter=2)
ans_h_style = ParagraphStyle('ah', fontName='Times-Bold', fontSize=16,
                             leading=20, alignment=TA_LEFT, spaceAfter=10)
ans_style = ParagraphStyle('ans', fontName='Times-Roman', fontSize=11,
                           leading=15, alignment=TA_LEFT, spaceAfter=10)

# --- Checkerboard palette ---
DARK = HexColor('#33475b')
LIGHT = HexColor('#e8edf1')
GRIDLINE = HexColor('#7a8a99')
ABSENT_BORDER = HexColor('#c5ced6')
XCOLOR = HexColor('#b03030')


def board(cols, rows, sq, shaded=False, removed=(), crossed=(), pad=7):
    """A grid. shaded=checkerboard. removed=(c,r) drawn as gaps.
    crossed=(c,r) keep square but draw a red X."""
    removed = set(removed)
    crossed = set(crossed)
    w = cols * sq + 2 * pad
    h = rows * sq + 2 * pad
    d = Drawing(w, h)
    for c in range(cols):
        for r in range(rows):
            x = pad + c * sq
            y = pad + r * sq
            if (c, r) in removed:
                d.add(Rect(x, y, sq, sq, fillColor=white,
                           strokeColor=ABSENT_BORDER, strokeWidth=0.8,
                           strokeDashArray=[3, 3]))
                continue
            fill = (DARK if (c + r) % 2 == 0 else LIGHT) if shaded else white
            d.add(Rect(x, y, sq, sq, fillColor=fill,
                       strokeColor=GRIDLINE, strokeWidth=0.9))
    for (c, r) in crossed:
        x = pad + c * sq
        y = pad + r * sq
        m = sq * 0.2
        d.add(Line(x + m, y + m, x + sq - m, y + sq - m,
                   strokeColor=XCOLOR, strokeWidth=2.4))
        d.add(Line(x + m, y + sq - m, x + sq - m, y + m,
                   strokeColor=XCOLOR, strokeWidth=2.4))
    d.hAlign = 'CENTER'
    return d


def diagram(d):
    return [Spacer(1, 0.10 * inch), d, Spacer(1, 0.10 * inch)]


def workspace(n):
    return Spacer(1, 0.22 * inch * n)


story = []

# --- Title block + framing ---
story.append(Paragraph("Practice Set No. 3", title_style))
story.append(Paragraph("Dominoes and the Checkerboard", sub_style))
story.append(Paragraph(
    "A domino is a tile that covers two squares side by side. "
    "Take your time &mdash; the trick is to notice, not to compute.",
    frame_line_style))

# P1 — physical warm-up (cut-out sheet)
p1 = ("<b>1.</b>&nbsp;&nbsp;On the last sheet you will find paper dominoes and "
      "a small board to cut out. Each <b>domino</b> covers exactly two squares "
      "that sit next to each other. Cover the board completely &mdash; no gaps, "
      "no overlaps, nothing hanging off the edge. How many dominoes did it take?")
story.append(KeepTogether(
    [Paragraph(p1, prob_style)] + diagram(board(3, 2, 0.42 * inch)) + [workspace(3)]))
story.append(FrameBreak())

# P2 — odd/even parity (the Test #7 tool)
p2 = ("<b>2.</b>&nbsp;&nbsp;Here is a board with nine squares. Try to cover it "
      "with dominoes the same way. Can you do it? Explain why or why not.")
story.append(KeepTogether(
    [Paragraph(p2, prob_style)] + diagram(board(3, 3, 0.42 * inch)) + [workspace(3)]))
story.append(FrameBreak())

# P3 — notice the coloring
p3 = ("<b>3.</b>&nbsp;&nbsp;This board is shaded like a checkerboard. Picture "
      "covering it with dominoes &mdash; each one lies flat across two squares "
      "that share an edge. Pick any spot for a domino: <b>what two colors does "
      "it land on?</b> Is that always true, no matter where it goes?")
story.append(KeepTogether(
    [Paragraph(p3, prob_style)]
    + diagram(board(4, 4, 0.42 * inch, shaded=True)) + [workspace(3)]))
story.append(FrameBreak())

# P4 — same-color removal fails
p4 = ("<b>4.</b>&nbsp;&nbsp;On this board the two squares marked "
      "<font color='#b03030'><b>X</b></font> have been taken away &mdash; they "
      "sit in opposite corners, and notice they are the <b>same color</b>. Now "
      "try to cover the 14 squares that remain. Can you? Count how many dark and "
      "how many light squares are left, and use problem 3 to explain.")
story.append(KeepTogether(
    [Paragraph(p4, prob_style)]
    + diagram(board(4, 4, 0.42 * inch, shaded=True, crossed=[(0, 0), (3, 3)]))
    + [workspace(3)]))
story.append(FrameBreak())

# P5 — the mutilated chessboard
p5 = ("<b>5.</b>&nbsp;&nbsp;A full chessboard has 8 &times; 8 = 64 squares. "
      "Two opposite corners are cut off, leaving 62 squares. Could exactly "
      "<b>31 dominoes</b> cover what is left? Explain your answer using what you "
      "found in problem 4.")
story.append(KeepTogether(
    [Paragraph(p5, prob_style)]
    + diagram(board(8, 8, 0.40 * inch, shaded=True, removed=[(0, 0), (7, 7)]))
    + [workspace(2)]))
story.append(FrameBreak())

# P6 — the balance twist
p6 = ("<b>6.</b>&nbsp;&nbsp;This time two squares are removed &mdash; but "
      "<b>one is dark and one is light</b>, so the colors are balanced again. "
      "Does the covering work now? Try it on the board below, and say what the "
      "checkerboard coloring was really checking all along.")
story.append(KeepTogether(
    [Paragraph(p6, prob_style)]
    + diagram(board(4, 4, 0.42 * inch, shaded=True, removed=[(0, 0), (0, 3)]))
    + [workspace(2)]))

# --- Answer key ---
story.append(NextPageTemplate('single'))
story.append(PageBreak())

story.append(Paragraph("Answer Key &mdash; for parents", ans_h_style))
story.append(Paragraph(
    "<b>1.</b>&nbsp;&nbsp;<b>3 dominoes.</b> The board has 6 squares and each "
    "domino covers 2, so 6 &divide; 2 = 3. (Any full covering must split the "
    "squares into pairs.)", ans_style))
story.append(Paragraph(
    "<b>2.</b>&nbsp;&nbsp;<b>No.</b> Each domino covers 2 squares, so any board "
    "that can be covered must have an <b>even</b> number of squares. Nine is "
    "odd, so one square is always left stranded. <i>(This is the odd/even "
    "tool from Saturday Test No. 7.)</i>", ans_style))
story.append(Paragraph(
    "<b>3.</b>&nbsp;&nbsp;Every domino lands on <b>exactly one dark and one "
    "light</b> square. It always covers two neighbors, and on a checkerboard "
    "neighbors are always different colors &mdash; so this is true no matter "
    "where the domino goes.", ans_style))
story.append(Paragraph(
    "<b>4.</b>&nbsp;&nbsp;<b>No.</b> The two opposite corners are the same "
    "color (both dark), so removing them leaves <b>6 dark and 8 light</b> "
    "squares. But every domino needs one of each color &mdash; 6 dominoes use "
    "up the 6 dark squares, and 2 light squares are left with no partner. "
    "Impossible.", ans_style))
story.append(Paragraph(
    "<b>5.</b>&nbsp;&nbsp;<b>No.</b> Opposite corners of a chessboard share a "
    "color, so cutting them off leaves <b>30 of one color and 32 of the "
    "other</b>. Each of the 31 dominoes covers one of each color, which would "
    "need 31 and 31. The 2 extra squares of the majority color can never be "
    "covered. <i>(This is the classic &ldquo;mutilated chessboard.&rdquo;)</i>",
    ans_style))
story.append(Paragraph(
    "<b>6.</b>&nbsp;&nbsp;<b>Yes</b> &mdash; with one dark and one light square "
    "gone, the colors are balanced (7 and 7 on the 4&times;4), and the board "
    "can be covered. The coloring was never really about corners; it was "
    "checking whether <b>the dark and light counts stay equal</b>. If they "
    "don't, no covering can exist. <i>(In fact, on any chessboard, removing one "
    "dark and one light square always leaves something dominoes can cover.)</i>",
    ans_style))

doc.build(story)
print(f"Wrote {OUTPUT}")
