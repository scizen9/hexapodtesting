import numpy as np
import matplotlib.pyplot as plt

from DATA_noise import data

print(np.mean(data))
print(np.std(data))

plt.hist(data, bins=np.arange(min(data)-0.05, max(data)+0.1, 0.1))

plt.title("Indicator Noise")
plt.xlabel("Reading (µm)")
plt.ylabel("Counts")

plt.tight_layout()
plt.show()
