#!/usr/bin/env python3

from Utilities import *
from Vector import VectorProcessing

DEBUG = False


class SolveBoard:
	def __init__(self, board) -> None:
		self.board = board
		self.boardSize = board.boardSize
		self.stat = Statistics(self.boardSize)

		self.markSureCells()
		self.markSureBlanks()

		# self.board.Display()

		vp = VectorProcessing(board)
		vp.InitializeAllVectorsFromBoard()
		vp.InitializeAllSubVectors()

		vp.ProcessOneClues()

		vp.PrintVectors()

	def markSureBlanks(self):
		# Process Columns
		for idx in range(self.boardSize):
			self._processVectorForSureBlankCells(self.board.inputColumns[idx], self.boardSize, columnNumber=idx)
			self._processVectorForSureBlankCells(self.board.inputRows[idx], self.boardSize, rowNumber=idx)

	def _processVectorForSureBlankCells(self, clueVector, size, columnNumber=None, rowNumber=None):
		countSegments = len(clueVector)
		totalSegmentLength = sum(clueVector) + countSegments - 1
		if size == totalSegmentLength:
			idx = 0
			for i in range(len(clueVector) - 1):
				idx += clueVector[i]
				if columnNumber is not None:
					self.board.SetCellValue(columnNumber, idx, 0)
				else:
					self.board.SetCellValue(idx, rowNumber, 0)
				idx += 1

	def markSureCells(self):
		for idx in range(self.boardSize):
			self._processVectorForSureCells(self.board.inputColumns[idx], self.boardSize, columnNumber=idx)
			self._processVectorForSureCells(self.board.inputRows[idx], self.boardSize, rowNumber=idx)

	def _processVectorForSureCells(self, clueVector, size, columnNumber=None, rowNumber=None):
		countSegments = len(clueVector)
		totalMinSegmentLength = sum(clueVector) + countSegments - 1
		tail_MinSegmentLength = size - totalMinSegmentLength

		if totalMinSegmentLength >= (size // 2 + 1) and self.HaveProcessableSegment(
				clueVector, tail_MinSegmentLength
		):
			idx: int = 0

			for segment in clueVector:
				if segment <= tail_MinSegmentLength:
					idx += segment + 1
				else:
					idx += tail_MinSegmentLength

					for _ in range(segment - tail_MinSegmentLength):
						if columnNumber is not None:
							self.board.SetCellValue(columnNumber, idx, 1)
						else:
							self.board.SetCellValue(idx, rowNumber, 1)
						idx += 1
					if idx < size:
						idx += 1

	@staticmethod
	def HaveProcessableSegment(clueVector, tail_MinSegmentLength):
		for segment in clueVector:
			if segment > tail_MinSegmentLength:
				return True
		return False
