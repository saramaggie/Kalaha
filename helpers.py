
class EarlyCloseException(Exception):
	'''docstring for EarlyCloseException'''
	def __init__(self, location):
		self.location = location
		self.message = f'Window closed during {self.location}'

		super().__init__(self.message)
