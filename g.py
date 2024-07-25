import numpy as np
import matplotlib.pyplot as plt

from transform import indicator_to_hexapod


def f(x, s, u):
    return 1/(s*np.sqrt(2*np.pi))*np.e**(-1/2*((x-u)/s)**2)


def g(x, s):
    return np.sqrt(2/np.pi)/s*np.e**(-x**2/(2*s**2))


def circle(origin, radius, color, fill, label):
    circle = plt.Circle(origin, radius, color=color, fill=fill, label=label)
    plt.gca().add_patch(circle)


def circle_std(origin, mean, std, color0, color1, label, zorder):
    circle = plt.Circle(origin, mean+std, color=color0, fill=True, zorder=0)
    plt.gca().add_patch(circle)

    circle = plt.Circle(origin, mean-std, color="white", fill=True, zorder=0)
    plt.gca().add_patch(circle)

    circle_mean(origin, mean, color1, label, zorder)


def circle_mean(origin, mean, color, label, zorder):
    circle = plt.Circle(origin, mean, color=color, fill=False, label=label, zorder=zorder)
    plt.gca().add_patch(circle)


def hist(x, s, u, i, title):
    ys, *_ = plt.hist(x, bins=np.arange(np.floor(min(x)*10)/10, np.ceil(max(x)*10)/10+0.1, 0.1), color="blue", zorder=2)

    plt.axvline(u, color="orange", label="Mean ± StD", zorder=3)
    plt.fill_betweenx([0, max(ys)], u-s, u+s, color="bisque", zorder=1)
    plt.axvline(i, color="red", label="Ideal", zorder=3)

    xs = np.linspace(min(x), max(x), 1000)
    plt.plot(xs, f(xs, s, u)*len(x)*0.1, color="green", label="Gaussian", zorder=4)

    noshow("Magnitude (µm)", "Count (#)", title)


def noshow(xlabel, ylabel, title):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    plt.legend(loc="upper right")
    plt.tight_layout()


def show(xlabel, ylabel, title):
    noshow(xlabel, ylabel, title)
    plt.show()


def reduce_data(data, transform):
    if transform is True:
        data = [indicator_to_hexapod(i) for i in data]

    x = [i[0]*1000 for i in data]
    y = [i[1]*1000 for i in data]
    z = [i[2]*1000 for i in data]

    return x, y, z


def supshow(title):
    plt.suptitle(title)
    plt.show()
