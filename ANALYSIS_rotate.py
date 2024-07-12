import numpy as np
import matplotlib.pyplot as plt

from DATA_rotate import data, ns

ms, bs = [], []

for i in data:
    m, b = np.polyfit(ns, i, 1)
    ms.append(m)
    bs.append(b)

residuals = []
stds1 = []
stds2 = []
n = 0
while n != len(data):
    m = ms[n]
    b = bs[n]
    theory = [m*i+b for i in ns]
    
    residual = []
    for i in range(len(data[n])):
        residual.append(data[n][i]-theory[i])

    std = np.std(residual)
    if n < len(data)/2:
        stds1.append(std)
    else:
        stds2.append(std)
    
    
    residuals.append(residual)
    n += 1

print("Rotation Matrix:")

for i in range(3):
    print(ms[i], ms[i+3], ms[i+6])

print()

for i in range(9, 12):
    print(ms[i], ms[i+3], ms[i+6])

print()
print("Translation Matrix:")

for i in range(3):
    print(bs[i], bs[i+3], bs[i+6])

print()

for i in range(9, 12):
    print(bs[i], bs[i+3], bs[i+6])

print()
print("Translation Vector:")

for i in range(3):
    print(np.mean([bs[i], bs[i+3], bs[i+6]]))

print()

for i in range(9, 12):
    print(np.mean([bs[i], bs[i+3], bs[i+6]]))
    
print()
print("Residual Matrix:")

for i in range(3):
    print(stds1[i], stds1[i+3], stds1[i+6])

print()

for i in range(3):
    print(stds2[i], stds2[i+3], stds2[i+6])

print()
print(f"{np.mean(stds1)} ± {np.std(stds1)}")
print(f"{np.mean(stds2)} ± {np.std(stds2)}")


def f(m, b, x):
    return m*x+b


x = np.linspace(-30, 30, 1000)

titles = ["x'", "y'", "z'", "Rotated x'", "Rotated y'", "Rotated z'"]
_ = [0, 3, 6, 9, 12, 15]
for i in _:
    i3 = int(i/3)
    if i <= 6:
        plt.subplot(2, 2, i3+1)
    else:
        plt.subplot(2, 2, i3-2)
    plt.scatter(ns, data[i], s=3)
    plt.scatter(ns, data[i+1], s=3)
    plt.scatter(ns, data[i+2], s=3)

    plt.plot(x, f(ms[i], bs[i], x), color="blue", label="X")
    plt.plot(x, f(ms[i+1], bs[i+1], x), color="orange", label="Y")
    plt.plot(x, f(ms[i+2], bs[i+2], x), color="green", label="Z")

    plt.xlabel("Input Position (µm)")
    plt.ylabel("Output Position (µm)")
    plt.title(titles[i3])

    plt.legend()
    plt.tight_layout()
    if i == 6:
        plt.suptitle("-Axis Motion")
        plt.show()
    if i == 15:
        plt.suptitle("-Axis Motion")
        plt.show()


for i in _:
    i3 = int(i/3)
    if i <= 6:
        plt.subplot(2, 2, i3+1)
    else:
        plt.subplot(2, 2, i3-2)
    plt.scatter(ns, residuals[i], s=3, label="X")
    plt.scatter(ns, residuals[i+1], s=3, label="Y")
    plt.scatter(ns, residuals[i+2], s=3, label="Z")

    plt.xlabel("Input Position (µm)")
    plt.ylabel("Output Position (µm)")
    plt.title(titles[i3])

    plt.legend()

    if i == 6:
        plt.tight_layout()
        plt.suptitle("-Axis Residuals")
        plt.show()
    if i == 15:
        plt.tight_layout()
        plt.suptitle("-Axis Residuals")
        plt.show()

