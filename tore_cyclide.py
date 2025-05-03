import numpy as np
import matplotlib.pyplot as mpl

def tore(r1:float = 1,
        r2:float = 0.5,
        lo:float = 50,
        la:float = 50) -> tuple:
    
    u = np.linspace(0, 2 * np.pi, lo)
    v = np.linspace(0, 2 * np.pi, la)
    u, v = np.meshgrid(u, v)
    x = (r1 + r2 * np.cos(u)) * np.cos(v)
    y = (r1 + r2 * np.cos(u)) * np.sin(v)
    z = r2 * np.sin(u)

    return x, y, z

def cyclide(a:float = 3,
        b:float = 2.2,
        c:float = 1.25,
        d:float = 2.2,
        lo:float = 50,
        la:float = 50) -> tuple:
    
    u = np.linspace(0, 2 * np.pi, lo)
    v = np.linspace(0, 2 * np.pi, la)
    u, v = np.meshgrid(u, v)
    x = (d * (c - a*np.cos(u) * np.cos(v)
        + b**2 * np.cos(u))) / (a - c*np.cos(u)
        * np.cos(v))
    y = (b * np.sin(u) * (a - d * np.cos(v))) \
        / (a - c * np.cos(u) * np.cos(v))
    z = (b * np.sin(v) * (c * np.cos(u) - d)) \
        / (a - c * np.cos(u) * np.cos(v))
    
    return x, y, z

xt, yt, zt = tore()
xc, yc, zc = cyclide()

fig, axs = mpl.subplots(1, 2, figsize=(12,6))
fig.tight_layout()

axs[0] = fig.add_subplot(121, projection="3d")
axs[0].set_xscale("linear")
axs[0].set_yscale("linear")
axs[0].set_aspect("equal")
axs[0].set_xlim(-1,1)
axs[0].set_ylim(-1,1)
axs[0].set_zlim(-1,1)
axs[0].set_box_aspect(None, zoom=1)
axs[0].view_init(40, -10, 0)
axs[0].plot_surface(xt, yt, zt,cmap="gray",antialiased=True)
axs[0].axis("off")

axs[1] = fig.add_subplot(122, projection="3d")
axs[1].set_xscale("linear")
axs[1].set_yscale("linear")
axs[1].set_aspect("equal")
axs[1].set_box_aspect(None, zoom=1.5)
axs[1].view_init(60, -50, 0)
axs[1].plot_surface(xc, yc, zc,cmap="gray",antialiased=True)
axs[1].axis("off")

mpl.show()
