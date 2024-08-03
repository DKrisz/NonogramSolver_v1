import numpy as np

from Utilities import Pos, Tabla


class Board:
	def __init__(self, tabla: Tabla, boardSize, clueColumns, clueRows) -> None:

		self.tabla = tabla
		self.boardSize = boardSize
		self.init_InputsToDisplay = False

		# Initialize Board with -1 (empty)
		self.board = np.full(self.boardSize ** 2, -1).reshape(self.boardSize, self.boardSize)

		self.inputColumns = clueColumns
		self.inputRows = clueRows
		self.tabla.DrawInputs(self.inputColumns, self.inputRows)

	def SetCellValue(self, col, row, value):
		self.board[row, col] = value

	def GetCellValue(self, col, row):
		return self.board[row, col]

	def GetColVector(self, idx):
		return self.board[:, idx]

	def GetRowVector(self, idx):
		return self.board[idx, :]

	def Display(self) -> None:
		for col in range(self.boardSize):
			for row in range(self.boardSize):
				p = Pos(col, row)
				value = self.GetCellValue(col, row)
				self.tabla.DrawCell(p, value)

		self.tabla.DrawGrid()

		if self.init_InputsToDisplay:
			self.tabla.DrawInputs(self.inputColumns, self.inputRows)
			self.init_InputsToDisplay = False
