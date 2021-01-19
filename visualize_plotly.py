import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

pallete = ['darkgreen', 'tomato', 'yellow', 'darkblue', 'darkviolet', 'indianred', 'yellowgreen', 'mediumblue', 'cyan',
           'black', 'indigo', 'pink', 'lime', 'sienna', 'plum', 'deepskyblue', 'forestgreen', 'fuchsia', 'brown',
           'turquoise', 'aliceblue', 'blueviolet', 'rosybrown', 'powderblue', 'lightblue', 'skyblue', 'lightskyblue',
           'steelblue', 'dodgerblue', 'lightslategray', 'lightslategrey', 'slategray',
           'slategrey', 'lightsteelblue', 'cornflowerblue', 'royalblue', 'ghostwhite', 'lavender',
           'midnightblue', 'navy', 'darkblue', 'blue', 'slateblue', 'darkslateblue',
           'mediumslateblue', 'mediumpurple', 'rebeccapurple', 'darkorchid',
           'darkviolet', 'mediumorchid']
color_pallete = ['lightcoral', 'firebrick', 'maroon', 'darkred', 'red',
                 'salmon', 'darksalmon', 'coral', 'orangered', 'lightsalmon', 'chocolate',
                 'saddlebrown',
                 'sandybrown', 'olive', 'olivedrab', 'darkolivegreen', 'greenyellow',
                 'chartreuse', 'lawngreen',
                 'darkseagreen', 'palegreen', 'lightgreen', 'limegreen',
                 'green', 'seagreen', 'mediumseagreen', 'springgreen', 'mediumspringgreen',
                 'mediumaquamarine', 'aquamarine', 'lightseagreen', 'mediumturquoise',
                 'lightcyan', 'paleturquoise', 'darkslategray', 'darkslategrey', 'teal', 'darkcyan', 'aqua', 'cyan',
                 'darkturquoise', 'cadetblue', 'thistle', 'violet', 'purple', 'darkmagenta',
                 'magenta', 'orchid', 'mediumvioletred', 'deeppink', 'hotpink', 'lavenderblush', 'palevioletred',
                 'crimson', 'lightpink']


def cube_data(position3d, size=(1, 1, 1)):
    # position3d - 3-list or array of shape (3,) that represents the point of coords (x, y, 0), where a bar is placed
    # size = a 3-tuple whose elements are used to scale a unit cube to get a paralelipipedic bar
    # returns - an array of shape(8,3) representing the 8 vertices of  a bar at position3d

    cube = np.array([[0, 0, 0],
                     [1, 0, 0],
                     [1, 1, 0],
                     [0, 1, 0],
                     [0, 0, 1],
                     [1, 0, 1],
                     [1, 1, 1],
                     [0, 1, 1]], dtype=float)  # the vertices of the unit cube

    cube *= np.asarray(size)  # scale the cube to get the vertices of a parallelipipedic bar
    cube += np.asarray(position3d)  # translate each  bar on the directio OP, with P=position3d
    return cube


def triangulate_cube_faces(positions, sizes=None):
    # positions - array of shape (N, 3) that contains all positions in the plane z=0, where a histogram bar is placed
    # sizes -  array of shape (N,3); each row represents the sizes to scale a unit cube to get a bar
    # returns the array of unique vertices, and the lists i, j, k to be used in instantiating the go.Mesh3d class

    if sizes is None:
        sizes = [(1, 1, 1)] * len(positions)
    else:
        if isinstance(sizes, (list, np.ndarray)) and len(sizes) != len(positions):
            raise ValueError('Your positions and sizes lists/arrays do not have the same length')

    all_cubes = [cube_data(pos, size) for pos, size in zip(positions, sizes) if size[2] != 0]
    p, q, r = np.array(all_cubes).shape

    # extract unique vertices from the list of all bar vertices
    vertices, ixr = np.unique(np.array(all_cubes).reshape(p * q, r), return_inverse=True, axis=0)
    # for each bar, derive the sublists of indices i, j, k assocated to its chosen  triangulation
    I = []
    J = []
    K = []

    for k in range(len(all_cubes)):
        I.extend(np.take(ixr, [8 * k, 8 * k + 2, 8 * k, 8 * k + 5, 8 * k, 8 * k + 7, 8 * k + 5, 8 * k + 2, 8 * k + 3,
                               8 * k + 6, 8 * k + 7, 8 * k + 5]))
        J.extend(np.take(ixr, [8 * k + 1, 8 * k + 3, 8 * k + 4, 8 * k + 1, 8 * k + 3, 8 * k + 4, 8 * k + 1, 8 * k + 6,
                               8 * k + 7, 8 * k + 2, 8 * k + 4, 8 * k + 6]))
        K.extend(np.take(ixr, [8 * k + 2, 8 * k, 8 * k + 5, 8 * k, 8 * k + 7, 8 * k, 8 * k + 2, 8 * k + 5, 8 * k + 6,
                               8 * k + 3, 8 * k + 5, 8 * k + 7]))

    return vertices, I, J, K  # triangulation vertices and I, J, K for mesh3d


def draw_solution(pieces):
    positions = []
    sizes = []
    colors = []
    sorted_size = []
    for each in pieces:
        positions.append(each[0:3])
        sizes.append(each[3:])
        sorted_size.append(set(each[3:]))

    colors = pallete[:len(positions)]
    color_index = [sorted_size, colors]
    vertices, I, J, K = triangulate_cube_faces(positions, sizes=sizes)

    X, Y, Z = vertices.T
    colors2 = [val for val in colors for _ in range(12)]
    mesh3d = go.Mesh3d(x=X, y=Y, z=Z, i=I, j=J, k=K, facecolor=colors2, flatshading=True)
    layout = go.Layout(width=650,
                       height=700,
                       title_text='Truck Loading True Solution',
                       title_x=0.5,
                       scene=dict(
                           camera_eye_x=-1.25,
                           camera_eye_y=1.25,
                           camera_eye_z=1.25)
                       )
    fig = go.Figure(data=[mesh3d], layout=layout)
    fig.show()
    return color_index


def draw(results, color_index):
    mesh = []
    clr = color_index[1]
    sorted_pieces = color_index[0]
    for pieces in results:
        positions = []
        sizes = []
        colors = []
        for each in pieces:
            positions.append(each[0:3])
            sizes.append(each[3:])
            for i in range(len(sorted_pieces)):
                if set(each[3:]) == sorted_pieces[i]:
                    colors.append(clr[i])

        vertices, I, J, K = triangulate_cube_faces(positions, sizes=sizes)

        X, Y, Z = vertices.T
        colors2 = [val for val in colors for _ in range(12)]
        mesh.append(go.Mesh3d(x=X, y=Y, z=Z, i=I, j=J, k=K, facecolor=colors2, flatshading=True))
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{'type': 'surface'}, {'type': 'surface'}],
               [{'type': 'surface'}, {'type': 'surface'}]])

    # Visualize 4 Rank 1 solutions

    fig.add_trace(mesh[0],
                  row=1, col=1)

    fig.add_trace(mesh[1],
                  row=1, col=2)

    fig.add_trace(mesh[2],
                  row=2, col=1)

    fig.add_trace(mesh[3],
                  row=2, col=2)


    fig.update_layout(
        title_text='Rank 1 Solutions',
        autosize=True,
        height=1500,
        width=1500,
        title_x=0.5,
        scene=dict(
            camera_eye_x=-1.25,
            camera_eye_y=1.25,
            camera_eye_z=1.25)

    )

    fig.show()
    return color_index
