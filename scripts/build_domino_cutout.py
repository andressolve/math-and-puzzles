"""Build the domino cut-out supplement for Practice Set No. 3, problem 1.

One sheet: a 2x3 board to cover, plus loose 1x2 paper dominoes to cut out.
No text on the figure page (per the cut-and-fold convention). Solid black
borders = cut. Same square size for board and tiles so the tiles fit.
"""

from reportlab.platypus import (
    SimpleDocTemplate, Spacer, Table, TableStyle,
)
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, Rect, Line
from reportlab.graphics import renderPDF
from reportlab.platypus.flowables import Flowable
from reportlab.lib.colors import HexColor, white, black

OUTPUT = "/Users/andresrodriguez/Documents/payday_tests/supplements/domino_cut_out.pdf"

SQ = 1.4 * inch
GRIDLINE = HexColor('#7a8a99')
TILE_FILL = HexColor('#eef2f5')

page_w, page_h = letter
left_m = right_m = 0.7 * inch
top_m = bot_m = 0.6 * inch


class Diagram(Flowable):
    def __init__(self, drawing):
        Flowable.__init__(self)
        self.drawing = drawing
        self.width = drawing.width
        self.height = drawing.height
        self.hAlign = 'CENTER'

    def draw(self):
        renderPDF.draw(self.drawing, self.canv, 0, 0)


def board_2x3():
    cols, rows, pad = 3, 2, 4
    w = cols * SQ + 2 * pad
    h = rows * SQ + 2 * pad
    d = Drawing(w, h)
    # outer cut border (solid)
    for c in range(cols):
        for r in range(rows):
            x = pad + c * SQ
            y = pad + r * SQ
            d.add(Rect(x, y, SQ, SQ, fillColor=white,
                       strokeColor=GRIDLINE, strokeWidth=0.9))
    d.add(Rect(pad, pad, cols * SQ, rows * SQ, fillColor=None,
              strokeColor=black, strokeWidth=1.6))
    return Diagram(d)


def domino_tile():
    pad = 4
    w = 2 * SQ + 2 * pad
    h = SQ + 2 * pad
    d = Drawing(w, h)
    d.add(Rect(pad, pad, 2 * SQ, SQ, fillColor=TILE_FILL,
               strokeColor=black, strokeWidth=1.6, rx=6, ry=6))
    # faint center divider so it reads as two squares
    d.add(Line(pad + SQ, pad + SQ * 0.18, pad + SQ, pad + SQ * 0.82,
               strokeColor=GRIDLINE, strokeWidth=0.8, strokeDashArray=[3, 3]))
    return Diagram(d)


doc = SimpleDocTemplate(OUTPUT, pagesize=letter,
                        leftMargin=left_m, rightMargin=right_m,
                        topMargin=top_m, bottomMargin=bot_m)

story = []
# the board to cover
story.append(board_2x3())
story.append(Spacer(1, 0.55 * inch))

# five dominoes to cut out (need 3; give extras), two per row
tiles = [[domino_tile(), domino_tile()],
         [domino_tile(), domino_tile()],
         [domino_tile(), None]]
t = Table(tiles, colWidths=[3.0 * inch, 3.0 * inch],
          hAlign='CENTER')
t.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
]))
story.append(t)

doc.build(story)
print(f"Wrote {OUTPUT}")
