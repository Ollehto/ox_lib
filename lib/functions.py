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
	if b0 is None:
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