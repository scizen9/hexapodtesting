import matplotlib.pyplot as plt
import numpy as np

from DATA_repeat import data

_ = [0, 4, 8, 12, 16]
radii = [2, 1.5, 1, 0.5, 0]
titles = ["Test 1", "Test 2, 1.5 µm", "Test 2, 1 µm", "Test 2, 0.5 µm", "Test 3"]
means0, means1, stds0, stds1 = [], [], [], []

for i in _:
    x0 = data[i]
    y0 = data[i+1]
    x1 = data[i+2]
    y1 = data[i+3]

    mag0, mag1 = [], []
    n = 0
    while n != len(x0):
        mag0.append(np.sqrt(x0[n]**2+y0[n]**2))
        mag1.append(np.sqrt(x1[n]**2+y1[n]**2))

        n += 1

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
    print("")

    radius = radii[int(i/4)]
    title = titles[int(i/4)]

    plt.scatter(x0, y0, color="blue", label="Depart Position")
    plt.scatter(x1, y1, color="orange", label="Return Position")
    if title != "Test 3":
        circle = plt.Circle((0, 0), radius, color="green", fill=False, label="Ideal Depart Position")
        plt.gca().add_patch(circle)

    plt.title(title)
    plt.xlabel("X Position (μm)")
    plt.ylabel("Y Position (μm)")

    plt.legend()
    plt.tight_layout()
    plt.show()


    plt.hist2d(x0+x1, y0+y1, bins=[10, 10], cmap=plt.cm.jet)
    plt.colorbar(label="Counts")

    plt.title(f"{title} 2D Histogram")
    plt.xlabel("X Position (μm)")
    plt.ylabel("Y Position (μm)")

    plt.tight_layout()
    plt.show()


    x = range(len(mag0))

    plt.fill_between(x, mean0-std0, mean0+std0, color="lightblue")
    plt.fill_between(x, mean1-std1, mean1+std1, color="bisque")

    plt.axhline(mean0, color="blue", label="Depart Mean ± StD")
    plt.axhline(mean1, color="orange", label="Return Mean ± StD")
    if title != "Test 3":
        plt.axhline(radius, color="purple", label="Ideal Depart")
    plt.axhline(0, color="red", label="Ideal Return")

    plt.scatter(x, mag0, label="Depart Data")
    plt.scatter(x, mag1, label="Return Data")

    plt.title(f"{title} Magnitudes")
    plt.xlabel("Trial (#)")
    plt.ylabel("Magnitude (μm)")

    plt.legend()
    plt.tight_layout()
    plt.show()


x = [2, 1.5, 1, 0.5, None]

plt.scatter(x, means0, color="blue", label="Depart Mean ± StD")
plt.scatter(x, means1, color="orange", label="Return Mean ± StD")

plt.errorbar(x, means0, yerr=stds0, color="blue", capsize=3)
plt.errorbar(x, means1, yerr=stds1, color="orange", capsize=3)

plt.title("Magnitude Variation")
plt.xlabel("Ideal Magnitude (μm)")
plt.ylabel("Magnitude (μm)")

plt.legend()
plt.tight_layout()
plt.show()
