from pipython import GCSDevice
from serial import Serial
from f import home, move, position, zero, read
import numpy as np
"""
Gets rotation and translation matrices
"""
increment = 0.4  # microns
start = -2000  # microns
stop = 2000  # microns

increment *= 10
start *= 10
stop *= 10

with GCSDevice() as pidevice:
    with Serial("/dev/ttyACM0", 115200) as ser:
        pidevice.ConnectRS232("/dev/ttyUSB0", 115200)
        home(pidevice)
        zero(ser)

        i0, i1, i2 = [], [], []
        n = start
        while n != stop:
            move(pidevice, [n/10000, 0, 0])

            i_reading = read(ser)
            i_reading = [i*1000 for i in i_reading]

            i0.append(i_reading[0])
            i1.append(i_reading[1])
            i2.append(i_reading[2])

            print(n)
            n += increment


def f(x, m, b):
    return m*x+b


ns = [i/10 for i in range(len(i0))]

i_list = [i0, i1, i2]
for i in i_list:
    m, b = np.polyfit(ns, i, 1)
    print(m, b)
    
    p, predict = 0, []
    while p != len(ns):
        n, j = ns[p], i[p]
        predict.append(f(n, m, b))
        p += 1

    corr_matrix = np.corrcoef(i, predict)
    corr = corr_matrix[0, 1]
    print(corr**2)
