import numpy as np

BOARD_SIZE = 9
NUM_START_WALLS = 10


class Board:
    def __init__(self, board_size: int):
        self.board_size = board_size
        self.squares = np.array([[None] * board_size for _ in range(board_size)])
        self.lattice = np.array([[None] * (board_size - 1) for _ in range(board_size - 1)])
        self.pieces = []

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

    def add_pawn(
        self,
        pawn: Pawn,
        x: int,
        y: int,
    ):
        if not 0 <= x <= self.board_size - 1:
            raise ValueError(f'x must be between 0 and {self.board_size - 1}.')
        elif not 0 <= y <= self.board_size - 1:
            raise ValueError(f'y must be between 0 and {self.board_size - 1}.')
        elif pawn in self.pieces:
            raise ValueError(f'Pawn already on board.')

        self.pieces.append(pawn)
        self.squares[x][y] = pawn

    def move_pawn(
        self,
        pawn: Pawn,
        new_x: int,
        new_y: int
    ):
        self.squares[pawn.x][pawn.y] = None

        pawn.x = new_x
        pawn.y = new_y

        self.squares[pawn.x][pawn.y] = pawn

    def add_wall(
        self,
        wall: Wall,
        x: int,
        y: int,
        orientation: int
    ):
        wall.x = x
        wall.y = y
        wall.orientation = orientation
        wall.on_board = True

        self.lattice[x][y] = wall
        self.pieces.append(wall)


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
        orientaion: int | None = None,
        on_board: bool = False
    ):
        self.x = x
        self.y = y
        self.orientation = orientaion
        self.on_board = on_board


class Player:
    def __init__(
        self,
        pawn_x: int,
        pawn_y: int,
        pawn_color: str
    ):
        self.pawn = Pawn(pawn_x, pawn_y, pawn_color)
        self.walls = [Wall() for _ in range(NUM_START_WALLS)]


def check_wall_center_collision(lattice, new_wall_x, new_wall_y):
    return lattice[new_wall_x][new_wall_y] != None


def check_wall_adjacent_collision(lattice, new_wall_x, new_wall_y, new_wall_orientation):
    collisions = []

    for delta in [-1,1]:
        neighbor_x = new_wall_x * (1 - new_wall_orientation) + (new_wall_x +  delta) * new_wall_orientation
        neighbor_y = (new_wall_y + delta) * (1 - new_wall_orientation) + new_wall_y * new_wall_orientation

        if all(coord in range(lattice.shape[0]) for coord in [neighbor_x, neighbor_y]):
            neighbor = lattice[neighbor_x][neighbor_y]
        else:
            neighbor = None

        collisions.append(neighbor is not None and neighbor.orientation == new_wall_orientation)

    return any(collisions)


def check_wall_collision(lattice, new_wall_x, new_wall_y, new_wall_orientation):
    return check_wall_center_collision(lattice, new_wall_x, new_wall_y) or check_wall_adjacent_collision(lattice, new_wall_x, new_wall_y, new_wall_orientation)

