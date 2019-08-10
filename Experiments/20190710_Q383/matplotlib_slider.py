import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib as mpl

def sinc(x, y):
    r = np.sqrt(x**2 + y**2)
    return np.sin(r) / r

x = np.linspace(-20, 20, 1000)
y = np.linspace(-20, 20, 1000)
# compute sinc on a grid of points using numpy broadcasting
z = sinc(x.reshape(1000, 1), y.reshape(1, 1000))


fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)

heat_map = plt.pcolor(x, y, z)
ax.margins(x=0)

ax_min = plt.axes([0.1, 0.1, 0.7, 0.03])
ax_max = plt.axes([0.1, 0.15, 0.7, 0.03])
ax_gamma = plt.axes([0.1, 0.05, 0.7, 0.03])

cb = plt.colorbar(mappable=heat_map, ax=ax, label='$z=\mathrm{Sinc}(x, y)$')

slider_min = Slider(ax_min, 'Min', np.min(z), np.max(z), valinit=np.min(z))
slider_max = Slider(ax_max, 'Max', np.min(z), np.max(z), valinit=np.max(z))
slider_gamma = Slider(ax_gamma, '$\gamma$', 0, 3, 1)

def update(val):
    val_min = slider_min.val
    val_max = slider_max.val
    val_gamma = slider_gamma.val
#     norm = mpl.colors.Normalize(vmin=val_min, vmax=val_max)
    norm = mpl.colors.PowerNorm(val_gamma, vmin=val_min, vmax=val_max)
    heat_map.set_norm(norm)
    cb.update_normal(heat_map)
    fig.canvas.draw_idle()


slider_min.on_changed(update)
slider_max.on_changed(update)
slider_gamma.on_changed(update)

plt.show()
