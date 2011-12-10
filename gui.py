#!/usr/bin/env python2

import gtk
from board import Board
from bot import Bot

class App(gtk.Window):
	def __init__(self):
		super(App, self).__init__()

		self.set_title('Tic-Tac-Toe')
		self.connect('destroy', gtk.main_quit)
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_default_size(250,250)
		self.show()

		self.init_widgets()
		self.game_count = 0
		self.start_new_game()
	
	def init_widgets(self):
		vbox = gtk.VBox()
		self.add(vbox)
		
		self.button_position = {}
		self.buttons = {}

		for i in xrange(3):
			hbox = gtk.HBox()
			vbox.add(hbox)
			for j in xrange(3):
				button = gtk.Button()
				self.button_position[button] = (i,j)
				hbox.add(button)
				button.connect('clicked', self.game_button_clicked)
				button.show()
				self.buttons[i, j] = button
			hbox.show()

		hbox = gtk.HBox()

		restart_button = gtk.Button('restart')
		restart_button.connect('clicked', self.start_new_game)
		restart_button.show()
		hbox.add(restart_button)
		
		self.score_label= gtk.Label('0 - 0')
		self.score_label.show()
		hbox.add(self.score_label)

		vbox.add(hbox)
		hbox.show()

		vbox.show()
	
	def draw_board_state(self):
		for i in xrange(3):
			for j in xrange(3):
				button = self.buttons[i,j]
				if self.board.board[i][j] == 0:
					label = '  '
				elif self.board.board[i][j] == 1:
					label = 'X'
				else:
					label = '0'
				button.set_label(label)
				
	def start_new_game(self, widget=None):
		for button in self.button_position:
			button.set_label(' ')

		self.board = Board()

		if self.game_count % 2 == 0:
			self.bot = Bot(1, self.board)
			self.bot.act()
			self.draw_board_state()
			self.player_color = 2
		else:
			self.bot = Bot(2, self.board)
			self.player_color = 1

		self.game_count += 1

	def game_button_clicked(self, button):
		position = self.button_position[button]

		if position not in self.board.get_possible_actions():
			return

		self.board.move(self.player_color, self.button_position[button]) 
		self.draw_board_state()
		
		if not self.board.can_be_played():
			return

		self.bot.act()
		self.draw_board_state()

		if not self.board.get_winner() != 0:
			return

if __name__ == '__main__':
	App()
	gtk.main()
