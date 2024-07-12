import numpy as np

rotation_matrix = np.matrix([[0.9268337930691367, -0.24481893411313363, -0.01563800089551743],
                             [-0.2570753616619034, -0.9431084405282446, -0.0048695695435624995],
                             [0.05088689393646248, 0.052398770598283025, -1.00062448521567]])

rotation_matrix_inverse = np.linalg.inv(rotation_matrix)

x = np.mean([-0.212645590682196, -0.053410981697171456, -0.09617304492512481])
y = np.mean([0.1454242928452578, 0.1292845257903492, 0.14492512479201325])
z = np.mean([0.009983361064891848, 0.0028286189683860027, 0.005657237936771649])

translation_vector = np.matrix([[x/1000],
                                [y/1000],
                                [z/1000]])


def hexapod_to_indicator(vector):
    vector = np.matrix([[i] for i in vector])
    indicator = rotation_matrix*vector+translation_vector
    indicator = indicator.tolist()
    return sum(indicator, [])


def indicator_to_hexapod(vector):
    vector = np.matrix([[i] for i in vector])
    hexapod = rotation_matrix_inverse*(vector-translation_vector)
    hexapod = hexapod.tolist()
    return sum(hexapod, [])


