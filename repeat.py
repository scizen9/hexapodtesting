from pipython import GCSDevice
from serial import Serial
from time import sleep
import numpy as np

from f import home, zero, move, read, position
from transform import indicator_to_hexapod

radius = 0.002

with GCSDevice() as pidevice:
    with Serial("/dev/ttyACM0", 115200) as ser:
        pidevice.ConnectRS232("/dev/ttyUSB0", 115200)
    
        home(pidevice)
        sleep(1)
        
        x0, y0, x1, y1, ns = [], [], [], [], []
        n = 0
        while n != 500:
            zero(ser)
            
            # a = random.uniform(-radius, radius)
            # b = np.sqrt(radius**2-a**2)
            
            # _ = random.randrange(-1, 1)
            # if _ < 0:
            #     b = -b
            
            # _ = random.randrange(-1, 1)
            # if _ < 0:
            #     x = a
            #     y = b
            # else:
            #     x = b
            #     y = a
            
            mag = np.random.normal(0.0, radius)
            angle = np.random.uniform(0, np.pi)
            
            x = mag*np.cos(angle)
            y = mag*np.sin(angle)
            
            move(pidevice, [x, y, 0])
            sleep(1)
            
            r0 = read(ser)
            print(r0)
            r0h = indicator_to_hexapod(r0)
            
            pos = position(pidevice)
            
            dx = pos[0]-r0h[0]
            dy = pos[1]-r0h[1]
            
            move(pidevice, [-dx, -dy, 0])
            sleep(1)
            
            r1 = read(ser)
            
            x0.append(r0[0]*1000)
            y0.append(r0[1]*1000)
            
            x1.append(r1[0]*1000)
            y1.append(r1[1]*1000)
            
            ns.append(n)
            
            print(n)
            n += 1

print(x0)
print(y0)
print(x1)
print(y1)

