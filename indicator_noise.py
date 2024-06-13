from pipython import GCSDevice
from serial import Serial
from f import home, move, position, zero, read
import matplotlib.pyplot as plt
import statistics
from time import sleep
import numpy as np

with GCSDevice() as pidevice:
    with Serial("/dev/ttyACM0", 115200) as ser:
        pidevice.ConnectRS232("/dev/ttyUSB0", 115200)
        home(pidevice)
        zero(ser)
        
        reading0, reading1, reading2 = [], [], []
        while True:
            reading = read(ser)
            reading = [i*1000 for i in reading]
            
            reading0.append(reading[0])
            reading1.append(reading[1])
            reading2.append(reading[2])
            
            sleep(0.05)
            if len(reading0) > 1000:
                break

readings = [reading0, reading1, reading2]
for i in readings:
    plt.plot(range(len(i)), i)
plt.show()

readings = reading0+reading1+reading2
unique_values = []
for i in readings:
    if i not in unique_values:
        unique_values.append(i)

plt.hist(readings, bins=np.arange(min(readings), max(readings)+0.1, 0.1))
plt.tight_layout()
plt.show()
