import numpy as np

rotation_matrix = np.matrix([[0.9715077736492439, -0.23926970493915284, -0.0033034887845582064],
                             [-0.23953414062946243, -0.9721111762737883, -0.002855459496873518],
                             [-0.0029395936223349777, 0.0013029057764649252, -0.9990367898938869]])

hexapod_position = np.matrix([[0.712], [-0.334], [0.122]])
indicator_position = rotation_matrix * hexapod_position
print(indicator_position)

rotation_matrix_inverse = np.linalg.inv(rotation_matrix)
indicator_position = np.matrix([[-0.132], [-0.645], [0.092]])
hexapod_position = rotation_matrix_inverse * indicator_position
print(hexapod_position)
