# Modules
import PySimpleGUI as sg

# Program Files
from helpers import EarlyCloseException, load_data
import game_base as game
import UI.elements as ui


def settings(window):
	'''Event loop collecting user input from the configuration menu

	Parameters
	----------
	window : Object
	    The user-interface window

	Returns
	-------
	Dict
	    Configurations for numer of balls, whether or not the players are human, and starting player formated for interpretation by following functions

	Raises
	------
	EarlyCloseException
	    If the user closes the window this exception is raised
	'''

	while True:
		event, values = window.read()

		if event == sg.WIN_CLOSED:
			# End program if window is closed
			raise EarlyCloseException('settings')

		formated_answers = {}
		for key in values:
			if values[key]:
				formated_answers[key[0]] = key[1]

		if len(formated_answers.keys()) != 4:
			ui.popup_notice('missing_answer')

		else:
			break

	return formated_answers


def play_game(window, board, players, gamer):
	'''The actual game. Here user is looped through the different stages of the game until one player is out of balls or the window is closed.

	Parameters
	----------
	window : Object
	    The user-interface window
	board : list
	    One list containing all the individual bowls
	players : Object
	    The players, a list containing the two player objects
	gamer : list
	    The starting player

	Raises
	------
	EarlyCloseException
	    If the user closes the window this exception is raised
	'''

	gamer.disable_bowls(False)
	turn_text = load_data('gameplay', 'only_humans')

	while gamer.has_balls():
		if not gamer.human:
			choice = gamer.cpu_round()

		else:
			window['-TURN-INFO-'].update(turn_text.format(gamer.p_id))

			event, values = window.read()

			if event == sg.WIN_CLOSED:
				# End game if window is closed
				raise EarlyCloseException('game')

			choice = event[1]

		last_bowl = game.move_balls(board, gamer, choice)

		if last_bowl != gamer.home.index:
			gamer = game.next_turn(players, gamer.index)

	return


def main():
	'''
	Main function responsible for the overall program layout
	'''

	window = ui.create_window()

	try:
		config = settings(window)
		board = ui.create_board(config['balls'])

		players, starter = game.setup_players(board, config)
		ui.switch_layout(window, players)

		play_game(window, board, players, starter)

	except EarlyCloseException:
		ui.popup_notice('early_exit')

	else:
		champion = game.winner(players, config['start'])
		ui.popup_notice('winner', champion)

	finally:
		print('Closing')
		window.close()


if __name__ == '__main__':
	main()
