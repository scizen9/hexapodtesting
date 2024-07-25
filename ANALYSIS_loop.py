import numpy as np
import matplotlib.pyplot as plt

from data.DATA_loop import data, steps
from g import f, show, circle_mean, reduce_data

x, y, z = reduce_data(data, True)

mag = []
n = 0
while n != len(x):
    mag.append(np.sqrt(x[n]**2+y[n]**2))
    n += 1

start_steps, stop_steps = [], []
n = 0
for i in steps:
    start_steps.append(n)
    n += i+1
    stop_steps.append(n-1)

startx, starty, start_mag = [], [], []
for i in start_steps:
    startx.append(x[i])
    starty.append(y[i])
    start_mag.append(mag[i])

stopx, stopy, stop_mag = [], [], []
for i in stop_steps:
    stopx.append(x[i])
    stopy.append(y[i])
    stop_mag.append(mag[i])

plt.scatter(x, y, color="blue", zorder=1)
plt.plot(x, y, color="blue", zorder=1)

plt.scatter(startx, starty, color="orange", label="Start Position", zorder=2)
plt.scatter(stopx, stopy, color="green", label="Stop Position", zorder=3)
plt.scatter(0, 0, color="purple", label="Ideal Stop Position", zorder=4)

circle_mean((0, 0), 0.1, "red", "Stop Position Limit", 5)

# plt.xlim(-0.2, 0.2)
# plt.ylim(-0.2, 0.2)

show("x' (µm)", "y' (µm)", "Control Loop")


plt.scatter(range(len(mag)), mag, color="blue", zorder=1)
plt.plot(range(len(mag)), mag, color="blue", zorder=1)

plt.scatter(start_steps, start_mag, color="orange", label="Start Position", zorder=2)
plt.scatter(stop_steps, stop_mag, color="green", label="Stop Position", zorder=2)
plt.axhline(0.1, color="red", label="Stop Position Limit", zorder=3)

plt.yscale("log")

show("Step (#)", "Magnitude (µm)", "Control Loop Magnitude")


mean = np.mean(steps)
std = np.std(steps)

print(mean)
print(std)

xsteps = range(len(steps))

plt.scatter(xsteps, steps, color="blue", zorder=1)

plt.axhline(mean, color="orange", label="Mean ± StD", zorder=2)
plt.fill_between(xsteps, mean-std, mean+std, color="bisque", zorder=0)

show("Trial (#)", "Step (#)", "Step per Trial")


ys, *_ = plt.hist(steps, bins=np.arange(min(steps)-0.5, max(steps)+1, 1), color="blue", zorder=1)

plt.axvline(mean, color="orange", label="Mean ± StD", zorder=2)
plt.fill_betweenx([0, max(ys)], mean-std, mean+std, color="bisque", zorder=0)

plt.axvline(1, color="red", label="Ideal", zorder=2)

x = np.linspace(min(steps), max(steps), 1000)
plt.plot(x, f(x, std, mean)*len(steps), color="green", label="Gaussian", zorder=3)

show("Step (#)", "Count (#)", "Step Distribution")
