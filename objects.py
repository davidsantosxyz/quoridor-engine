import numpy as np
import config


class Board:
    def __init__(self, board_size: int):
        self.board_size = board_size
        self.squares = np.array([[None] * board_size for _ in range(board_size)])

        self.lattice_size = board_size - 1
        self.lattice = np.array([[None] * self.lattice_size for _ in range(self.lattice_size)])
        
        self.canvas_size = 2*self.board_size - 1
        self.canvas = [[config.EMPTY_SYMBOL] * self.canvas_size for _ in range(self.canvas_size)]

        self.pieces = []

        self.player_white = Player(*config.WHITE_STARTING_COORDS,config.WHITE_PAWN_SYMBOL)
        self.player_black = Player(*config.BLACK_STARTING_COORDS,config.BLACK_PAWN_SYMBOL)
        self.add_pawn(self.player_white.pawn,self.player_white.pawn.x,self.player_white.pawn.y)
        self.add_pawn(self.player_black.pawn,self.player_black.pawn.x,self.player_black.pawn.y)

    def print_squares(self):
        for row in self.squares:
            print(row)

    def print_lattice(self):
        for row in self.lattice:
            for dot in row:
                if isinstance(dot, Wall):
                    print(dot.orientation, end=' ')
                else:
                    print('.', end=' ')

            print()
        
    def paint_squares(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                square = self.squares[i][j]

                if square is not None:
                    self.canvas[2*i][2*j] = square.color

    def paint_wall(
        self,
        x: int,
        y: int,
        orientation: Literal[0, 1],
    ):
        for delta in [-1,0,1]:
            if orientation == 0:
                self.canvas[x][y + delta] = config.HORIZONTAL_WALL_SYMBOL
            else:
                self.canvas[x + delta][y] = config.VERTICAL_WALL_SYMBOL

    def paint_lattice(self):
        for i in range(self.board_size - 1):
            for j in range(self.board_size - 1):
                point = self.lattice[i][j]

                if point is not None: 
                    self.paint_wall(2*i+1, 2*j+1, point.orientation)

    def print_board(self):
        self.paint_squares()
        self.paint_lattice()

        i = j = -1
        for row in self.canvas:
            i += 1

            for cell in row:
                j += 1

                if cell == config.HORIZONTAL_WALL_SYMBOL:
                    print(cell, end = cell)
                elif cell == config.EMPTY_SYMBOL and i % 2 == 0 and j % 2 == 0:
                    print(config.SQUARE_SYMBOL, end = config.EMPTY_SYMBOL)
                else:
                    print(cell, end=config.EMPTY_SYMBOL)

            print()

    def validate_coordinates(
        self,
        x: int,
        y: int,
        on: Literal["squares", "lattice"],
    ) -> None:
        offset = {"squares": 0, "lattice": 1}[on]
        limit = self.board_size - offset

        if not 0 <= x < limit:
            raise ValueError(f"x must be between 0 and {limit - 1}")
        if not 0 <= y < limit:
            raise ValueError(f"y must be between 0 and {limit - 1}")

    def validate_square_empty(
        self,
        x: int,
        y: int
    ) -> None:
        if self.squares[x][y] is not None:
            raise ValueError("Square is already occupied")

    def validate_point_empty(
        self,
        x: int,
        y: int,
    ) -> None:
        if self.lattice[x][y] is not None:
            raise ValueError("Point is already occupied")

    def validate_piece_outside(self, piece) -> None:
        if piece in self.pieces:
            raise ValueError(f'Piece already on board')

    def add_pawn(
        self,
        pawn: Pawn,
        x: int,
        y: int,
    ) -> None:
        self.validate_coordinates(x, y, on = 'squares')
        self.validate_piece_outside(pawn)
        self.validate_square_empty(x, y)

        pawn.x = x
        pawn.y = y

        self.pieces.append(pawn)
        self.squares[x][y] = pawn

    def move_pawn(
        self,
        pawn: Pawn,
        new_x: int,
        new_y: int
    ) -> None:
        self.validate_coordinates(new_x,new_y, on = 'squares')
        self.validate_square_empty(new_x, new_y)

        self.squares[pawn.x][pawn.y] = None

        pawn.x = new_x
        pawn.y = new_y

        self.squares[new_x][new_y] = pawn

    def add_wall(
        self,
        wall: Wall,
        x: int,
        y: int,
        orientation: Literal[0, 1]
    ) -> None:
        self.validate_coordinates(x, y, on = 'lattice')
        self.validate_piece_outside(wall)
        self.validate_point_empty(x, y)
        if check_wall_collision(self.lattice, x, y, orientation):
            raise ValueError('Wall collision')


        wall.x = x
        wall.y = y
        wall.orientation = orientation

        self.lattice[x][y] = wall
        self.pieces.append(wall)
        
    def find_cuts(self):
        cuts = []

        for piece in self.pieces:
            if isinstance(piece,Wall):
                first_origin = (piece.x, piece.y) 
                first_destin = (
                    piece.x + (1 - piece.orientation),
                    piece.y + piece.orientation
                )
                first_cut = (first_origin, first_destin)
                cuts.append(first_cut)

                second_origin = (
                    piece.x + piece.orientation,
                    piece.y + (1 - piece.orientation)
                ) 
                second_destin = (
                    piece.x + 1,
                    piece.y + 1
                )
                second_cut = (second_origin, second_destin)
                cuts.append(second_cut)

        return cuts


class Pawn:
    def __init__(
        self,
        x: int | None = None,
        y: int | None = None,
        color: str | None = None
    ):
        self.x = x
        self.y = y
        self.color = color


class Wall:
    def __init__(
        self,
        x: int | None = None ,
        y: int | None = None,
        orientaion: Literal[0, 1] | None = None,
    ):
        self.x = x
        self.y = y
        self.orientation = orientaion


class Player:
    def __init__(
        self,
        pawn_x: int | None = None,
        pawn_y: int | None = None,
        pawn_symbol: str | None = None,
    ):
        self.pawn = Pawn(pawn_x, pawn_y, pawn_symbol)
        self.walls = [Wall() for _ in range(config.NUM_START_WALLS)]


def check_wall_collision(
    lattice,
    new_wall_x: int,
    new_wall_y: int,
    new_wall_orientation: Literal[0, 1],
) -> bool:
    collisions = []

    for delta in [-1,1]:
        neighbor_x = new_wall_x * (1 - new_wall_orientation) + (new_wall_x +  delta) * new_wall_orientation
        neighbor_y = (new_wall_y + delta) * (1 - new_wall_orientation) + new_wall_y * new_wall_orientation

        if all(0 <= coord < lattice.shape[0] for coord in [neighbor_x, neighbor_y]):
            neighbor = lattice[neighbor_x][neighbor_y]
        else:
            neighbor = None

        collisions.append(neighbor is not None and neighbor.orientation == new_wall_orientation)

    return any(collisions)

