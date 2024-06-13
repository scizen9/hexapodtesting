from pipython import GCSDevice
from serial import Serial
from f import home, move, position, zero, read
import matplotlib.pyplot as plt
import statistics
import numpy as np

axis = "x'"
increment = 0.4  # microns
start = 0  # microns
stop = 500  # microns

increment *= 10
start *= 10
stop *= 10

with GCSDevice() as pidevice:
    with Serial("/dev/ttyACM0", 115200) as ser:
        pidevice.ConnectRS232("/dev/ttyUSB0", 115200)

        readings = []
        n = 0
        while n != 60:
            home(pidevice)
            zero(ser)

            move(pidevice, [stop/10000, 0, 0])

            m = stop
            while m != start-increment:
                move(pidevice, [m/10000, 0, 0])
                # if m == 0:
                # readings.append(read(ser)[0]*1000)
                m -= increment

            readings.append(read(ser)[0]*1000)
            print(n)
            n += 1

mean = statistics.mean(readings)
std = statistics.stdev(readings)

increment = increment/10
start = start/10
stop = stop/10

print(f"{mean} ± {std}")

ns = range(len(readings))

plt.fill_between(ns, mean-std, mean+std, color="bisque")
plt.plot(ns, readings, color="blue")
plt.axhline(mean, color="orange", label="Mean ± StD")

plt.title(f"{axis}-Axis Repeatability Test, {increment} µm Increment")
# plt.title(f"{axis}-Axis Repeatability Test, {stop} µm Range")
# plt.title(f"{axis}-Axis Repeatability Test, {start} µm Final Position")
plt.xlabel("Trial (#)")
plt.ylabel("Output Distance from Home Position (µm)")

plt.legend()
plt.tight_layout()
plt.show()

plt.hist(readings, bins=np.arange(min(readings)-0.05, max(readings)+0.1, 0.1), color="blue")

plt.title(f"{axis}-Axis Repeatability Test, {increment} µm Increment")
# plt.title(f"{axis}-Axis Repeatability Test, {stop} µm Range")
# plt.title(f"{axis}-Axis Repeatability Test, {start} µm Final Position")
plt.xlabel("Output Distance from Home Position (µm)")
plt.ylabel("Counts")

plt.tight_layout()
plt.show()
