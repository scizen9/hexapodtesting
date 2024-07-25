import numpy as np
import matplotlib.pyplot as plt

from data.DATA_noise import data
from g import noshow, f, reduce_data, supshow

x, y, z = reduce_data(data, False)

axes = [x, y, z]

titles = ["X", "Y", "Z"]
means, stds = [], []

for n in range(len(axes)):
    i = axes[n]
    plt.subplot(2, 2, n+1)

    mean = np.mean(i)
    std = np.std(i)

    #print(mean)
    print(std)

    means.append(mean)
    stds.append(std)


    plt.scatter(range(len(i)), i, color="blue", zorder=1)

    plt.axhline(mean, color="orange", label="Mean ± StD", zorder=2)
    plt.fill_between(range(len(i)), mean-std, mean+std, color="bisque", zorder=0)

    noshow("Trial (#)", "Reading (µm)", titles[n])

supshow("-Indicator Noise")


for n in range(len(axes)):
    i = axes[n]
    plt.subplot(2, 2, n+1)
    ys, *_ = plt.hist(i, bins=np.arange(min(i)-0.05, max(i)+0.1, 0.1), color="blue", zorder=1)

    mean = means[n]
    std = stds[n]

    plt.axvline(mean, color="orange", label="Mean ± StD", zorder=2)
    plt.fill_betweenx([0, max(ys)], mean-std, mean+std, color="bisque", zorder=0)

    x = np.linspace(min(i), max(i), 1000)
    plt.plot(x, f(x, std, mean)*0.1*len(i), color="green", label="Gaussian", zorder=3)

    noshow("Reading (µm)", "Count (#)", titles[n])

supshow("-Indicator Noise Histograms")

std_mag = np.sqrt(sum([i**2 for i in stds]))
print(std_mag)
