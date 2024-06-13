from pipython import GCSDevice
from serial import Serial
from f import home, move, position, zero, read
import matplotlib.pyplot as plt
import statistics


def get_data(increment, coord):
    n, trial, x, y, z, x2y2z2, h, ratio1, ratio2 = 0, [], [], [], [], [], [], [], []
    n = -5000
    while n != 5000+increment:
        if coord == "x":
            move(pidevice, [n/10000, 0, 0])
        elif coord == "y":
            move(pidevice, [0, n/10000, 0])
        else:
            move(pidevice, [0, 0, n/10000])

        i_reading = read(ser)
        h_reading = position(pidevice)

        for i in range(len(i_reading)):
            if i_reading[i] is None:
                i_reading[i] = 0

        i_reading = [i*1000 for i in i_reading]  # Convert from mm to um.
        h_reading = [i*1000 for i in h_reading]

        i0, i1, i2 = i_reading[0], i_reading[1], i_reading[2]

        trial.append(n/10)
        x.append(i0)
        y.append(i1)
        z.append(i2)
        if n >= 0:
            x2y2z2.append((i0**2+i1**2+i2**2)**0.5)
        else:
            x2y2z2.append(-(i0**2+i1**2+i2**2)**0.5)

        if coord == "x":
            h.append(h_reading[0])
        elif coord == "y":
            h.append(h_reading[1])
        else:
            h.append(h_reading[2])

        try:
            if coord == "x":
                ratio1.append(i1/i0)
                ratio2.append(i2/i0)
            elif coord == "y":
                ratio1.append(i0/i1)
                ratio2.append(i2/i1)
            else:
                ratio1.append(i0/i2)
                ratio2.append(i1/i2)
        except ZeroDivisionError:
            ratio1.append(None)
            ratio2.append(None)

        print(n)
        n += increment

    return trial, x, y, z, x2y2z2, h, ratio1, ratio2


with GCSDevice() as pidevice:
    with Serial("/dev/ttyACM0", 115200) as ser:
        pidevice.ConnectRS232("/dev/ttyUSB0", 115200)
        home(pidevice)
        zero(ser)

        increment, coord = 4, "z"
        trial, x, y, z, x2y2z2, h, ratio1, ratio2 = get_data(increment, coord)

# Figure 1
plt.plot(trial, x, color="blue", label="Indicator-X")
plt.plot(trial, y, color="orange", label="Indicator-Y")
plt.plot(trial, z, color="green", label="Indicator-Z")
plt.plot(trial, h, color="red", label=f"Hexapod-{coord.lower()}'")
plt.plot(trial, x2y2z2, color="black", label="sqrt(X^2+Y^2+Z^2)", linestyle="dashed")

plt.title(f"{coord.lower()}'-Axis Operational Test, {increment/10} µm Increment")
plt.xlabel("Input Distance (µm)")
plt.ylabel("Output Distance (µm)")

plt.legend()
plt.tight_layout()
plt.show()


def get_ratio_figure(ratio1, ratio2, trial, coord, num, increment):
    colors1 = ["blue", "green"]
    colors2 = ["orange", "red"]
    colors3 = ["bisque", "lightsalmon"]
    if coord == "x":
        r_strs = ["y/x", "z/x"]
    elif coord == "y":
        r_strs = ["x/y", "z/y"]
    else:
        r_strs = ["x/z", "y/z"]

    n = 0
    for i in [ratio1, ratio2]:
        r = [j for j in i if j is not None]
        mean = statistics.mean(r)
        std = statistics.stdev(r)
        print(f"Mean: {mean}\n")
        print(f"StD: {std}")

        plt.axhline(mean, color=colors2[n], label=f"{r_strs[n]} Mean")
        plt.fill_between(trial, mean-std, mean+std, color=colors3[n])
        plt.plot(trial, i, color=colors1[n], label=f"{r_strs[n]}")
        
        n += 1

    plt.title(f"Indicator-Measured Ratios, {increment/10} {coord.upper()}-Axis µm Input Increase")
    plt.xlabel("Input Distance (µm)")
    plt.ylabel(f"Output Ratio (Unitless)")

    plt.legend()
    plt.tight_layout()
    plt.show()


get_ratio_figure(ratio1, ratio2, trial, coord, 1, increment)

