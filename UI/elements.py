# Modules
import PySimpleGUI as sg

from helpers import load_data
import UI.layout as layout


class Bowl(sg.Button):
	'''docstring for Bowl'''
	def __init__(self, b_id, balls):
		self.b_id = b_id

		if b_id == 6 or b_id == 13:
			self.balls = 0
			f_size = 70
			style = ('white', 'green')
		else:
			self.balls = balls
			f_size = 50
			style = None

		if b_id < 7:
			self.owner = 0
		else:
			self.owner = 1

		super().__init__(
			button_text=f' {self.balls} ',
			key=('bowl', self.b_id),
			font=('Helvetica', f_size),
			pad=(10, 10),
			disabled=True,
			disabled_button_color=style
		)

	def is_home(self):
		'''docstring for is_home'''
		return self.b_id == 6 or self.b_id == 13

	def pick_up(self):
		'''docstring for pick_up'''
		final = self.balls + self.b_id

		self.balls = 0
		self.update_bowl(True)

		return final

	def add_ball(self):
		'''docstring for modify'''
		self.balls += 1
		self.update_bowl(False)

	def update_bowl(self, state):
		'''docstring for update_bowl'''
		if self.balls < 10:
			text = f' {self.balls} '
		else:
			text = self.balls

		if self.balls == 0 or self.is_home():
			state = True

		self.update(text, disabled=state)


def create_window():
	'''docstring for GameWindow'''
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
	# window.Maximize()

	return window


def switch_layout(window, players):
	'''docstring for switch_layout'''
	text = load_data('gameplay')
	game_ui = layout.game_layout(players, text)
	window.extend_layout(window['-BASE-'], [[game_ui]])
	window.Finalize()
	window['-SETTINGS-'].hide_row()

	return window


def create_board(config):
	'''docstring for create_board'''
	board = [Bowl(b_id, config['balls']) for b_id in range(14)]

	return board


def popup_notice(cause, champion=None):
	'''docstring for notify'''
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
