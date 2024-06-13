from pipython import GCSDevice
from serial import Serial
from f import home, move, position, zero, read
import matplotlib.pyplot as plt
import statistics
import numpy as np


def f(x, factor):
    return -1/x+factor


with GCSDevice() as pidevice:
    with Serial("/dev/ttyACM0", 115200) as ser:
        pidevice.ConnectRS232("/dev/ttyUSB0", 115200)
        home(pidevice)
        zero(ser)
    
        r1, r2, a = [], [], []
        n = -5000
        while n != 5000:
            move(pidevice, [n/10000, 0, 0])
            i_reading = read(ser)
        
            i_reading = [i*1000 for i in i_reading]
            i0, i1, i2 = i_reading[0], i_reading[1], i_reading[2]
            try:
                r1.append(i1/i0)
                r2.append(i2/i0)
            except ZeroDivisionError:
                r1.append(None)
                r2.append(None)

            a.append(n/10)
            print(n)
            n += 100


r1temp = [i for i in r1 if i != None]
mean = statistics.mean(r1temp)
factor = -np.sin(np.pi/12)/np.cos(np.pi/12)

r1temp2 = []
for i in r1temp:
    if i*0.9 > factor:
        if i*1.1 < factor:
            r1temp2.append(i)

mean2 = statistics.mean(r1temp2)
print(mean)
print(mean2)

plt.plot(a, r1, color="blue", label="Data")
x = np.linspace(min(a), max(a), 1000)
#plt.plot(x, f(x, factor), color="orange", linestyle="dashed", label="-1/x-sin/cos")

#plt.plot(x, f(x, mean), color="green", linestyle="dashed", label="-1/x+Mean")
#plt.plot(x, g(x, median), color="red", linestyle="dashed", label="-1/x+Median")

plt.axhline(factor, color="orange", linestyle="dashed", label="Geometry -(sin15/cos15)")
plt.axhline(factor*0.9, color="green", linestyle="dashed", label="90% Lower Bound")
plt.axhline(factor*1.1, color="red", linestyle="dashed", label="110% Upper Bound")

plt.title("y/x Ratio, 10 µm X-Axis Input Increment")
plt.xlabel("Input Distance (µm)")
plt.ylabel("Output Ratio y/x (Unitless)")

plt.legend()
plt.tight_layout()
plt.show()

