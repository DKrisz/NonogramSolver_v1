import re

DEFAULT_LENGTH = -1


class Vector:
	def __init__(self, length=DEFAULT_LENGTH, parent=None, data='', start_idx=-1, end_idx=-1, column=True):
		self.parent = parent
		if length == DEFAULT_LENGTH:
			self.length = end_idx - start_idx
			self.data = data
		elif length:
			self.length = length
			self.data = data or '.' * self.length
		else:
			self.data = ''

		self.start_idx = start_idx if start_idx >= 0 else 0
		self.end_idx = end_idx if end_idx >= 0 else self.start_idx + length
		self.children: list[Vector] = []
		self.open = True
		self.column = column
		self.subVLengths = []

	def AddSubVector(self, newVector) -> None:
		self.children.append(newVector)
		self.UpdateSubVLengths()

	def UpdateSubVLengths(self):
		for child in self.children:
			self.subVLengths.append(child.length)


class VectorProcessing:
	converter_board2vector = {-1: '.', 0: 'X', 1: 'O'}
	converter_vector2board = {'.': -1, 'X': 0, 'O': 1}

	def __init__(self, board):
		self.board = board
		self.boardSize = self.board.boardSize

		self.columnVectors = [Vector(self.boardSize, column=True) for _ in range(self.boardSize)]
		self.rowVectors = [Vector(self.boardSize, column=False) for _ in range(self.boardSize)]

		self.regex_subVector = re.compile(r'[O.]*', flags=re.DOTALL)

	@classmethod
	def _convertBoardVectorItemValue(cls, item):
		return cls.converter_board2vector[item]

	def GetBoardVectorData(self, currentBoardVector):
		out = ''
		for i in range(len(currentBoardVector)):
			out += self._convertBoardVectorItemValue(currentBoardVector[i])
		return out

	def InitializeAllVectorsFromBoard(self):
		for idx in range(self.boardSize):
			self.columnVectors[idx].data = self.GetBoardVectorData(self.board.board[:, idx])
			self.rowVectors[idx].data = self.GetBoardVectorData(self.board.board[idx, :])

	def InitializeAllSubVectors(self):
		for idx in range(self.boardSize):
			self.AddSubVectors(self.columnVectors[idx])
			self.AddSubVectors(self.rowVectors[idx])

	# _ = input('Press <ENTER> to continue')

	def AddSubVectors(self, parentVector):
		matches = self.regex_subVector.finditer(parentVector.data)
		for match in matches:
			if match.end() > match.start():
				parentVector.AddSubVector(
						Vector(
								length=DEFAULT_LENGTH, parent=parentVector, data=match.group(),
								start_idx=match.start(),
								end_idx=match.end(),
								column=parentVector.column
						)
				)

	def PrintVectors(self):
		# print('\nCOLUMNS:\n')
		# for i, v in enumerate(self.columnVectors):
		# 	print(f'Column {i}: {v.data}')
		print('\nROWS:\n')
		for i, v in enumerate(self.rowVectors):
			print(f'Row {i}: {v.data} | Sub-vectors: {self.GetSubVectorsOfVector(v, returnType="str")}')

	@staticmethod
	def GetSubVectorsOfVector(parentVector: Vector, returnType: str = 'str') -> str | list[str] | list[Vector]:
		"""
		Return given vector's sub-vectors in various formats: string, list of strings, or list of Vectors

		:param parentVector: Vector containing the sub-vectors
		:param returnType: Specify return type: 'str': string; 'list': list of strings; 'obj': list of Vectors
		:return: str | list[str] | list[Vector] based on returnType parameter
		"""

		if returnType == 'str':
			out = ''
			for child in parentVector.children:
				out += f'{child.data} | '
			return out[:-3]

		if returnType == 'list':
			out = []
			for child in parentVector.children:
				out.append(child.data)
			return out

		if returnType == 'obj':
			out = []
			for child in parentVector.children:
				out.append(child)
			return out

	def ProcessOneClues(self):
		for idx in range(self.boardSize):
			if len(self.board.inputColumns[idx]) == 1:
				print(f'Column: {idx} | Clue: {self.board.inputColumns[idx]}')
				self._processOneClueVector(self.columnVectors[idx], self.board.inputColumns[idx])

		for idx in range(self.boardSize):
			if len(self.board.inputRows[idx]) == 1:
				print(f'Row: {idx} | Clue: {self.board.inputRows[idx]}')

	def _processOneClueVector(self, parentVector, clue):
		subVs: list[Vector] = self.GetSubVectorsOfVector(parentVector, returnType='obj')
		countOfSubVs = len(subVs)

		if countOfSubVs == 1 and subVs[0].length == clue:
			self.FillSubVector(subVs[0], 'O')

	def FillSubVector(self, subV, value):
		self._FillSubV(subV, value)
		self._CopySubVToParentVector(subV)
		self._copyVectorToBoard(subV.parent)

	def _FillSubV(self, subV, value):
		pass

	def _CopySubVToParentVector(self, subV):
		pass

	def _copyVectorToBoard(self, vector):
		pass
