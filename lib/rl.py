import numpy as np
from . import functions
from . import ox

class OXAgent:
	def __init__(self):#, player_first=True):
		self.__ox = ox.OXGame()
		self.__all_boards = np.empty((3**9, 3, 3), dtype=np.int8)
		for s in np.arange(3**9):
			functions.get_board(s, self.__all_boards[s, :, :])

		self.__values = np.empty((3**9, 9), dtype=np.float)
		self.__values.fill(-100)
		self.__actions = np.zeros((3**9, 9), dtype=np.bool)
		for s in np.arange(3**9):
			empty_indices = functions.list_empty_indices(self.__all_boards[s])
			self.__actions[s, empty_indices] = True
			self.__values[s, empty_indices] = 0

		print("initialized")

	def play(self, loop=100, alpha=0.1, epsilon=0.05, gamma=0.9):
		for l in range(loop):
			while True:
				state = functions.get_state(self.__ox.get_board())
				if epsilon > np.random.rand():#exploratory
					actions = np.where(self.__actions[state, :])[0]
					action = np.random.choice(actions)
				else:
					action = np.argmax(self.__values[state, :])

				win = self.__ox.set(action)
				if win == 1:#win
					score = 1
				elif win == 2:#lose
					score = -1
				else:
					score = 0

				next_state = functions.get_state(self.__ox.get_board())
				optimal_future_value = np.max(self.__values[next_state, :])
 
				self.__values[state, action] += alpha * (score + gamma*optimal_future_value - self.__values[state, action])

				if win != 0:
					break

			self.__ox.reset()

		return self.__values

	def finish_learning(self):
		self.__ox.__init__(player_first=False, values=self.__values)
		self.set = self.__ox.set
		self.reset = self.__ox.reset

	def __repr__(self):
		return str(self.__ox)

if __name__ == "__main__":
	oxa = OXAgent()
	values = oxa.play(loop=20000, alpha=0.2, epsilon=0.1, gamma=0.95)
	print(values[res>-2])