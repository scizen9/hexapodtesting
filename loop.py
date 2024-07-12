from pipython import GCSDevice
from serial import Serial
from time import sleep
import numpy as np

from f import home, zero, move, read, position
from transform import indicator_to_hexapod

x, y = [], []
steps = []

with GCSDevice() as pidevice:
    with Serial("/dev/ttyACM0", 115200) as ser:
        pidevice.ConnectRS232("/dev/ttyUSB0", 115200)
        
        n = 0
        while n != 60:
            home(pidevice)
            sleep(1)
        
            zero(ser)

            mag = np.random.normal(0, 2)
            angle = np.random.uniform(0, np.pi)
            
            a = mag*np.cos(angle)
            b = mag*np.sin(angle)
            
            move(pidevice, [a/1000, b/1000, 0])
            sleep(1)
            
            i = read(ser)
            print(i)
            h = indicator_to_hexapod(i)
            
            pos = position(pidevice)
            
            step = 0
            while True:
                x.append(h[0])
                y.append(h[1])
                
                if np.sqrt(h[0]**2+h[1]**2) <= 0.1/1000:
                    break
                
                move(pidevice, [pos[0]-h[0], pos[1]-h[1], 0])
                sleep(1)
                
                i = read(ser)
                print(i)
                h = indicator_to_hexapod(i)
                
                pos = position(pidevice)

                step += 1
            
            steps.append(step)

            n += 1

print(x)
print(y)
print(steps)