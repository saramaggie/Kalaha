# Modules
import PySimpleGUI as sg


class Player:
	'''docstring for Player'''
	def __init__(self, index, human, bowls):
		self.index = index
		self.p_id = index + 1
		self.human = human
		self.home = bowls[-1]
		self.board = bowls[:6]
		self.is_starter = False

	@property
	def strategy(self):
		'''docstring for strategy'''
		return self._strategy

	@strategy.setter
	def strategy(self, ):

		pass

	# @property
	def score(self):
		'''docstring for score'''
		self._score = self._ball_counter(True)
		return self._score

	def disable_bowls(self, toggle):
		'''docstring for toggle_board'''
		[bowl.update_bowl(toggle) for bowl in self.board]

	def has_balls(self):
		'''docstring for has_balls'''
		return self._ball_counter() != 0

	def _ball_counter(self, incl_home=False):
		'''docstring for count_balls'''
		count = sum([bowl.balls for bowl in self.board])

		if incl_home:
			count += self.home.balls
		return count


class Bowl(sg.Button):
	'''docstring for Bowl'''
	def __init__(self, b_id, balls):
		self.b_id = b_id

		if b_id == 6 or b_id == 13:
			self.balls = 0
			style = ('white', 'green')
		else:
			self.balls = balls
			style = None

		if b_id < 7:
			self.owner = 0
		else:
			self.owner = 1

		super().__init__(
			button_text=f' {self.balls} ',
			key=('bowl', self.b_id),
			font=('Helvetica', 50),
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
