"""Practice Set — for Francisco. Builds practice_set_01.pdf.

6 problems, untimed. Focused on the balance-scale concept gap from
test #3 C7, scaffolded as: 3 outcomes -> 2 coins -> 3 coins -> 9 coins.
Bookended with a digit-rearrangement warm-up and a no-7 counting problem.
"""

from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, FrameBreak,
    Paragraph, Spacer, PageBreak, Table, TableStyle,
)
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import black, HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.graphics.shapes import Drawing, Line, Polygon, Circle

OUTPUT = "/Users/andresrodriguez/Documents/payday_tests/practice_sets/practice_set_01.pdf"

# Page geometry (letter)
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
body_style = ParagraphStyle('body', fontName='Times-Roman', fontSize=12.5,
                            leading=17, alignment=TA_LEFT)
hint_style = ParagraphStyle('hint', parent=body_style, fontSize=11.5,
                            textColor=HexColor('#555555'))
ans_style = ParagraphStyle('ans', fontName='Times-Roman', fontSize=11.5,
                           leading=15.5, alignment=TA_LEFT)
ans_h_style = ParagraphStyle('ansH', fontName='Times-Bold', fontSize=15,
                             leading=18, alignment=TA_LEFT, spaceAfter=8)


def header_table():
    data = [["Name __________________________", "Date ____________"]]
    t = Table(data, colWidths=[content_w*0.65, content_w*0.35])
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,-1), 11.5),
        ('TEXTCOLOR', (0,0), (-1,-1), HexColor('#333333')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    return t


def working_space(n_lines=5):
    return Spacer(1, 0.22 * inch * n_lines)


def balance_scale(width=2.0*inch):
    """Balance-scale icon, mirrored from test #3 for visual continuity."""
    pad = 0.1 * inch
    w = width
    h = 1.5 * inch
    d = Drawing(w + 2*pad, h + 2*pad)
    cx = pad + w/2
    base_y = pad + 0.05*inch
    fh = 0.65 * inch
    fw = 0.6 * inch
    d.add(Polygon([cx - fw/2, base_y,
                   cx + fw/2, base_y,
                   cx, base_y + fh],
                  strokeColor=black, strokeWidth=1.4, fillColor=HexColor('#dddddd')))
    d.add(Line(cx - 0.5*inch, base_y, cx + 0.5*inch, base_y,
               strokeColor=black, strokeWidth=1.6))
    beam_y = base_y + fh + 0.05*inch
    half_beam = 0.85 * inch
    d.add(Line(cx - half_beam, beam_y, cx + half_beam, beam_y,
               strokeColor=black, strokeWidth=1.6))
    string_h = 0.32 * inch
    for sx in (cx - half_beam, cx + half_beam):
        d.add(Line(sx, beam_y, sx - 0.18*inch, beam_y - string_h,
                   strokeColor=black, strokeWidth=0.9))
        d.add(Line(sx, beam_y, sx + 0.18*inch, beam_y - string_h,
                   strokeColor=black, strokeWidth=0.9))
    pan_y = beam_y - string_h
    pan_w = 0.5 * inch
    for px in (cx - half_beam, cx + half_beam):
        d.add(Polygon([px - pan_w, pan_y,
                       px + pan_w, pan_y,
                       px + pan_w*0.7, pan_y - 0.18*inch,
                       px - pan_w*0.7, pan_y - 0.18*inch],
                      strokeColor=black, strokeWidth=1.2, fillColor=HexColor('#f0f0f0')))
        d.add(Line(px - pan_w, pan_y, px + pan_w, pan_y,
                   strokeColor=black, strokeWidth=1.2))
    d.add(Circle(cx, beam_y, 0.045*inch, strokeColor=black,
                 strokeWidth=1.0, fillColor=black))
    return d


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

# Page 1 top: Title + subtitle + header + P1
story.append(Paragraph("Practice Set &mdash; for Francisco", title_style))
story.append(Paragraph(
    "A few puzzles. Take your time, show your work where it helps.",
    subtitle_style))
story.append(header_table())
story.append(Spacer(1, 0.22*inch))
story.append(Paragraph(
    "<b>1.</b>&nbsp;&nbsp;Using the digits <b>4, 7, 2, 9</b> each exactly once, "
    "write the largest 4-digit number you can make. Then write the smallest.",
    body_style))
story.append(Spacer(1, 0.20*inch))
story.append(Paragraph(
    "&nbsp;&nbsp;&nbsp;&nbsp;Largest: ____________ &nbsp;&nbsp;&nbsp;&nbsp;"
    "Smallest: ____________",
    body_style))
story.append(working_space(3))
story.append(FrameBreak())

# Page 1 bottom: balance icon + P2 (three outcomes)
story.append(centered(balance_scale(width=1.8*inch)))
story.append(Spacer(1, 0.04*inch))
story.append(Paragraph(
    "<b>2.</b>&nbsp;&nbsp;When you put coins on a balance scale, three different "
    "things can happen depending on what's on each side. List all three.",
    body_style))
story.append(Spacer(1, 0.10*inch))
story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;(a) ____________________________________", body_style))
story.append(Spacer(1, 0.06*inch))
story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;(b) ____________________________________", body_style))
story.append(Spacer(1, 0.06*inch))
story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;(c) ____________________________________", body_style))
story.append(FrameBreak())

# Page 2 top: P3 (2 coins)
story.append(Paragraph(
    "<b>3.</b>&nbsp;&nbsp;You have <b>2 coins</b>, and one of them is slightly "
    "heavier than the other. Using a balance scale, how can you find the heavy "
    "one in just <b>1 weighing</b>?",
    body_style))
story.append(working_space(6))
story.append(FrameBreak())

# Page 2 bottom: P4 (3 coins)
story.append(Paragraph(
    "<b>4.</b>&nbsp;&nbsp;Now you have <b>3 coins</b>, and one is slightly "
    "heavier than the others. Find the heavy coin in just <b>1 weighing</b>. "
    "Describe how.",
    body_style))
story.append(Spacer(1, 0.06*inch))
story.append(Paragraph(
    "<i>Hint: you don't have to put every coin on the scale.</i>",
    hint_style))
story.append(working_space(6))
story.append(FrameBreak())

# Page 3 top: P5 (9 coins)
story.append(Paragraph(
    "<b>5.</b>&nbsp;&nbsp;You have <b>9 coins</b>, and one is slightly heavier "
    "than the rest. Find the heavy coin in just <b>2 weighings</b>. Describe "
    "your strategy.",
    body_style))
story.append(Spacer(1, 0.06*inch))
story.append(Paragraph(
    "<i>Hint: think about what you just figured out in problem 4. "
    "Can you do it twice?</i>",
    hint_style))
story.append(working_space(7))
story.append(FrameBreak())

# Page 3 bottom: P6 (no 7s)
story.append(Paragraph(
    "<b>6.</b>&nbsp;&nbsp;How many 2-digit numbers contain <b>no 7</b> anywhere "
    "in them?",
    body_style))
story.append(working_space(8))
story.append(NextPageTemplate('single'))
story.append(PageBreak())

# Page 4: Answer key
story.append(Paragraph("Answer Key &mdash; for parents", ans_h_style))

story.append(Paragraph(
    "<b>1.</b>&nbsp;&nbsp;<b>Largest 9742, smallest 2479.</b> "
    "Biggest digit in the highest place for the largest; smallest digit first for the smallest.",
    ans_style))
story.append(Spacer(1, 0.08*inch))

story.append(Paragraph(
    "<b>2.</b>&nbsp;&nbsp;<b>The scale tilts left, tilts right, or balances.</b> "
    "Three outcomes \u2014 this is the key idea behind the rest of the coin problems. "
    "Each weighing gives you one of three answers, so each weighing can split a pile "
    "into three.",
    ans_style))
story.append(Spacer(1, 0.08*inch))

story.append(Paragraph(
    "<b>3.</b>&nbsp;&nbsp;<b>Put one coin on each side.</b> The heavy one is on "
    "the side that goes down. (Confidence builder.)",
    ans_style))
story.append(Spacer(1, 0.08*inch))

story.append(Paragraph(
    "<b>4.</b>&nbsp;&nbsp;<b>Weigh 1 coin against 1 coin, leave the third aside.</b> "
    "If the scale balances, the heavy coin is the one you set aside. "
    "If it tilts, the heavy coin is on the lower side. "
    "One weighing handles 3 coins because the scale has 3 outcomes (problem 2).",
    ans_style))
story.append(Spacer(1, 0.08*inch))

story.append(Paragraph(
    "<b>5.</b>&nbsp;&nbsp;<b>Split into 3 groups of 3.</b> "
    "<i>Weighing 1:</i> weigh group A against group B. If they balance, the heavy "
    "coin is in C; otherwise it's in the heavier of A or B. Now you have 3 suspect "
    "coins. <i>Weighing 2:</i> use the trick from problem 4 to find the heavy coin "
    "among those 3. Same trick, applied twice. With <i>n</i> weighings you can "
    "handle up to 3<super>n</super> coins.",
    ans_style))
story.append(Spacer(1, 0.08*inch))

story.append(Paragraph(
    "<b>6.</b>&nbsp;&nbsp;<b>72.</b> Tens digit can be 1\u20139 except 7 \u2014 8 choices. "
    "Units digit can be 0\u20139 except 7 \u2014 9 choices. 8 &times; 9 = 72. "
    "(Or: 90 two-digit numbers in total, minus 18 that contain a 7.)",
    ans_style))

doc.build(story)
print(f"Built: {OUTPUT}")
