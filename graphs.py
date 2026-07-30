from copy import deepcopy

def _validate_greater_than_zero(input_value: int | float, var_name: str) -> None:
    if input_value <= 0:
        raise ValueError(f'{var_name} must be grater than 0, but {input_value} was given')

def mesh_graph(side_length: int):
    _validate_greater_than_zero(side_length, 'side_length')

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
    _validate_greater_than_zero(side_length, 'side_length')

    for var_name, var_value in (('x', x),('y', y)):
        if not 0 <= var_value < side_length:
            raise ValueError(f'{var_name} must be between {0} and {side_length - 1}')

    return x * side_length + y

def cuts_to_adj_entries(cuts, mesh_side: int):
    _validate_greater_than_zero(mesh_side, 'mesh_side')

    entries = []

    for cut in cuts:
        coord_x = mesh_coord_to_num(cut[0][0], cut[0][1], mesh_side)
        coord_y = mesh_coord_to_num(cut[1][0], cut[1][1], mesh_side)
        entry = (coord_x, coord_y)

        entries.append(entry)

    return entries
        
def remove_edges(adj_matrix, entries):
    adj_matrix = deepcopy(adj_matrix)

    for cut in entries:
        adj_matrix[cut[0]][cut[1]] = 0
        adj_matrix[cut[1]][cut[0]] = 0

    return adj_matrix

def find_connected_component(v: int, adj, l = []) -> list:
    l.append(v)

    neighbors = [ind for ind, edge in enumerate(adj[v]) if edge == 1]
    paths = [i for i in neighbors if i not in l]
    for i in paths:
        find_connected_component(i, adj, l)

    return l
