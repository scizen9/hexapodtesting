from pipython import GCSDevice
from serial import Serial
from f import home, move, position, zero, read
import numpy as np

with GCSDevice() as pidevice:
    with Serial("/dev/ttyACM0", 115200) as ser:
        pidevice.ConnectRS232("/dev/ttyUSB0", 115200)

        pos = [[0.5, 0, 0], [0, 0.5, 0], [0, 0, 0.5]]
        readings = []
        for i in pos:
            home(pidevice)
            zero(ser)
            move(pidevice, i)
            reading = read(ser)
            for j in range(len(reading)):
                if reading[j] is None:
                    reading[j] = 0

            #print(f"Hexapod    {i}: {position(pidevice)}\n"
            #      f"Indicators {i}: {reading}")
            print(f"Hexapod:    {i}\n"
                  f"Indicators: {reading}")
            readings.append(reading)


def get_angles(readings):
    for i in readings:
        angle_xx = np.arctan(i[0]/0.5)
        angle_yy = np.arctan(i[1]/0.5)
        angle_zz = np.arctan(i[2]/0.5)
        angle_xy = angle_xx+angle_yy
        angle_xz = angle_xx+angle_zz
        angle_yz = angle_yy+angle_zz

        angles_aa = [angle_xx, angle_yy, angle_zz]
        angles_ab = [angle_xy, angle_xz, angle_yz]

        angles_aa = [np.rad2deg(i) for i in angles_aa]
        angles_ab = [np.rad2deg(i) for i in angles_ab]

        print(f"{angles_aa}\n"
              f"{angles_ab}\n")


get_angles(readings)

