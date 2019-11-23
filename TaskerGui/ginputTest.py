import matplotlib.pyplot as plt
import numpy as np
from math import pi, sin, cos, tan

"""
t = np.arange(10)
plt.plot(t, np.sin(t))
x = plt.ginput(1)
plt.show()
print(x)
"""

def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))


x = np.linspace(0, 2*pi, 100)
y = []
for i in x:
    y.append(sin(i))


plt.plot(x, y)
fig = plt.gcf()
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

"""
fig, ax = plt.subplots()
ax.plot(np.random.rand(10))
fig.show()
"""

