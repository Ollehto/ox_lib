import numpy as np


class OXGame:
	def __init__(self, state=0, player_first=False):
		self.__state = state
		self.__status = 0
		self.__player = 1 if player_first else 2
		self.__player_first = player_first

	def get_matrix(self):
		state = self.__state
		repr_array = np.empty(9, dtype=np.int8)
		for n in range(0, 8):
			new_state = state // (3**(8-n))
			repr_array[n] = new_state
			state -= new_state * (3**(8-n))

		repr_array[8] = state
		return repr_array.reshape((3, 3))

	def __repr__(self):
		return str(self.get_matrix())

	def __decide_win(self):##NEED FIX
		board_raw = self.get_matrix()
		for p in (1, 2):
			board = board_raw == p
			if np.any(np.all(board, axis=1)) or np.any(np.all(board, axis=0)) or np.all(board[(0, 1, 2), (0, 1, 2)]) or np.all(board[(2, 1, 0), (0, 1, 2)]):
				self.__status = p
		return self.__status

	def status(self):
		return self.__status

if __name__ == "__main__":
	ox = OXGame()
	print(ox)