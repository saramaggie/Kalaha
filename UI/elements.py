# Modules
import PySimpleGUI as sg

from helpers import load_data
import UI.layout as layout


class Bowl(sg.Button):
	'''
	A button object representing a bowl

	Attributes
	----------
	balls : int
	    The ammount of balls set to start with.
	index : int
	    The position of the bowl relative to the board.
	owner : int
	    The index of the player that the bowl belongs to.
	'''
	def __init__(self, index, balls):
		self.index = index

		if index == 6 or index == 13:
			self.balls = 0
			f_size = 70
			style = ('white', 'green')
		else:
			self.balls = balls
			f_size = 50
			style = None

		if index < 7:
			self.owner = 0
		else:
			self.owner = 1

		super().__init__(
			button_text=f' {self.balls} ',
			key=('bowl', self.index),
			font=('Helvetica', f_size),
			pad=(10, 10),
			disabled=True,
			disabled_button_color=style
		)

	def is_home(self):
		'''A bowl is a "home" if it has an index of 6 (player 1) or 13 (player 2)

		Returns
		-------
		bool
		    True if home, False otherwise.
		'''
		return self.index == 6 or self.index == 13

	def pick_up(self):
		'''Method for calculating what bowls will recive the picked bowl's balls

		Returns
		-------
		int
		    The number of bowls that will recive a ball, starting at the bowl after this one.
		'''
		final = self.balls + self.index

		self.balls = 0
		self.update_bowl(True)

		return final

	def add_ball(self):
		'''
		Adds a ball to bowl.
		'''

		self.balls += 1
		self.update_bowl(False)

	def update_bowl(self, state):
		'''Update the text on the bowl as well as setting the state of the bowl.

		Parameters
		----------
		state : bool
		    If the bowl should be disabled or not
		'''
		if self.balls < 10:
			text = f' {self.balls} '
		else:
			text = self.balls

		if self.balls == 0 or self.is_home():
			state = True

		self.update(text, disabled=state)


def create_window():
	'''Creates the UI window

	Returns
	-------
	Obj
	    The created window object
	'''
	text = load_data('config')
	base_ui = layout.base_layout(text)

	window = sg.Window(
		'Kalaha',
		[[base_ui]],
		element_justification="center",
		font=('Helvetica', 20),
		finalize=True,
		resizable=True,
		use_ttk_buttons=True
	)
	window.Maximize()

	return window


def switch_layout(window, players):
	'''Switch between the layout of the settings-UI to the layout of the game itself.

	Parameters
	----------
	window : Object
	    The UI window
	players : List
	    The players

	Returns
	-------
	Object
	    The updated window
	'''
	text = load_data('gameplay')
	game_ui = layout.game_layout(players, text)
	window.extend_layout(window['-BASE-'], [[game_ui]])
	window.Finalize()
	window['-SETTINGS-'].hide_row()

	return window


def create_board(config):
	'''Create the bowls by adding them to a single list representing the gameboard.

	Parameters
	----------
	config : int
	    The number of balls to be added to the bowl

	Returns
	-------
	list
	    The created board
	'''
	board = [Bowl(index, config) for index in range(14)]

	return board


def popup_notice(cause, champion=None):
	'''Creator of popup-window

	Parameters
	----------
	cause : str
	    What popup should be shown.
	champion : None, optional
	    If it's the popup announsing the winnner the object of that player will then be passed here.
	'''
	msg = load_data('popout', cause)

	if cause == 'missing_answer':
		window_title = 'Missing option'
		button_text = 'Okay, okay...'

	elif cause == 'early_exit':
		window_title = 'Early exit'
		button_text = 'Byeeeeeee'

	elif cause == 'winner':
		window_title = 'Game over'
		button_text = 'Wohoooo!'
		msg = msg.format(champion.p_id, champion.score())

	sg.Popup(
		msg,
		title=window_title,
		custom_text=button_text,
		font=('Helvetica', 15)
	)
