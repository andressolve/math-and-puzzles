"""Build a single-page quiet grid paper PDF — letter, 1/4" squares, light gray."""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

OUTPUT = "/Users/andresrodriguez/Documents/payday_tests/supplements/grid_paper.pdf"

page_w, page_h = letter
margin = 0.5 * inch
sq = 0.25 * inch  # 1/4" squares

line_color = HexColor('#BFC4CC')  # quiet, cool gray
line_w = 0.35

c = canvas.Canvas(OUTPUT, pagesize=letter)
c.setStrokeColor(line_color)
c.setLineWidth(line_w)

# Vertical lines — start at left margin, step by sq, stop at right margin
x = margin
while x <= page_w - margin + 0.01:
    c.line(x, margin, x, page_h - margin)
    x += sq

# Horizontal lines
y = margin
while y <= page_h - margin + 0.01:
    c.line(margin, y, page_w - margin, y)
    y += sq

c.showPage()
c.save()
print(f"Wrote {OUTPUT}")
