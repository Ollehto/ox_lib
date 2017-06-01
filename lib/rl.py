import numpy as np


def get_board(state, b0=None):
	if b0 is None:
		repr_array = np.empty(9, dtype=np.int8)
	else:
		repr_array = b0.ravel()
	for n in range(0, 8):
		new_state = state // (3**(8-n))
		repr_array[8-n] = new_state
		state -= new_state * (3**(8-n))

	repr_array[0] = state
	return repr_array.reshape((3, 3))

def get_state(board):
	state = board.ravel().dot(np.power(3, np.arange(9)))
	return state

def decide_win(board):
	for p in (1, 2):
		board_bool = board == p
		if np.any(np.all(board_bool, axis=1)) or np.any(np.all(board_bool, axis=0)) or np.all(board_bool[(0, 1, 2), (0, 1, 2)]) or np.all(board_bool[(2, 1, 0), (0, 1, 2)]):
			return p
	if np.sum(board == 0) == 0:
		return -1
	else:
		return 0

def list_empty_indices(board):
	return np.where(board.ravel() == 0)[0]

class OXGame():
	def __init__(self, board=np.zeros((3, 3), dtype=np.int8), player_first=True):
		self.__board = board
		self.__player_first = player_first
		self.__player = 1 if player_first else 2

		if not player_first:
			self.computer_set()

		decide_win(self.__board)

	def __repr__(self):
		return str(self.__board)

	def reset(self):
		self.__board.fill(0)

	def __computer_set(self):
		flatind = np.random.choice(list_empty_indices(self.__board))# randomly choose from indices of cells where no o/x is placed
		self.__board.ravel()[flatind] = 3 - self.__player
		return decide_win(self.__board)

	def __player_set(self, place):
		if self.__board.ravel()[place] != 0:
			raise Exception("Place already occupied")
		self.__board.ravel()[place] = self.__player
		return decide_win(self.__board)

	def set(self, place):#returns 1 if player wins, -1 if loses, otherwise 0
		if self.__player_first:
			win = self.__player_set(place)
			if win != 0:
				return win
			cp_win = self.__computer_set()
			return cp_win
		else:
			cp_win = self.__computer_set()
			if cp_win != 0:
				return cp_win
			win = self.__player_set(place)
			return win

	def get_board(self):
		return self.__board

class OXAgent:
	def __init__(self):#, player_first=True):
		self.__ox = OXGame()
		self.__actions = np.zeros((3**9, 9), dtype=np.int8)
		self.__actions.fill(-1)
		self.__values = np.empty(3**9, dtype=np.float)
		self.__values.fill(0.5)

		board = np.empty((3, 3), dtype=np.int8)

		for s in np.arange(3**9):
			board = get_board(s, board)

			diff = np.sum(board == 1) - np.sum(board == 2)
			if diff == 0 or diff == 1:# if agent can place next
				win = decide_win(board)
				if win == 1:
					self.__values[s] = 1
				elif win == 2 or win == -1:
					self.__values[s] = 0

				empty_indices = list_empty_indices(board)
				for i, empty_index in enumerate(empty_indices):
					self.__actions[s, i] = empty_index

		self.__policy = np.empty(3**9, dtype=np.int8)

		for s in np.arange(3**9):
			board = get_board(s, board)
			if np.sum(board == 0) % 2 == 1:
				actions = self.__actions[s, :][self.__actions[s, :] >= 0]
				if actions.size != 0:
					self.__policy[s] = np.random.choice(actions)

		print("initialized")

	def play(self, loop=100, alpha=0.1, epsilon=0.05):
		for l in range(loop):
			while True:
				state = get_state(self.__ox.get_board())
				if epsilon > np.random.rand():#exploratory
					actions = self.__actions[state, :][self.__actions[state, :] >= 0]
					if actions.size != 0:
						self.__policy[state] = np.random.choice(actions)

				next_action = self.__policy[state]
				win = self.__ox.set(next_action)
				new_state = get_state(self.__ox.get_board())
 
				self.__values[state] += alpha * (self.__values[new_state] - self.__values[state])

				if win != 0:
					#print(self.__ox)
					#print(new_state)
					break

			self.__ox.reset()

		return self.__values

if __name__ == "__main__":
	oxa = OXAgent()
	print(oxa.play(loop=10000, alpha=0.8, epsilon=0.5))