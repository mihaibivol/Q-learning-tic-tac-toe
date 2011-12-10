import json
import random

REWARD = {1 : 100,
          2 : -100,
          0 : -3}

class Bot(object):
	def __init__(self, color, board):
		self.board = board
		self.color = color
		self.load_strategy()
		self.moves = []

	def get_strategy_color(self, board_color):
		if board_color == self.color:
			return 1
		elif board_color == 0:
			return 0
		else:
			return 2

	def get_state_from_board(self):
		state = 0
		for i in xrange(3):
			for j in xrange(3):
				strategy_color = self.get_strategy_color(self.board.get_color((i, j)))
				state = state * 10 + strategy_color

		return state

	def load_strategy(self):
		
		self.strategy = {}

		try:
			fd = open('strategy.json', 'r')
		except IOError:
			return

		self.strategy = json.load(fd)
		fd.close()

	def act(self):
		state = self.get_state_from_board()
		possible_actions = self.board.get_possible_actions()
		# don't know where to move
		move = None

		if state in self.strategy:
			# move in the place with highest score
			action = max(self.strategy[state], key = lambda a : a['score'])
			if action['score'] > 0:
				move = tuple(action['move'])
			else:
				# if actions have negative score, remove them from possible actions
				for act in self.strategy[state]:
					if tuple(act['move']) in possible_actions:
						possible_actions.remove(act['move'])
			if len(possible_actions) == 0:
				move = tuple(action['move'])
		
		if move == None:
			move = random.choice(possible_actions)

		self.moves.append((state, move))
		self.board.move(self.color, move)
	
	def update_strategy(self):
			strategy_color = self.get_strategy_color(self.board.get_winner())
			score = REWARD[strategy_color]
			self.load_strategy()
			strategy = self.strategy
			
			self.moves.reverse()

			for move in self.moves:
				state = move[0]
				action = move[1]

				# search in strategy for old score
				# if not found old score is 0

				if state in strategy:
					for act in strategy[state]:
						if act['move'] == action:
							old_score = action['score']
							# if update always remove from strategy
							strategy.remove(act)
							break
					else:
						old_score = 0
				else:
					old_score = 0

				score = old_score + 0.8 * (0.9 * score - old_score - 10)
				if state not in strategy:
					strategy[state] = []

				strategy[state].append({'move' : action,
				                        'score' : score})

			fd = open('strategy.json', 'w')
			json.dump(strategy, fd)
			fd.close()

