# Modules
import PySimpleGUI as sg


def base_layout(output):
	'''docstring for settings'''
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
	'''docstring for game'''
	board = [
		_col(players[0].home),
		_col([players[0].board[::-1], players[1].board]),
		_col(players[1].home)
	]

	final = [
		[sg.Text(output['placeholder'], key='-TURN-INFO-')],
		[sg.Text(output['instructions'])],
		board
	]

	return _col(final, col_id='-GAME-')


# Helper functions
def _col(content, align=None, col_id=None):
	'''docstring for col'''
	if type(content) != list:
		content = [[content]]

	c = sg.Column(
		content,
		element_justification='center',
		justification=align,
		key=col_id
	)
	return c


def _new_option(obj):
	'''docstring for new_option'''
	g_id = obj['id']
	text = [sg.Text(obj['text'])]

	options = [
		sg.Radio(ans[0], g_id, key=(g_id, ans[1]))
		for ans in obj['answers']
	]

	if g_id == 'p_1' or g_id == 'p_2':
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
