# Modules
import random

# Program Files


class Player:
	'''docstring for Player'''
	def __init__(self, index, human, bowls):
		self.index = index
		self.p_id = index + 1
		self.human = human
		self.home = bowls[-1]
		self.board = bowls[:6]
		self.is_starter = False

		if not human:
			print('COMUUUTER')
			self.strategy = 'A'

	def disable_bowls(self, toggle):
		'''docstring for toggle_board'''
		[bowl.update_bowl(toggle) for bowl in self.board]

	def has_balls(self):
		'''docstring for has_balls'''
		return self._ball_counter() != 0

	def score(self):
		'''docstring for score'''
		return self._ball_counter(True)

	def cpu_round(self):
		'''docstring for cpu_round'''
		if self.strategy == 'A':
			picked_bowl = self._strategy_a()
		elif self.strategy == 'B':
			picked_bowl = self._strategy_b()

		return picked_bowl

	def _strategy_a(self):
		'''docstring for _strategy_a'''
		non_empty_bowls = [bowl for bowl in self.board if bowl.balls != 0]

		choice = random.randrange(len(non_empty_bowls))

		return non_empty_bowls[choice].b_id

	def _strategy_b(self):
		'''docstring for _strategy_b'''
		most_balls = []
		max_ball_count = 0

		for bowl in self.board:
			if bowl.balls > max_ball_count:
				most_balls = [bowl]
				max_ball_count = bowl.balls

			elif bowl.balls == max_ball_count:
				most_balls.append(bowl)

		if len(most_balls) > 1:
			choice = random.randrange(len(most_balls))
		else:
			choice = 0

		return most_balls[choice].b_id

	def _ball_counter(self, incl_home=False):
		'''docstring for count_balls'''
		count = sum([bowl.balls for bowl in self.board])

		if incl_home:
			count += self.home.balls
		return count


def setup_players(board, config):
	''' Creating the players based on provided configuration

	:param      board:   One list containing the individual bowls
	:type       board:   List
	:param      config:  The settings that were chosen on the configuration screen
	:type       config:  Dict - 'balls','p_1','p_2','start'

	:returns:   List with created player objects as well as the object for the starting player
	:rtype:     List, Obj
	'''

	players = [
		Player(0, config['p_1'], board[:7]),
		Player(1, config['p_2'], board[7:])
	]

	[print(bowl.b_id) for bowl in players[0].board]

	if config['start'] == 2:
		starter = players[random.randrange(2)]
	else:
		starter = players[config['start']]

	return players, starter


def next_turn(players, current):
	''' Doc '''
	next_up = (current + 1) % 2

	players[current].disable_bowls(True)
	players[next_up].disable_bowls(False)

	return players[next_up]


def move_balls(board, player, picked_bowl):
	'''docstring for drop_balls'''
	choice = int(picked_bowl)

	final = board[choice].pick_up()
	curr = choice + 1

	while curr <= final:
		if curr > 13:
			curr -= 14
			final -= 14

		if board[curr].is_home() and (board[curr] is not player.home):
			curr += 1
			final += 1
		else:
			board[curr].add_ball()
			curr += 1

	return final


def winner(players, starter):
	'''docstring for winner'''
	scores = (players[0].score(), players[1].score())

	if scores[0] == scores[1]:
		non_starter = (starter + 1) % 2
		return players[non_starter]
	else:
		highest = scores.index(max(scores))
		return players[highest]
