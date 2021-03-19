# Modules
import json


class EarlyCloseException(Exception):
	'''docstring for EarlyCloseException'''
	def __init__(self, location):
		self.location = location
		self.message = f'Window closed during {self.location}'

		super().__init__(self.message)


def load_data(section, subsection=None):
	'''docstring for load_msg'''
	m_file = open('UI/data.json',)
	m_string = json.load(m_file)

	data = m_string[section]

	if subsection is not None:
		data = data[subsection]

	m_file.close()

	return data
