# Modules
import json
import PySimpleGUI as sg

from classes import Bowl
import UI.layout as layout


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
	window.Maximize()

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


def popup_notice(cause, champion):
	'''docstring for notify'''
	msg = load_data('popout', cause)

	if cause == 'missing_answer':
		window_title = 'Missing option'
		button_text = 'Okay, okay...'

	elif cause == 'early_close':
		window_title = 'Early close'
		button_text = 'Byeeeeeee'

	elif cause == 'winner':
		window_title = 'Game over'
		button_text = 'Wohoooo!'
		msg = msg.format(champion.p_id, champion.score())

	sg.Popup(msg, title=window_title, custom_text=button_text)


def load_data(section, subsection=None):
	'''docstring for load_msg'''
	m_file = open('UI/data.json',)
	m_string = json.load(m_file)

	data = m_string[section]

	if subsection is not None:
		data = data[subsection]

	m_file.close()

	return data
