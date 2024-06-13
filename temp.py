from pipython import GCSDevice
from serial import Serial
from f import home, move, position, zero, read
import numpy as np
import matplotlib.pyplot as plt
import statistics

def get_data(axis):
    with GCSDevice() as pidevice:
        with Serial("/dev/ttyACM0", 115200) as ser:
            pidevice.ConnectRS232("/dev/ttyUSB0", 115200)
            home(pidevice)
            zero(ser)

            n = -10002
            n_values, x_values, y_values, z_values = [], [], [], []
            while n != 10002:
                if axis == "x":
                    move(pidevice, [n/10000, 0, 0])
                elif axis == "y":
                    move(pidevice, [0, n/10000, 0])
                else:
                    move(pidevice, [0, 0, n/10000])
                reading = read(ser)
                while None in reading:
                    i = reading.index(None)
                    reading[i] = 0
                reading = [i*1000 for i in reading]  # Convert to um.

                x_values.append(reading[0])
                y_values.append(-reading[1])
                z_values.append(reading[2])
                n_values.append(n/10)
            
                print(n)
                n += 2
    return n_values, [x_values, y_values, z_values]


def figure_1(n_values, values, axis):
    if axis == "x":
        def f(x):
            return x*np.cos(np.pi/12)
        def g(x):
            return x*np.sin(np.pi/12)
        def h(x):
            return x-x
    elif axis == "y":
        def f(x):
            return x*np.sin(np.pi/12)
        def g(x):
            return x*np.cos(np.pi/12)
        def h(x):
            return x-x
    else:
        def f(x):
            return x-x
        def g(x):
            return x-x
        def h(x):
            return x
 
    x = np.linspace(min(n_values), max(n_values), len(n_values))
    plt.plot(x, f(x), color="blue", label="X-Predicted Distance", linestyle="dashed")
    plt.plot(x, g(x), color="orange", label="Y-Predicted Distance", linestyle="dashed")
    plt.plot(x, h(x), color="green", label="Z-Predicted Distance", linestyle="dashed")

    def a(x, m, b):
        return m*x+b


    colors = ["blue", "orange", "green"]
    axes = ["X", "Y", "Z"]
    ms, bs = [], []
    n = 0
    while n != len(values):
        m, b = np.polyfit(n_values, values[n], 1)
        print(f"Slope:     {m}\n"
              f"Intercept: {b}")
        ms.append(m)
        bs.append(b)
        if b < 0:
            label = f"{axes[n]}-Output={'{:4.2f}'.format(m)}*Input{'{:4.2f}'.format(b)}"
        else:
            label = f"{axes[n]}-Output={'{:4.2f}'.format(m)}*Input+{'{:4.2f}'.format(b)}"
        plt.plot(x, a(x, m, b), color=colors[n], label=label)
        plt.scatter(n_values, values[n], color=colors[n])
        n += 1

    plt.title("Input versus Output Distances, 0.2 µm Increment")
    plt.xlabel("Input Distance (µm)")
    plt.ylabel("Output Distance (µm)")

    plt.legend()
    plt.tight_layout()
    plt.show()

    return ms, bs, colors, axes
        

def figure_2(n_values, values, ms, bs, colors, axes):
    def a(x, m, b):
        return m*x+b
    
    n = 0
    differences = []
    for i in values:
        m = ms[n]
        b = bs[n]
        value = values[n]
        j = 0
        difference = []
        for i in n_values:
            difference.append(a(i, m, b)-value[j])
            j += 1
        differences.append(difference)
        n += 1

    total = differences[0]+differences[1]+differences[2]
    mean = statistics.mean(total)
    std = statistics.stdev(total)
    
    plt.fill_between(n_values, mean-std, mean+std, color="darksalmon")
    plt.axhline(mean, color="red", label="Mean ± StD")

    n = 0
    for i in differences:
        plt.scatter(n_values, i, color=colors[n], label=f"{axes[n]}-Axis Fit Minus Data")
        n += 1

    plt.title("Best-Fit Minus Experimental Data")
    plt.xlabel("Input Distance (µm)")
    plt.ylabel("Difference (µm)")

    plt.legend()
    plt.tight_layout()
    plt.show()
    
    return differences



def figure_3(values, differences):
    total = differences[0]+differences[1]+differences[2]
    plt.hist(total)
    plt.show()
    
    
    
axis = "x"
n_values, values = get_data(axis)
ms, bs, colors, axes = figure_1(n_values, values, axis)
differences = figure_2(n_values, values, ms, bs, colors, axes)
figure_3(values, differences)

difference = [abs(i) for i in difference]
mean = statistics.mean(difference)
std = statistics.stdev(difference)
plt.fill_between(n_values, mean-std, mean+std, color="bisque")
plt.axhline(mean, color="orange", label="Mean ± StD")
plt.scatter(n_values, difference, color="blue", label="Abs(Distance)")

plt.title("Abs(Difference)")
plt.xlabel("Input Distance (µm)")
plt.ylabel("Difference (µm)")

plt.legend()
plt.tight_layout()
plt.show()


# Figure 2
plt.scatter(f(x), x_values, color="blue", label="Theory-Experiment Relation")

m, b = np.polyfit(f(x), x_values, 1)

print(f"Slope:     {m}\n"
      f"Intercept: {b}")

x = np.linspace(0, f(max(n_values)), 1000)
plt.plot(x, g(x, m, b), color="orange", label="Best-Fit Line")

plt.title("Theoretical versus Experimental Distances, 0.2 µm Increment")
plt.xlabel("Theoretical Distance (µm)")
plt.ylabel("Experimental Distance (µm)")

plt.legend()
plt.tight_layout()
plt.show()
