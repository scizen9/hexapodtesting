from pipython import GCSDevice
from serial import Serial

from f import read

with GCSDevice() as pidevice:
    with Serial("/dev/ttyACM0", 115200) as ser:
        pidevice.ConnectRS232("/dev/ttyUSB0", 115200)

        readings = []
        while True:
            #home(pidevice)
            #sleep(1)

            #zero(ser)
            #sleep(1)

            reading = read(ser)
            reading = [i*1000 for i in reading]
            print(reading)

            readings.append(reading)

            if len(readings) > 500:
                break

print(readings)
