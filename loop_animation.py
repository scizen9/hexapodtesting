import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

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

startx, starty, startz, start_mag = [], [], [], []
for i in start_steps:
    startx.append(x[i])
    starty.append(y[i])
    start_mag.append(mag[i])

stopx, stopy, stopz, stop_mag = [], [], [], []
for i in stop_steps:
    stopx.append(x[i])
    stopy.append(y[i])
    stop_mag.append(mag[i])

colors = ["blue"]*len(x)
n = 0
while n != len(x):
    if n in stop_steps:
        colors[n] = "orange"
    n += 1
fig, ax = plt.subplots()

circle = patches.Circle((0, 0), 0.15, edgecolor="red", facecolor="none", zorder=5)
ax.add_patch(circle)

# ax.set_xlim(-5, 5)
# ax.set_ylim(-5, 5)

ax.set_xlim(-0.2, 0.2)
ax.set_ylim(-0.2, 0.2)

ax.set_xlabel("x' (µm)")
ax.set_ylabel("y' (µm)")
ax.set_title("Control Loop")

lines = []
points = []

for i in range(len(x) - 1):
    line, = ax.plot([], [], lw=2)
    point, = ax.plot([], [], "o")
    lines.append(line)
    points.append(point)


def animate(num):
    for i in range(num - 1):
        line = lines[i]
        point = points[i]
        line.set_data(x[i:i + 2], y[i:i + 2])
        point.set_data(x[i:i + 2], y[i:i + 2])
        if colors[i] == "blue":
            line.set_color("blue")
            point.set_color("black")
        else:
            line.set_color("orange")
            point.set_color("black")
    return lines + points


# ani = animation.FuncAnimation(fig, animate, frames=len(x)+1, interval=20)
plt.show()

# ani.save("loop_movie.mp4", writer = "ffmpeg", fps = 5)
