# Modules
import PySimpleGUI as sg


def base_layout(output):
	'''
	The definition of the layout of the settings/base page (SEE PDF REFERENCE
	for info on how PySimpleGUI works)

	:param      output:  The different texts that is to be displayed on the
	                     settings UI
	:type       output:  dict

	:returns:   The outer column containing the settings layout
	:rtype:     column object
	'''
	settings = [
		[sg.Text(output['instructions'])],
		[_divider('h')],
		[_new_option(output['balls'])],
		[_divider('h')],
		[_col([
			[sg.Text(output['human'])],
			[_divider('h')],
			[
				_new_option(output['p_1']),
				_divider('v'),
				_new_option(output['p_2'])
			]
		])],
		[_divider('h')],
		[_new_option(output['start'])],
		[_col(sg.Submit('Play'), 'right')]
	]

	base = _col(settings, col_id='-SETTINGS-')

	return _col(base, col_id='-BASE-')


def game_layout(players, output):
	'''
	docstring for game

	:param      players:  The players
	:type       players:  List of the two player objects
	:param      output:   The different texts that is to be displayed on the
	                      game UI
	:type       output:   dict

	:rtype:     column object
	:returns:   The column containing the board and the text elements combined
	'''
	board = [
		_col(players[0].home),
		_col([players[0].board[::-1], players[1].board]),
		_col(players[1].home)
	]

	compleate = [
		[sg.Text(output['placeholder'], key='-TURN-INFO-')],
		[sg.Text(output['instructions'])],
		board
	]

	return _col(compleate, col_id='-GAME-')


# Helper functions

def _col(content, align=None, col_id=None):
	'''
	Helper function. To declutter the code when creating columns in layouts.

	:param      content:  The content
	:type       content:  { type_description }
	:param      align:    The align
	:type       align:    { type_description }
	:param      col_id:   The col identifier
	:type       col_id:   { type_description }

	:returns:   { description_of_the_return_value }
	:rtype:     { return_type_description }
	'''
	if type(content) != list:
		content = [[content]]

	c = sg.Column(
		content,
		element_justification='center',
		justification=align,
		key=col_id
	)
	return c


def _new_option(option):
	'''
	Helper function. To declutter the code when creating new single-choice options

	:param      option:  The option
	:type       option:  { type_description }

	:returns:   { description_of_the_return_value }
	:rtype:     { return_type_description }
	'''
	group_id = option['id']
	text = [sg.Text(option['text'])]

	options = [
		sg.Radio(answr[0], group_id, key=(group_id, answr[1]))
		for answr in option['answers']
	]

	if group_id == 'p_1' or group_id == 'p_2':
		return _col([text, options])
	else:
		return _col([text + options])


def _divider(direction, line_color='#283B5B'):
	'''docstring for _divider'''
	if direction == 'h':
		line = sg.HorizontalSeparator(color=line_color)
	else:
		line = sg.VerticalSeparator(color=line_color)

	return line


def _text_h(content, text_id=None):
	'''docstring for _text_head'''
	pass


def _text_p(content, text_id=None):
	'''docstring for _text_head'''
	pass
