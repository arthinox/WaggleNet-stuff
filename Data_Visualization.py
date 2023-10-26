import matplotlib.pyplot as plt
import numpy as np

count = 0
tmp = []
weight = []

with open("Schmitz Hive Travel (10152023).txt", 'r') as data: # file location depends on where it is on our laptop
    for lines in data.readlines():
        if count == 0:
            count += 1
            continue
        tmp = lines.split(",")
        weight.append(float(tmp[1]))

weight = np.array(weight)
mean = np.mean(weight)
std = np.std(weight)
threshold = 3
outliers = []
for x in weight:
    z_score = (x - mean) / std
    if abs(z_score) > threshold:
        outliers.append(x)

outliers = np.sort(outliers)
print(len(outliers)/len(weight))

# new_weight = np.zeros(weight.shape)
# offset = 2
# for i in range(offset, len(weight) - offset):
#     new_weight[i] = np.median(weight[i-offset: i+offset])


plt.plot(range(0, len(weight)), weight)
plt.xlabel("time (seconds)")
plt.ylabel("weight (kg)")
plt.title("weight over time")
plt.show()