import numpy as np
import matplotlib.pyplot as plt

from data.DATA_re import data
from transform import indicator_to_hexapod
from g import g, circle_std, circle_mean, hist, show, reduce_data, supshow

raw = []
for i in data:
    j = [indicator_to_hexapod(k) for k in i]
    raw.append(j)

radii = [2, 1.5, 1, 0.5, 2*np.sqrt(2/np.pi)]
titles = ["Test 1", "Test 2, 1.5 µm", "Test 2, 1 µm", "Test 2, 0.5 µm", "Test 3"]

means0, means1 = [], []
stds0, stds1 = [], []
for n in range(int(len(raw)/2)):
    radius = radii[n]
    title = titles[n]

    _ = raw[2*n]

    x0 = [i[0]*1000 for i in _]
    y0 = [i[1]*1000 for i in _]
    z0 = [i[2]*1000 for i in _]

    _ = raw[2*n+1]
    x1 = [i[0]*1000 for i in _]
    y1 = [i[1]*1000 for i in _]
    z1 = [i[2]*1000 for i in _]
    
    mean0x = np.mean(x0)
    mean0y = np.mean(y0)
    mean0z = np.mean(z0)
    
    mean1x = np.mean(x1)
    mean1y = np.mean(y1)
    mean1z = np.mean(z1)
    
    print(mean0x, mean0y, mean0z)
    print(mean1x, mean1y, mean1z)
    print(np.sqrt(mean0x**2+mean0y**2+mean0z**2))
    print(np.sqrt(mean1x**2+mean1y**2+mean1z**2))

    mag0 = [np.sqrt(x0[i]**2+y0[i]**2+z0[i]**2) for i in range(len(x0))]
    mag1 = [np.sqrt(x1[i]**2+y1[i]**2+z1[i]**2) for i in range(len(x0))]

    mean0 = np.mean(mag0)
    mean1 = np.mean(mag1)
    std0 = np.std(mag0)
    std1 = np.std(mag1)

    means0.append(mean0)
    means1.append(mean1)
    stds0.append(std0)
    stds1.append(std1)

    print(mean0, mean1)
    print(std0, std1)
    print()

    plt.scatter(x0, y0, color="blue", zorder=1)
    plt.scatter(x1, y1, color="orange", zorder=1)

    circle_std((mean0x, mean0y), mean0, std0, "lightblue", "purple", "Mean ± StD Start", 2)
    circle_std((mean1x, mean1y), mean1, std1, "bisque", "red", "Mean ± StD Stop", 2)
    circle_mean((0, 0), radius, "green", "Ideal Start", 2)

    plt.scatter([0], [0], color="black", label="Ideal Stop", zorder=2)
    plt.scatter([mean0x], [mean0y], color="purple", zorder=2)
    plt.scatter([mean1x], [mean1y], color="red", zorder=2)

    show("x' Position (µm)", "y' Position (µm)", title)


    bins_x = np.arange(np.floor(min(x0+x1)*10)/10, np.ceil(max(x0+x1)*10)/10+0.1, 0.1)
    bins_y = np.arange(np.floor(min(y0+y1)*10)/10, np.ceil(max(y0+y1)*10)/10+0.1, 0.1)

    plt.hist2d(x0+x1, y0+y1, bins=[bins_x, bins_y], cmap=plt.cm.jet, zorder=1)
    plt.colorbar(label="Count (#)")

    circle_mean((mean0x, mean0y), mean0, "purple", "Mean Start", 2)
    circle_mean((mean1x, mean1y), mean1, "red", "Mean Stop", 2)
    circle_mean((0, 0), radius, "green", "Ideal Start", 2)

    plt.scatter([0], [0], color="black", label="Ideal Stop", zorder=2)
    plt.scatter([mean0x], [mean0y], color="purple", zorder=2)
    plt.scatter([mean1x], [mean1y], color="red", zorder=2)

    show("x' Position (μm)", "y' Position (μm)", f"{title} 2D Histogram")


    x = range(len(mag0))

    plt.scatter(x, mag0, color="blue", zorder=1)
    plt.scatter(x, mag1, color="orange", zorder=1)

    plt.axhline(mean0, color="purple", label="Mean ± StD Start", zorder=2)
    plt.axhline(mean1, color="red", label="Mean ± StD Stop", zorder=2)

    plt.fill_between(x, mean0-std0, mean0+std0, color="lightblue", zorder=0)
    plt.fill_between(x, mean1-std1, mean1+std1, color="bisque", zorder=0)
    
    plt.axhline(radius, color="green", label="Ideal Start", zorder=3)
    plt.axhline(0, color="black", label="Ideal Stop", zorder=3)

    show("Trial (#)", "Magnitude (µm)", f"{title} Magnitudes")


    plt.subplot(1, 2, 1)
    hist(mag0, std0, mean0, radius, "Start")
    if title == "Test 3":
        x = np.linspace(min(mag0), max(mag0), 1000)
        plt.plot(x, g(x, std0)*len(mag0)*0.1, color="black", label="Half-Gaussian")
        plt.legend()

    plt.subplot(1, 2, 2)
    hist(mag1, std1, mean1, 0, "Stop")

    supshow(f"{title} Magnitude Histogram")


x = radii[:4]
y0 = means0[:4]
y1 = means1[:4]

m0, b0 = np.polyfit(x, y0, 1)
m1, b1 = np.polyfit(x, y1, 1)
print(m0, b0)
print(m1, b1)

print(np.mean(stds0))
print(np.std(stds0))

plt.scatter(x, y0, label="Mean ± StD Start", color="blue")
plt.errorbar(x, y0, yerr=stds0[:4], capsize=3, color="blue")

plt.scatter(x, y1, label="Mean ± StD Stop", color="orange")
plt.errorbar(x, y1, yerr=stds1[:4], capsize=3, color="orange")

plt.plot(x, x, label="Ideal Start", color="green")
plt.plot(x, [0]*len(x), label="Ideal Stop", color="red")

show("Input Start Magnitude (µm)", "Output Start Magnitude (µm)", "Test 2 Results")


residuals0 = [x[i]-y0[i] for i in range(len(x))]
residuals1 = [i-0 for i in y1]

plt.scatter(x, residuals0, label="Resolution", color="blue")
plt.scatter(x, residuals1, label="Repeatability", color="orange")

plt.errorbar(x, residuals0, yerr=stds0[:4], capsize=3, color="blue")
plt.errorbar(x, residuals1, yerr=stds1[:4], capsize=3, color="orange")

plt.axhline(0, label="Ideal", color="green")
plt.axhline(0.2, label="Ideal Limit", color="red")

show("Input Start Magnitude (µm)", "Offset (µm)", "Test 2 Offset Results")
