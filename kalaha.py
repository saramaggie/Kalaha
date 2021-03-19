# Modules
import PySimpleGUI as sg
import random

# Program Files
import game
from helpers import EarlyCloseException
import UI.elements as ui
from classes import Player


def settings(window):
	''''''
	while True:
		event, values = window.read()

		if event == sg.WIN_CLOSED:
			# End game if window is closed
			raise EarlyCloseException('settings', window)

		formated_answers = {}
		for key in values:
			if values[key]:
				formated_answers[key[0]] = key[1]

		if len(formated_answers.keys()) != 4:
			ui.popup_notice('missing_answer')

		else:
			break

	return formated_answers


def setup_players(window, board, config):
	'''docstring for start'''

	# Create the players
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


def main():
	'''docstring for main'''

	window = ui.create_window()

	try:
		config = settings(window)
		board = ui.create_board(config)

		players, starter = setup_players(window, board, config)
		ui.switch_layout(window, players)

		game.play(window, board, players, starter, True)

	except EarlyCloseException:
		ui.popup_notice('early_close')

	else:
		champion = game.winner(players, config['start'])
		ui.popup_notice('winner', champion)

	finally:
		print('Closing')
		window.close()


if __name__ == '__main__':
	main()
