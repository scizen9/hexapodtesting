import matplotlib.pyplot as plt
import numpy as np

from data.DATA_flexure import data
from transform import indicator_to_hexapod
from g import f, circle_std, circle_mean, show

readings = data[0]
steps = data[1]

axes = []
for i in range(3):
    axis = [indicator_to_hexapod(j)[i]*1000 for j in readings]
    axes.append(axis)

x = axes[0]
y = axes[1]
z = axes[2]

mag = []
for n in range(len(x)):
    mag.append((x[n]**2+y[n]**2+z[n]**2)**(1/2))

start, stop = [], []
n = 0
for i in steps:
    start.append(n)
    n += i+1
    stop.append(n-1)

start_mag = [mag[i] for i in start]
stop_mag = [mag[i] for i in stop]

i = data[0]
raw = []
for j in i:
    k = indicator_to_hexapod(j)
    raw.append([m*1000 for m in k])

x, y = [], []
for i in start:
    x.append(raw[i][0])
    y.append(raw[i][1])

x2, y2 = [], []
for i in stop:
    x2.append(raw[i][0])
    y2.append(raw[i][1])

meanx = np.mean(x)
meany = np.mean(y)

mag1 = [np.sqrt(x[n]**2+y[n]**2) for n in range(len(x))]

mean = np.mean(mag1)
std = np.std(mag1)

n1 = [15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, -165, -150, -135, -120, -105, -90, -75, -60, -45, -30, -15, 0]


plt.plot([i[0] for i in raw], [i[1] for i in raw], color="blue", zorder=1)
plt.scatter([i[0] for i in raw], [i[1] for i in raw], color="blue", zorder=1)

plt.scatter(x, y, c=n1, cmap="rainbow", label="Start", zorder=2)
plt.colorbar(label="Angle (deg)")

plt.scatter(x2, y2, color="green", label="Stop", zorder=2)

circle_std((meanx, meany), mean, std, "lightblue", "purple", "Mean ± StD Start", 3)
plt.scatter([meanx], [meany], color="purple", zorder=2)

circle_mean((0, 0), 0.1, "red", "Limit Stop", 3)
plt.scatter(0, 0, color="black", label="Ideal Stop", zorder=2)

#plt.xlim(-10, 10)
#plt.ylim(-10, 10)

plt.xlim(-0.5, 0.5)
plt.ylim(-0.5, 0.5)

show("x' (µm)", "y' (µm)", "Flexure Test")


plt.scatter(range(len(mag)), mag, color="blue", zorder=1)
plt.plot(range(len(mag)), mag, color="blue", zorder=1)

plt.scatter(start, start_mag, c=n1, cmap="rainbow", label="Start", zorder=2)
plt.colorbar(label="Angle (deg)")
plt.scatter(stop, stop_mag, color="green", label="Stop", zorder=2)

plt.axhline(0.1, color="red", label="Limit Stop", zorder=3)

plt.yscale("log")

show("Step (#)", "Magnitude (µm)", "Flexure Test")


trials = range(len(steps))
mean = np.mean(steps)
std = np.std(steps)

plt.scatter(trials, steps, color="blue", zorder=1)

plt.axhline(mean, color="orange", label="Mean ± StD", zorder=2)
plt.fill_between(trials, mean-std, mean+std, color="bisque", zorder=0)

show("Trial (#)", "Step (#)", "Step versus Trial")


ys, *_ = plt.hist(steps, bins=np.arange(min(steps)-0.5, max(steps)+1, 1), color="blue", zorder=1)

plt.axvline(mean, color="orange", label="Mean ± StD", zorder=2)
plt.fill_betweenx([0, max(ys)], mean-std, mean+std, color="bisque", zorder=0)

plt.axvline(1, color="red", label="Ideal", zorder=2)

x = np.linspace(min(steps), max(steps), 1000)
plt.plot(x, f(x, std, mean)*len(steps), color="green", label="Gaussian", zorder=3)

show("Step (#)", "Count (#)", "Step Histogram")