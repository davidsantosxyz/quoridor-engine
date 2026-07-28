
def mesh_graph(side_length: int):
    num_vertices = side_length**2

    mesh = [[0] * num_vertices for _ in range(num_vertices)]

    for j in range(1,num_vertices):
        if j % side_length != 0:
            mesh[j][j-1] = 1
            mesh[j-1][j] = 1

    for j in range(side_length,num_vertices):
        mesh[j][j - side_length] = 1
        mesh[j - side_length][j] = 1

    return mesh

def mesh_coord_to_num(x, y, side_length: int) -> int:
    for var_name, var_value in (('x', x),('y', y)):
        if not 0 <= var_value < side_length:
            raise ValueError(f'{var_name} must be between {0} and {side_length - 1}')

    return x * side_length + y

