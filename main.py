from objects import *
import config

board = Board(config.BOARD_SIZE)

action = ''
while action != 'quit':
    board.print_board()
    action = input('Action:')


