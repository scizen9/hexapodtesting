from pipython import GCSDevice
from serial import Serial
from time import sleep
import numpy as np

from f import home, zero, move, read, position
from transform import indicator_to_hexapod

i_list, h_list, p_list = [], [], []
steps = []

with GCSDevice() as pidevice:
    with Serial("/dev/ttyACM0", 115200) as ser:
        pidevice.ConnectRS232("/dev/ttyUSB0", 115200)
            
        step = 0
        while True:
            i = read(ser)
            h = indicator_to_hexapod(i)
            p = position(pidevice)
            
            i_list.append(i)
            h_list.append(h)
            p_list.append(p)  
            
            print(i)
            print(h)
            print(p)
            print("")
                
            if np.sqrt(h[0]**2+h[1]**2+h[2]**2) <= 0.1/1000:
                break
                
            else:
                move(pidevice, [p[0]-h[0], p[1]-h[1], p[2]-h[2]])
                sleep(1)

            step += 1            
        steps.append(step)

print(i_list)
print(h_list)
print(p_list)
print(steps)
