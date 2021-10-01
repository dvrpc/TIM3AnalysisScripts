import numpy as np
import matplotlib.pyplot as plt

plt.scatter([0.1, 0.5], [13.8947783, 20.17227013], color = 'k')
plt.plot([0.1, 0.5], [13.8947783, 20.17227013], color = 'k', label = 'Linear Interpolation')
plt.plot([0, 0.6], 2*[16.65288159], color = 'r', linestyle = '--', label = 'Survey Target +20%')
plt.plot(2*[0.27574556], [13, 16.65288159], color = 'b', linestyle = ':', label = 'coef = 0.27574556')
plt.scatter([0.27574556], [16.65288159], color = 'b', s = 50)

plt.xlabel('Work Location inj_dist Value')
plt.ylabel('NJ Average Work Tour Length')

plt.xlim(0, 0.6)
plt.ylim(13, 21)

plt.legend(loc = 'best')
plt.grid(True)
plt.show()