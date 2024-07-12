import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

from DATA_loop import data

x, y, steps = data[0], data[1], data[2]

x = [i*1000 for i in x]
y = [i*1000 for i in y]

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

circle = patches.Circle((0, 0), 0.15, edgecolor="red", facecolor="none", zorder=5) # linewidth
ax.add_patch(circle)

ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)

ax.set_xlabel("x' (µm)")
ax.set_ylabel("y' (µm)")
ax.set_title("Control Loop")

lines = []
points = []

for i in range(len(x)-1):
    line, = ax.plot([], [], lw=2)
    point, = ax.plot([], [], "o")
    lines.append(line)
    points.append(point)


def animate(num):
    for i in range(num-1):
        line = lines[i]
        point = points[i]
        line.set_data(x[i:i+2], y[i:i+2])
        point.set_data(x[i:i+2], y[i:i+2])
        if colors[i] == "blue":
            line.set_color("blue")
            point.set_color("black")
        else:
            line.set_color("orange")
            point.set_color("black")
    return lines + points
    
ani = animation.FuncAnimation(fig, animate, frames=len(x)+1, interval=20)
plt.show() 

# ani.save("loop_movie.mp4", writer = "ffmpeg", fps = 5)


plt.plot(x, y, color="blue", label="Data", zorder=1)
plt.scatter(startx, starty, color="orange", label="Random Positions", zorder=2)
plt.scatter(stopx, stopy, color="green", label="Return Positions", zorder=3)
plt.scatter(0, 0, color="red", label="Origin", zorder=4)

circle = plt.Circle((0, 0), 0.1, fill=False, color="purple", label="Maximum Return Position", zorder=5)
plt.gca().add_patch(circle)

plt.xlim(-5, 5)
plt.ylim(-5, 5)

plt.title("Control Loop")
plt.xlabel("x' (µm)")
plt.ylabel("y' (µm)")

plt.legend()
plt.tight_layout()
plt.show()


plt.plot(range(len(mag)), mag, color="blue", label="Data")
plt.scatter(start_steps, start_mag, color="orange", label="Random Positions")
plt.scatter(stop_steps, stop_mag, color="green", label="Return Positions")
plt.axhline(0.1, color="red", label="Maximum Return Position")

plt.title("Control Loop Magnitude")
plt.xlabel("Step (#)")
plt.ylabel("Magnitude (µm)")

plt.legend()
plt.tight_layout()
plt.show()


mean = np.mean(steps)
std = np.std(steps)

print(mean)
print(std)

xsteps = range(len(steps))

plt.fill_between(xsteps, mean-std, mean+std, color="bisque")
plt.axhline(mean, color="orange", label="Mean ± Std")
plt.scatter(range(len(steps)), steps, label="Data")

plt.title("Steps per Trial")
plt.xlabel("Trial (#)")
plt.ylabel("Steps (#)")

plt.legend()
plt.tight_layout()
plt.show()

