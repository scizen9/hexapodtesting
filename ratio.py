from pipython import GCSDevice
from serial import Serial
from f import home, move, position, zero, read
import matplotlib.pyplot as plt
import statistics
import numpy as np
"""
Shows X/Y Ratio Trend
"""
axis = "x'"
increment = 10  # microns
start = -500  # microns
stop = 500  # microns

increment *= 10
start *= 10
stop *= 10

with GCSDevice() as pidevice:
    with Serial("/dev/ttyACM0", 115200) as ser:
        pidevice.ConnectRS232("/dev/ttyUSB0", 115200)
        home(pidevice)
        zero(ser)
    
        ratio = []
        n = start
        while n != stop+increment:
            move(pidevice, [n/10000, 0, 0])
            reading = read(ser)
        
            reading = [i*1000 for i in reading]
            i0, i1, i2 = reading[0], reading[1], reading[2]
            try:
                ratio.append(i1/i0)
            except ZeroDivisionError:
                ratio.append(None)

            print(n)
            n += increment


ns = [i/10 for i in range(len(ratio))]
ratio_floats = [i for i in ratio if i is not None]
mean = statistics.mean(ratio_floats)
ratio_theory = -np.sin(np.pi/12)/np.cos(np.pi/12)

ratio_constrain = []
for i in ratio_floats:
    if i*0.9 > ratio_theory:
        if i*1.1 < ratio_theory:
            ratio_constrain.append(i)

mean_constrain = statistics.mean(ratio_constrain)
print(f"Original Mean:    {mean}\n"
      f"Constrained Mean: {mean_constrain}")

plt.plot(ns, ratio, color="blue", label="Data")
x = np.linspace(min(ns), max(ns), 1000)


# def f(x, b):
# return -1/x+b


# plt.plot(x, f(x, mean), color="green", linestyle="dashed", label="-1/x+Mean")

# plt.axhline(factor, color="orange", linestyle="dashed", label="Geometry -(sin15/cos15)")
# plt.axhline(factor*0.9, color="green", linestyle="dashed", label="90% Lower Bound")
# plt.axhline(factor*1.1, color="red", linestyle="dashed", label="110% Upper Bound")

plt.title(f"Y/X Ratio, {increment/10} µm {axis}-Axis Increment")
plt.xlabel("Input Distance (µm)")
plt.ylabel("Output Y/X Ratio (Unitless)")

plt.legend()
plt.tight_layout()
plt.show()
