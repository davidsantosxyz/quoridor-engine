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

        wall.x = x
        wall.y = y
        wall.orientation = orientation

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
        orientaion: Literal[0, 1] | None = None,
    ):
        self.x = x
        self.y = y
        self.orientation = orientaion


class Player:
    def __init__(
        self,
        pawn_x: int,
        pawn_y: int,
        pawn_color: str,
    ):
        self.pawn = Pawn(pawn_x, pawn_y, pawn_color)
        self.walls = [Wall() for _ in range(NUM_START_WALLS)]


def check_wall_center_collision(
    lattice,
    new_wall_x: int,
    new_wall_y: int,
) -> bool:
    return lattice[new_wall_x][new_wall_y] != None


def check_wall_adjacent_collision(
    lattice,
    new_wall_x: int,
    new_wall_y: int,
    new_wall_orientation: Literal[0, 1],
) -> bool:
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


def check_wall_collision(
    lattice,
    new_wall_x: int,
    new_wall_y: int,
    new_wall_orientation: Literal[0, 1],
) -> bool:
    return check_wall_center_collision(lattice, new_wall_x, new_wall_y) or check_wall_adjacent_collision(lattice, new_wall_x, new_wall_y, new_wall_orientation)

