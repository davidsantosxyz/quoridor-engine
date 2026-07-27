
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

