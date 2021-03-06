# Modules
import random


class Player:
	'''Player object, to do things players do. Kind of self-explanatory, is it not?

	Attributes
	----------
	index : int
	    List index of player 0 (player 1) or 1 (player 2)
	p_id : int
	    Number of the player to be displayed
	human : bool
	    True if the player is human, otherwise false
	home : list
	    The bowl that is the home of the player.
	board : list
	    List containing the 6 bowls that belong to this player.
	is_starter : bool
	    False by default, set to True if player is configured to be the starting player by the user.
	strategy : str
	    Only set if the player is not human. For purpose of game it is set to strategy A by default. For the simulation it can be set to B.
	'''
	def __init__(self, index, human, bowls):
		self.index = index
		self.p_id = index + 1
		self.human = human
		self.home = bowls[-1]
		self.board = bowls[:6]
		self.is_starter = False

		if not human:
			self.strategy = 'A'

	def disable_bowls(self, toggle):
		'''Toggle bowl-availability.

		Parameters
		----------
		toggle : bool
			Whether or not the bowls on the player's board should be active or not
		'''

		[bowl.update_bowl(toggle) for bowl in self.board]

	def has_balls(self):
		'''Determines the player has any balls left in their bowls.

		Returns
		-------
		bool
		    True there are balls in any of the player's bowls, False otherwise.
		'''
		return self._ball_counter() != 0

	def score(self):
		''' Calculate final score for player

		Returns
		-------
		int
		    Total number of balls in bowls and home at end of game
		'''
		return self._ball_counter(True)

	def cpu_round(self):
		'''Gets result of the non-human players assigned strategy

		Returns
		-------
		int
		    Index of picked bowl generated by the player's strategy
		'''
		if self.strategy == 'A':
			picked_bowl = self._strategy_a()
		elif self.strategy == 'B':
			picked_bowl = self._strategy_b()

		return picked_bowl

	def _strategy_a(self):
		'''Select a non-empty bowl at random

		Returns
		-------
		int
		    Index of chosen bowl
		'''
		non_empty_bowls = [bowl for bowl in self.board if bowl.balls != 0]

		choice = random.randrange(len(non_empty_bowls))

		return non_empty_bowls[choice].index

	def _strategy_b(self):
		'''Select the bowl with the largest ball-count. If it results in more than one bowl, a random one of them is chosen.

		Returns
		-------
		int
		    Index of chosen bowl
		'''
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

		return most_balls[choice].index

	def _ball_counter(self, incl_home=False):
		'''
		Compute sum of balls in the players bowls. Home can be included, but
		isn't by default.
		
		Parameters
		----------
		incl_home : bool, optional
		    True if the home bowl is to be included in the sum. Otherwise False.
		
		Returns
		-------
		int
		    Sum of balls in the bowls belonging to player.
		'''
		count = sum([bowl.balls for bowl in self.board])

		if incl_home:
			count += self.home.balls
		return count


def setup_players(board, config):
	'''Creating the players based on provided configuration

	Parameters
	----------
	board : List
	    One list containing all the individual bowls
	config : Dict
	    The settings that were chosen on the configuration screen

	Returns
	-------
	List, Obj
	    List with created player objects as well as the object for the starting player
	'''

	players = [
		Player(0, config['p_1'], board[:7]),
		Player(1, config['p_2'], board[7:])
	]

	if config['start'] == 2:
		starter = players[random.randrange(2)]
	else:
		starter = players[config['start']]

	return players, starter


def next_turn(players, current):
	'''Get the next player and enable their board while disabling the board of previous player.

	Parameters
	----------
	players : list
	    The players, a list containing the two player objects
	current : int
	    Index of the player who just took their turn

	Returns
	-------
	object
	    Object of the player who is up next
	'''
	next_up = (current + 1) % 2

	players[current].disable_bowls(True)
	players[next_up].disable_bowls(False)

	return players[next_up]


def move_balls(board, player, picked_bowl):
	'''Move balls around the board

	Parameters
	----------
	board : List
	    One list containing all the individual bowls
	players : list
	    The players, a list containing the two player objects
	picked_bowl : int
	    Index of the chosen bowl

	Returns
	-------
	int
	    Index of the last bowl to receive an additional ball
	'''
	choice = int(picked_bowl)

	final = board[choice].pick_up()
	curr = choice + 1

	while curr <= final:
		# Reset down to 0 to start a new lap
		if curr > 13:
			curr -= 14
			final -= 14

		# Skip home of the opponent
		if board[curr].is_home() and (board[curr] is not player.home):
			curr += 1
			final += 1
		else:
			board[curr].add_ball()
			curr += 1

	return final


def winner(players, starter):
	'''Who won? The one with the larger score of course. If the players get the same score the player who didn't start wins.

	Parameters
	----------
	players : list
	    The players, a list containing the two player objects
	starter : int
	    Index of the starting player

	Returns
	-------
	Object
	    The winner
	'''
	scores = (players[0].score(), players[1].score())

	if scores[0] == scores[1]:
		non_starter = (starter + 1) % 2
		chicken_dinner = players[non_starter]
	else:
		highest = scores.index(max(scores))
		chicken_dinner = players[highest]

	return chicken_dinner
