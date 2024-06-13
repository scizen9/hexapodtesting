from pipython import GCSDevice
from serial import Serial
from f import home, move, position, zero, read
import matplotlib.pyplot as plt
import statistics
import numpy as np

with GCSDevice() as pidevice:
    with Serial("/dev/ttyACM0", 115200) as ser:
        pidevice.ConnectRS232("/dev/ttyUSB0", 115200)
        #move(pidevice, [-2, 0, 0])
        home(pidevice)
        zero(ser)

        n, ns, i0, i1, i2, temp = -20000, [], [], [], [], []
        while n != 20000:
            move(pidevice, [n/10000, 0, 0])
            #move(pidevice, [0, n/10000, 0])
            #move(pidevice, [0, 0, n/10000])
            i_reading = read(ser)
        
            i_reading = [i*1000 for i in i_reading]
            
            ns.append(n/10)
            i0.append(i_reading[0])
            i1.append(i_reading[1])
            i2.append(i_reading[2])
            temp.append(i_reading[1]/i_reading[0])
            print(n)
            n += 4


def f(x, m, b):
    return m*x


i_list = [i0, i1, i2]
for i in i_list:
    m, b = np.polyfit(ns, i, 1)
    print(m, b) 
    
    p, predict = 0, []
    while p != len(ns):
        n, j = ns[p], i[p]
        predict.append(f(n, m, b))
        p += 1

    #plt.scatter(ns, difference)
    corr_matrix = np.corrcoef(i, predict)
    corr = corr_matrix[0,1]
    print(corr**2)
plt.show()
for i in i_list:
    plt.plot(ns, i)
    plt.scatter(ns, i)
plt.show()
plt.plot(ns, temp, color="blue")
plt.title("Measured Y/X Ratio, 0.4 µm Increment")
plt.xlabel("Input Distance (µm)")
plt.ylabel("Output Y/X Ratio")	
plt.xlim(-2100, 2100)
plt.ylim(-0.4, -0.1)
plt.tight_layout()
plt.show()
