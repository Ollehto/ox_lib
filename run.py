from lib.rl import *

if __name__ == "__main__":
	#LEARN
	print("learning")
	oxa = OXAgent()
	values = oxa.play(loop=20000, alpha=0.7, epsilon=0.5, gamma=0.95)
	oxa.finish_learning()

	#PLAY
	while True:
		print("now play")
		win = 0
		while win == 0:
			print(oxa)
			try:
				place = int(input(">"))
				if place < 0 or place > 8:
					print("Input Invalid Out of Range")
					continue
				win = oxa.set(place)
			except Exception as inst:
				print(inst)
				continue
		print("win = "+str(win))
		print(oxa)
		yn = input("play again?(y/n) > ")
		if yn == 'y':
			oxa.reset()
		else:
			break