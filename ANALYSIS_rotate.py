import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

from data.DATA_rotate import data, ns
from g import noshow, reduce_data, supshow

raw = []
for i in range(len(data)):
    x, y, z = reduce_data(data[i], False)
    raw.append(x)
    raw.append(y)
    raw.append(z)

ns = [i*1000 for i in ns]

ms, bs = [], []

for i in raw:
    m, b = np.polyfit(ns, i, 1)

    ms.append(m)
    bs.append(b)

r21, r22, residuals, stds1, stds2 = [], [], [], [], []
n = 0

while n != len(raw):
    m = ms[n]
    b = bs[n]

    theory = [m*i+b for i in ns]
    real = raw[n]

    r2 = r2_score(real, theory)

    residual = []

    for i in range(len(real)):
        residual.append(real[i]-theory[i])

    std = np.std(residual)

    if n < len(raw)/2:
        stds1.append(std)
        r21.append(r2)

    else:
        stds2.append(std)
        r22.append(r2)
    
    residuals.append(residual)

    n += 1

print("Rotation Matrices:")
for i in range(3):
    print(ms[i], ms[i+3], ms[i+6])
print()

for i in range(9, 12):
    print(ms[i], ms[i+3], ms[i+6])
print()


print("Translation Matrices:")
for i in range(3):
    print(bs[i], bs[i+3], bs[i+6])
print()

for i in range(9, 12):
    print(bs[i], bs[i+3], bs[i+6])
print()


print("Translation Vectors:")
for i in range(3):
    print(np.mean([bs[i], bs[i+3], bs[i+6]]))
print()

for i in range(9, 12):
    print(np.mean([bs[i], bs[i+3], bs[i+6]]))
print()


print("Residual StD Matrices:")
for i in range(3):
    print(stds1[i], stds1[i+3], stds1[i+6])
print()

for i in range(3):
    print(stds2[i], stds2[i+3], stds2[i+6])
print()


print("R2 Matrices:")
for i in range(3):
    print(r21[i], r21[i+3], r21[i+6])
print()

for i in range(3):
    print(r22[i], r22[i+3], r22[i+6])
print()


mag_std1 = np.sqrt(sum([i**2 for i in stds1]))
mag_std2 = np.sqrt(sum([i**2 for i in stds2]))

print(mag_std1)
print(mag_std2)

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

    plt.scatter(ns, raw[i], s=3)
    plt.scatter(ns, raw[i+1], s=3)
    plt.scatter(ns, raw[i+2], s=3)

    plt.plot(x, f(ms[i], bs[i], x), color="blue", label="X-Fit")
    plt.plot(x, f(ms[i+1], bs[i+1], x), color="orange", label="Y-Fit")
    plt.plot(x, f(ms[i+2], bs[i+2], x), color="green", label="Z-Fit")

    noshow("Input Position (µm)", "Output Position (µm)", titles[i3])

    if i == 6 or i == 15:
        supshow("-Axis Motion")

for i in _:
    i3 = int(i/3)

    if i <= 6:
        plt.subplot(2, 2, i3+1)

    else:
        plt.subplot(2, 2, i3-2)

    plt.scatter(ns, residuals[i], s=3, label="X")
    plt.scatter(ns, residuals[i+1], s=3, label="Y")
    plt.scatter(ns, residuals[i+2], s=3, label="Z")

    noshow("Input Position (µm)", "Output Position (µm)", titles[i3])

    if i == 6 or i == 15:
        supshow("-Axis Residuals")
