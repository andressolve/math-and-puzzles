"""Build Practice Set No. 2 — Counting with Overlaps."""

from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, FrameBreak,
    Paragraph, Spacer, PageBreak,
)
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUTPUT = "/Users/andresrodriguez/Documents/payday_tests/practice_set_02.pdf"

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
sub_q_style = ParagraphStyle('subq', fontName='Times-Roman', fontSize=12,
                             leading=16, alignment=TA_LEFT,
                             leftIndent=0.3 * inch, spaceAfter=2)
wrap_style = ParagraphStyle('wrap', fontName='Times-Italic', fontSize=11.5,
                            leading=15, alignment=TA_LEFT, spaceBefore=6,
                            spaceAfter=2)
ans_h_style = ParagraphStyle('ah', fontName='Times-Bold', fontSize=16,
                             leading=20, alignment=TA_LEFT, spaceAfter=10)
ans_style = ParagraphStyle('ans', fontName='Times-Roman', fontSize=11,
                           leading=15, alignment=TA_LEFT, spaceAfter=10)


def workspace(n):
    return Spacer(1, 0.22 * inch * n)


story = []

# Title block + framing + P1
story.append(Paragraph("Practice Set No. 2", title_style))
story.append(Paragraph("Counting with Overlaps", sub_style))
story.append(Paragraph(
    "Each problem is about groups that share something. "
    "Notice what happens when groups overlap.", frame_line_style))

# P1 — disjoint warm-up
p1 = ("<b>1.</b>&nbsp;&nbsp;Twenty kids are on the playground. "
      "Eight of them are on the slide, five are on the swings, and "
      "nobody is on both at the same time. How many kids are doing "
      "one of those two things? How many are doing neither?")
story.append(Paragraph(p1, prob_style))
story.append(workspace(5))
story.append(FrameBreak())

# P2 — concrete overlap with a name list
p2_stem = ("<b>2.</b>&nbsp;&nbsp;Five friends &mdash; <b>Ana, Beto, Carla, "
           "Diego,</b> and <b>Elena</b> &mdash; filled out a survey.")
p2_lists = ("&nbsp;&nbsp;&nbsp;&nbsp;Dog-lovers: <i>Ana, Beto, Carla.</i><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Cat-lovers: <i>Ana, Beto, Diego, Elena.</i>")
story.append(Paragraph(p2_stem, prob_style))
story.append(Spacer(1, 0.06 * inch))
story.append(Paragraph(p2_lists, prob_style))
story.append(Spacer(1, 0.10 * inch))
story.append(Paragraph("(a)&nbsp;&nbsp;Who likes <b>both</b> dogs and cats?",
                       sub_q_style))
story.append(workspace(2))
story.append(Paragraph("(b)&nbsp;&nbsp;How many friends like dogs <b>or</b> "
                       "cats (or both)?", sub_q_style))
story.append(workspace(2))
story.append(Paragraph("(c)&nbsp;&nbsp;Does 3 + 4 give the answer to (b)? "
                       "If not, why not?", sub_q_style))
story.append(workspace(2))
story.append(FrameBreak())

# P3 — generalize
p3 = ("<b>3.</b>&nbsp;&nbsp;In a club of 10 kids, 6 like soccer and 5 like "
      "swimming. 3 of them like both. How many kids like at least one of "
      "the two sports? <i>(Use what you noticed in problem 2.)</i>")
story.append(Paragraph(p3, prob_style))
story.append(workspace(6))
story.append(FrameBreak())

# P4 — neither
p4 = ("<b>4.</b>&nbsp;&nbsp;The same club of 10 kids as in problem 3. "
      "How many of them like neither soccer nor swimming?")
story.append(Paragraph(p4, prob_style))
story.append(workspace(6))
story.append(FrameBreak())

# P5 — work backwards
p5 = ("<b>5.</b>&nbsp;&nbsp;In a group of 12 kids, 7 like cookies and 6 like "
      "cake. 11 of them like at least one of the two. How many kids like "
      "<b>both</b>?")
story.append(Paragraph(p5, prob_style))
story.append(workspace(6))
story.append(FrameBreak())

# P6 — revisit (cousin of test problem)
p6 = ("<b>6.</b>&nbsp;&nbsp;In a class of 25 students, 15 like pizza, 10 "
      "like ice cream, and 6 like both. How many students like neither "
      "pizza nor ice cream?")
story.append(Paragraph(p6, prob_style))
story.append(workspace(6))

# Answer key on its own page
story.append(NextPageTemplate('single'))
story.append(PageBreak())

story.append(Paragraph("Answer Key &mdash; for parents", ans_h_style))
story.append(Paragraph(
    "<b>1.</b>&nbsp;&nbsp;Doing one of them: 8 + 5 = <b>13</b> kids "
    "(since no one is on both, simple addition works). Doing neither: "
    "20 &minus; 13 = <b>7</b> kids.", ans_style))
story.append(Paragraph(
    "<b>2.</b>&nbsp;&nbsp;(a) <b>Ana</b> and <b>Beto</b> appear on both "
    "lists. (b) The friends who like dogs or cats (or both) are "
    "Ana, Beto, Carla, Diego, Elena &mdash; all <b>5</b>. "
    "(c) <b>No.</b> 3 + 4 = 7, but the answer is 5. Ana and Beto each got "
    "counted twice (once as dog-lovers, once as cat-lovers). The "
    "double-counted amount is 2 &mdash; exactly the number who like both. "
    "<i>(This is the key insight: 7 &minus; 2 = 5.)</i>", ans_style))
story.append(Paragraph(
    "<b>3.</b>&nbsp;&nbsp;Adding 6 + 5 = 11 double-counts the 3 kids who "
    "like both, so subtract them: 6 + 5 &minus; 3 = <b>8</b> kids like at "
    "least one sport.", ans_style))
story.append(Paragraph(
    "<b>4.</b>&nbsp;&nbsp;Total kids minus those who like at least one: "
    "10 &minus; 8 = <b>2</b> kids like neither.", ans_style))
story.append(Paragraph(
    "<b>5.</b>&nbsp;&nbsp;7 + 6 = 13, but only 11 kids like at least one. "
    "The 2 extras are kids counted twice &mdash; the ones who like both. "
    "So <b>2</b> kids like both. <i>(Same rule, rearranged: "
    "both = liked-cookies + liked-cake &minus; liked-at-least-one.)</i>",
    ans_style))
story.append(Paragraph(
    "<b>6.</b>&nbsp;&nbsp;Liking pizza or ice cream (or both): "
    "15 + 10 &minus; 6 = 19. Liking neither: 25 &minus; 19 = <b>6</b> "
    "students. <i>(This is the same shape as Saturday Test No. 4, "
    "problem 6.)</i>", ans_style))

doc.build(story)
print(f"Wrote {OUTPUT}")
