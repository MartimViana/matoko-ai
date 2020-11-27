from action import *

class Helper():
	def __init__(self, name, action):
		self.name = name
		self.action = action

	def interpret(self, str):
		# split input by a sequence of words
		words = str.split(' ')
		# Perform action according to str
		for a in self.action:
			# if str matches action input, execute action
			if a.match(words):
				a.run(words)
				break

	def greet(self):
		print('Hello! Im '+self.name+'!')

	def goodbye(self):
		print('Bye bye!')

	def getInput(self):
		return input('> ')

	def help(self):
		for a in self.action:
			print('\t* '+a.getInput())

	def start(self):
		while True:
			input = self.getInput()
			if input == 'exit': break
			elif input == 'help': self.help()
			else: self.interpret(input)
		self.goodbye()