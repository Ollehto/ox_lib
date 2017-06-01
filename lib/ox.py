import numpy as np
from . import functions
#import functions
class OXGame:
	def __init__(self, board=np.zeros((3, 3), dtype=np.int8), player_first=True, values=np.random.rand(3**9, 9)):
		self.__board = board
		self.__player_first = player_first
		self.__player = 1 if player_first else 2
		self.__values = values

		if not player_first:
			self.__computer_set()

		functions.decide_win(self.__board)

	def __repr__(self):
		return str(self.__board)

	def reset(self):
		self.__board.fill(0)
		if not self.__player_first:
			self.__computer_set()

	def __computer_set(self):
		state = functions.get_state(self.__board)
		flatind = np.argmax(self.__values[state, :])
		self.__board.ravel()[flatind] = 3 - self.__player
		return functions.decide_win(self.__board)

	def __player_set(self, place):
		if self.__board.ravel()[place] != 0:
			print(self.__board)
			print(place)
			raise Exception("Place already occupied")
		self.__board.ravel()[place] = self.__player
		return functions.decide_win(self.__board)

	def set(self, place):
		win = self.__player_set(place)
		if win != 0:
			return win
		cp_win = self.__computer_set()
		return cp_win

	def get_board(self):
		return self.__board