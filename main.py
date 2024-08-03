#!/usr/bin/env python3

import turtle

from BoardClasses import Board

# from input_1 import *
# from input_2 import *
from input_3 import *
# from input_4 import *

from Settings import DRAW_FRAME, DRAWING_SPEED, DRAWING_TRACE
from SolveBoard import SolveBoard
from Utilities import Ablak, Tabla


def Main():
	boardSize = BOARD_SIZE
	speed = DRAWING_SPEED
	trace = DRAWING_TRACE
	frame = DRAW_FRAME

	scrn = Ablak(boardSize, trace).GetScreen()
	tabla = Tabla(boardSize, frame, speed)
	scrn.update()

	board = Board(tabla, boardSize, INPUT_COLS, INPUT_ROWS)
	SolveBoard(board)

	board.Display()

	turtle.mainloop()


if __name__ == '__main__':
	Main()
	print('--- FINISHED ---')
