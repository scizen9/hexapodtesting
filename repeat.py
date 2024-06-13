from pipython import GCSDevice
from serial import Serial
from f import home, move, position, zero, read
import matplotlib.pyplot as plt
import statistics
import numpy as np

axis = "x"
increment = 0.4
# remember to change indicator

increment = increment*10

with GCSDevice() as pidevice:
    with Serial("/dev/ttyACM0", 115200) as ser:
        pidevice.ConnectRS232("/dev/ttyUSB0", 115200)
        
        readings = []
        n = 0
        while n != 60:
            home(pidevice)
            zero(ser)
            
            m = 0
            while m != 1000:
                move(pidevice, [m/10000, 0, 0])
                m += increment
            m = 1000
            while m != 0-increment:
                move(pidevice, [m/10000, 0, 0])
                m -= increment

            reading = read(ser)[0]
            readings.append(reading*1000)
            print(n)
            n += 1

mean = statistics.mean(readings)
std = statistics.stdev(readings)

increment = increment/10

print(f"{mean} ± {std}")

plt.fill_between(range(len(readings)), mean-std, mean+std, color="bisque")
plt.plot(range(len(readings)), readings, color="blue")
plt.axhline(mean, color="orange", label="Mean ± StD")

plt.title(f"{axis}'-Axis Repeatability Test, {increment} µm Increment")
plt.xlabel("Trial (#)")
plt.ylabel("Output Distance from Home Position (µm)")

plt.legend()
plt.tight_layout()
plt.show()


plt.hist(readings, bins=np.arange(min(readings)-0.05, max(readings)+0.1, 0.1), color="blue")

plt.title(f"{axis}'-Axis Repeatability Test, {increment} µm Increment")
plt.xlabel("Output Distance from Home Position (µm)")
plt.ylabel("Counts")

plt.tight_layout()
plt.show()
