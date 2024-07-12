from pipython import GCSDevice
from serial import Serial
from time import sleep

from f import home, zero, read

with GCSDevice() as pidevice:
    with Serial("/dev/ttyACM0", 115200) as ser:
        pidevice.ConnectRS232("/dev/ttyUSB0", 115200)
        
        reading0, reading1, reading2 = [], [], []
        while True:
            home(pidevice)
            sleep(1)

            zero(ser)
            sleep(1)

            reading = read(ser)
            reading = [i*1000 for i in reading]
            print(reading)
            
            reading0.append(reading[0])
            reading1.append(reading[1])
            reading2.append(reading[2])

            if len(reading0) > 500:
                break

print(reading0)
print(reading1)
print(reading2)

