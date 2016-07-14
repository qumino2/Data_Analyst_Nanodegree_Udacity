import matplotlib.pyplot as plt
import numpy as np

samples = np.genfromtxt('stroop_sample - Sheet1.csv', delimiter=',', dtype=np.float32)

#Single Horizontal Whisker Plot
# plt.figure()
# data = cities[:, 6]
# plot1 = plt.boxplot(data, vert=False, widths = 0.2, patch_artist=True)
# plt.ylabel('Congruent')


#Plotting vertical box plots
locations = [1, 3]
plt.figure()
plot2 = plt.boxplot(samples, widths=0.4, positions = locations, patch_artist=True)

#plt.grid(axis = 'y', linestyle='--', which='major', color = 'lightgrey', alpha = 0.7)

names = ['Congruent', 'Incongruent']

plt.xticks(locations, names)

#plt.ylabel('Data')
plt.title('Box Plot')

plt.show()