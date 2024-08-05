import turtle

from Settings import (
	CELL_PADDING, CELL_SURE_NO, CELL_SURE_YES,
	COLOR_BLACK, COLOR_BLUE, COLOR_WHITE
)


class SearchStatus:
	def __init__(self):
		self.out = []
		self.item_id = -1
		self.anchored = True
		self.itemFound = False
		self.item_length = 0
		self.item_start = 0
		self.item_dirty = False


class Statistics:
	def __init__(self, size):
		self.TotalCellCount = size * size
		self.TotalCell_Filled = 0
		self.RemainingCell_Filled = 0


class ReportFind:
	def __init__(self):
		self.start_idx = 0
		self.length = 0
		self.is_dirty = False


class RC:
	def __init__(self):
		self.column = 0
		self.idx = 0
		self.type = None
		self.length = 0
		self.hasItem = False


class Pos:
	# x: column
	# y: col
	def __init__(self, x, y, offset=(0.0, 0.0)):
		self.x = 0.0
		self.y = 0.0
		# offset = 0.0

		self._x = x - offset[0]
		self._y = y - offset[1]

		self._transform()

	def _transform(self):
		transformation = (1.0, -1.0)
		self.x = self._x * transformation[0]
		self.y = self._y * transformation[1]


class Tabla(turtle.Turtle):
	def __init__(self, size, frame: bool = False, speed: int = 0) -> None:
		super(Tabla, self).__init__()

		# General settings
		self._size = size
		self._speed = speed

		self.speed(self._speed)
		self.hideturtle()
		self.penup()

		if frame:
			self.DrawFrame()

	def DrawInputs(self, columns, rows):
		p_start_H = Pos(0.5, -0.1)
		p_start_V = Pos(-0.1, 0.7)
		offset_H = (1.0, 0.0)
		offset_V = (0.0, 1.0)
		textAttrib = FontAttribs('Calibri Light', 20, 'normal')

		self._writeClueTexts('col', p_start_H, offset_H, columns, textAttrib)
		self._writeClueTexts('row', p_start_V, offset_V, rows, textAttrib)

	def _writeClueTexts(self, what, startP, offset, clueTexts, textAttrib):
		if what == 'col':
			sep = '\n'
			alignment = 'center'
		else:
			sep = ' '
			alignment = 'right'
		self.penup()
		for idx in range(self._size):
			self.setposition((startP.x + offset[0] * idx, startP.y - offset[1] * idx))
			out = sep.join([str(x) for x in clueTexts[idx]])
			self.write(out, align=alignment, font=textAttrib.GetFontInfo())

	def DrawFrame(self):
		self.pencolor('#dddddd')
		grid = {
			'x1': -1.0,
			'y1': 1.0,
			'x2': self._size + 1.0,
			'y2': (self._size + 1) * -1.0
		}
		self.pu()
		self.goto(grid['x1'], grid['y1'])
		self.pd()
		self.goto(grid['x1'], grid['y2'])
		self.goto(grid['x2'], grid['y2'])
		self.goto(grid['x2'], grid['y1'])
		self.goto(grid['x1'], grid['y1'])
		self.pencolor('#000000')

	def DrawGrid(self) -> None:
		self.pencolor('#000000')

		x1 = 0.0
		y1 = 0.0
		x2 = float(self._size)
		y2 = float(self._size) * - 1.0

		# Vertical grid lines
		for x in range(self._size + 1):
			self.SetPenSize(x)

			# col = float(x)
			self.penup()
			self.goto(x1 + x, y1)
			self.pendown()
			self.goto(x1 + x, y2)

		# Horizontal grid lines
		for y in range(self._size + 1):
			self.SetPenSize(y)

			# row = float(y)
			self.penup()
			self.goto(x1, y1 - y)
			self.pendown()
			self.goto(x2, y1 - y)

		self.pu()

	def SetPenSize(self, index: int) -> None:
		if (index % 5) == 0:
			self.pensize(3)
		else:
			self.pensize(0)

	def DrawCell(self, pos: Pos, value) -> None:
		if value == CELL_SURE_NO:
			self._DrawCell_False(pos)
		elif value == CELL_SURE_YES:
			self._DrawCell_True(pos)
		else:
			self._DrawCell_None(pos)

	def _DrawCell_False(self, pos: Pos) -> None:
		cellPadding = CELL_PADDING

		self.pu()
		self.pensize(0)
		self.setposition((pos.x + cellPadding, pos.y - cellPadding))
		self.pd()
		self.goto(pos.x + 1.0 - cellPadding, pos.y - 1.0 + cellPadding)
		self.pu()
		self.setposition((pos.x + cellPadding, pos.y - 1.0 + cellPadding))
		self.pd()
		self.goto(pos.x + 1.0 - cellPadding, pos.y - cellPadding)
		self.pu()

	def _DrawCell_True(self, pos: Pos) -> None:
		self._drawSquare(pos=pos, fillColor=COLOR_BLUE, penColor=COLOR_BLACK)

	def _DrawCell_None(self, pos: Pos) -> None:
		self._drawSquare(pos=pos, fillColor=COLOR_WHITE, penColor=COLOR_BLACK)

	def _drawSquare(self, pos: Pos, fillColor: str, penColor: str):
		shape = (
			(pos.x, pos.y - 1.0),
			(pos.x + 1.0, pos.y - 1.0),
			(pos.x + 1.0, pos.y),
			(pos.x, pos.y)
		)

		self.pu()
		self.pensize(0)
		self.pencolor(penColor)
		self.setposition((pos.x, pos.y))
		self.fillcolor(fillColor)
		self.begin_fill()
		self.pd()

		for x, y in shape:
			self.goto(x, y)
		self.end_fill()


class Ablak:
	def __init__(self, size, trace: bool = False) -> None:
		self._size = size
		self._trace = trace
		margin = 3.0

		self._scrn = turtle.Screen()
		self._scrn.title('Nonogram Solver')
		self._scrn.mode('world')
		self._scrn.setworldcoordinates(
				llx=-margin,
				lly=(self._size + margin) * -1,
				urx=self._size + margin,
				ury=margin
		)

		# parent._scrn.setup(width=0.6, height=0.6, startx=-0.0, starty=0.0)
		self._scrn.tracer(self._trace)

	def GetScreen(self) -> turtle.Screen:
		return self._scrn


class FontAttribs:
	fontFace: str
	fontSize: int
	fontWeight: str

	def __init__(self, fontFace='', fontSize=12, fontWeight='normal'):
		self.fontFace = fontFace
		self.fontSize = fontSize
		self.fontWeight = fontWeight

	def GetFontInfo(self):
		return self.fontFace, self.fontSize, self.fontWeight
