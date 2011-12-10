#!/usr/bin/env python2

from bot import Bot
from board import Board

def run_test():
	board = Board()
	bot1 = Bot(1, board)
	bot2 = Bot(2, board)
	while not board.get_winner():
		print board
		if not board.can_be_played():
			break
		bot1.act()
		print board
		if not board.can_be_played():
			break
		bot2.act()
	
	print board
	bot1.update_strategy()
	bot2.update_strategy()
	print 'bot %d wins' % board.get_winner()

def main():
	test_number = 100
	while test_number:
		run_test()
		test_number -= 1

if __name__ == '__main__':
	main()

