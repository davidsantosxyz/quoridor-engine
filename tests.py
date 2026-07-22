from main import *

board = Board(BOARD_SIZE)
player1 = Player(0,4,'white')
board.add_pawn(player1.pawn)
board.print_squares()
board.move_pawn(player1.pawn, 7,2)
board.print_squares()
board.move_pawn(player1.pawn, 0,0)
board.print_squares()
board.add_wall(Wall(),6,1,0)
board.print_lattice()
check_wall_collision(board.lattice, 6, 1, 1)

