import numpy as np

rotation_matrix = np.matrix([[0.9268337930691367, -0.24481893411313368, -0.015638000895517427],
                             [-0.2570753616619034, -0.9431084405282446, -0.0048695695435624995],
                             [0.05088689393646248, 0.05239877059828302, -1.0006244852156698]])

rotation_matrix_inverse = np.linalg.inv(rotation_matrix)

x = -0.12074320576816407
y = 0.1398779811425401
z = 0.006156405990016496

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


