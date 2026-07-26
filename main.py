from objects import *
import config

board = Board(config.BOARD_SIZE)

player1 = Player(pawn_color='white')
board.add_pawn(player1.pawn, 8, 4)

player2 = Player(pawn_color='black')
board.add_pawn(player2.pawn, 0, 4)

action = ''
while action != 'quit':
    board.print_squares()
    board.print_lattice()
    action = input('Action:')


