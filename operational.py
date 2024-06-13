from pipython import GCSDevice
from serial import Serial
from f import home, move, position, zero, read
import matplotlib.pyplot as plt

axis = "x'"
increment = 10  # microns
start = -500  # microns
stop = 500  # microns

increment *= 10
start *= 10
stop *= 10

with GCSDevice() as pidevice:
    with Serial("/dev/ttyACM0", 115200) as ser:
        pidevice.ConnectRS232("/dev/ttyUSB0", 115200)
        home(pidevice)
        zero(ser)

        x, y, z, xyz2, h = [], [], [], [], []
        n = start
        while n != stop+increment:
            move(pidevice, [n/10000, 0, 0])  # Axis-dependent

            i_reading = read(ser)
            h_reading = position(pidevice)

            i_reading = [i*1000 for i in i_reading]  # Convert from mm to um.
            h_reading = [i*1000 for i in h_reading]

            i0, i1, i2 = i_reading[0], i_reading[1], i_reading[2]

            x.append(i0)
            y.append(i1)
            z.append(i2)
            xyz2.append((i0**2+i1**2+i2**2)**0.5)

            h.append(h_reading[0])  # Axis-dependent

            print(n)
            n += increment


ns = [i/10 for i in range(0, len(x))]
plt.plot(ns, x, color="blue", label="Indicator-X")
plt.plot(ns, y, color="orange", label="Indicator-Y")
plt.plot(ns, z, color="green", label="Indicator-Z")
plt.plot(ns, h, color="red", label=f"Hexapod-{axis}")
plt.plot(ns, xyz2, color="black", label="sqrt(X^2+Y^2+Z^2)", linestyle="dashed")

plt.title(f"{axis}-Axis Operational Test, {increment/10} µm Increment")
plt.xlabel("Input Distance (µm)")
plt.ylabel("Output Distance (µm)")

plt.legend()
plt.tight_layout()
plt.show()
