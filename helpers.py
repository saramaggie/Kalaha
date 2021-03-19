# Modules
import json


class EarlyCloseException(Exception):
	'''
	Exception for if the user closes the window prematurely. Logging the from
	where the window was closed.
	'''
	def __init__(self, location):
		self.location = location
		self.message = f'Window closed during {self.location}'

		super().__init__(self.message)


def load_data(section, subsection=None):
	'''Load the text that is to be displayed on the UI

	Parameters
	----------
	section : string
	    Section for which the data is to be loaded
	subsection : string, optional
	    Subsection (if any) to avoid returning unnessesary data

	Returns
	-------
	TYPE
	    Depending on the section the return value is of different types, but what is returned is always the needed output data to display to the user.

	Raises
	------
	fnf_error
	    Description
	'''

	try:
		m_file = open('UI/data.json',)

	except FileNotFoundError as fnf_error:
		print('There is no UI/data.json. Did you missplace it?')
		raise fnf_error

	m_string = json.load(m_file)
	m_file.close()

	data = m_string[section]

	if subsection is not None:
		data = data[subsection]

	return data
