# Modules
import PySimpleGUI as sg

# Program Files
from UI.elements import load_data
from helpers import EarlyCloseException


def play(window, board, players, gamer, first_round=False):
	'''docstring for main'''
	if first_round:
		gamer.disable_bowls(False)
		turn_text = load_data('gameplay', 'turn')

	while gamer.has_balls():

		window['-TURN-INFO-'].update(turn_text.format(gamer.p_id))

		event, values = window.read()

		if event == sg.WIN_CLOSED:
			# End game if window is closed
			raise EarlyCloseException('game')

		if gamer.human:
			choice = event
		else:
			choice = gamer.strategy

		last_bowl = move_balls(board, gamer, choice)

		if last_bowl != gamer.home.b_id:
			gamer = next_turn(players, gamer.index)

	return players


def next_turn(players, current):
	''' Doc '''
	next_up = (current + 1) % 2

	players[current].disable_bowls(True)
	players[next_up].disable_bowls(False)

	return players[next_up]


def move_balls(board, player, picked_bowl):
	'''docstring for drop_balls'''
	choice = int(picked_bowl[1])

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
