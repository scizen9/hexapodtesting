from time import sleep
from pipython import GCSDevice
from serial import Serial

from f import home, move, zero, read

start = -30  # μm
stop = 30
increment = 0.1

with GCSDevice() as pidevice:
    with Serial("/dev/ttyACM0", 115200) as ser:
        pidevice.ConnectRS232("/dev/ttyUSB0", 115200)

        readings, ns = [], []
        n = start
        while n != stop+increment:
            home(pidevice)
            sleep(1)

            zero(ser)
            sleep(1)

            r0 = read(ser)

            move(pidevice, [n/1000, 0, 0])
            # move(pidevice, [0, n/1000, 0])
            # move(pidevice, [0, 0, n/1000])
            sleep(1)

            r1 = read(ser)

            r = []
            m = 0
            while m != len(r1):
                r.append(1000*(r1[m]-r0[m]))
                m += 1

            x.append(r[0])
            y.append(r[1])
            z.append(r[2])

            ns.append(n)
            print(n)

            n += increment
            n = round(n, 1)

print(x)
print(y)
print(z)
print(n)

