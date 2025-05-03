from math import comb
import numpy as np
import matplotlib.pyplot as mpl
import time


def rbezier(
        u, v,
        points:np.ndarray,
        poids:np.ndarray
    ) -> np.ndarray:

    n, m = points.shape[1] - 1, points.shape[0] - 1
    bernstein_u = np.array([comb(n, i) * u**i * (1 - u)**(n - i) for i in range(n + 1)])
    bernstein_v = np.array([comb(m, j) * v**j * (1 - v)**(m - j) for j in range(m + 1)])
    bernstein = np.linalg.outer(bernstein_u, bernstein_v) * poids
    xyz = np.dot(bernstein.ravel(), points.reshape(-1, 3))
    rationnelle = bernstein.sum()

    return xyz / rationnelle if rationnelle != 0 else xyz


def afficher(
        points:np.ndarray,
        poids:np.ndarray,
    ) -> None:

    a = time.time()
    fig = mpl.figure(figsize=(8,8))
    ax = fig.add_subplot(projection="3d")

    ISOCOURBES = 40+1

    us = vs = np.linspace(0, 1, ISOCOURBES)
    uvs = np.r_[[us, vs]]

    for u in us:
        tv = np.asarray([rbezier(u, v, points, poids) for v in uvs[0]])
        ax.plot(*tv.T, ls="-", lw=1.0, color="gray", antialiased=True)

    for v in vs:
        tu = np.asarray([rbezier(u, v, points, poids) for u in uvs[1]])
        ax.plot(*tu.T, ls="-", lw=1.0, color="gray", antialiased=True)

    pc0 = points[:, :, 0]
    pc1 = points[:, :, 1]
    pc2 = points[:, :, 2]

    ax.scatter(*points.reshape(-1, 3).T, color="k", edgecolor="k", s=100)
    
    n, m = points.shape[1], points.shape[0]

    tuple(ax.plot(pc0[i, :], pc1[i, :], pc2[i, :], ls="dotted", dashes=(2,4), \
            alpha=0.5, lw=0.75, color="k") for i in range(m))

    tuple(ax.plot(pc0[:, j], pc1[:, j], pc2[:, j], ls="dotted", dashes=(2,4), \
            alpha=0.5, lw=0.75, color="k") for j in range(n))

    b = time.time()
    print("temps :", str(b-a), "s")

    fig.tight_layout()
    ax.set_axis_off()
    ax.view_init(elev=15, azim=-20)
    ax.set_box_aspect(None, zoom=1.25)
    mpl.show()


if __name__ == "__main__":
    points = np.array([
        [[-15, 0, 500], [5, 0, 800], [25, 0, 800], [45, 0, 500]],
        [[-15, 1, 800], [5, 1, 1400], [25, 1, 1400], [45, 1, 800]],
        [[-15, 2, 800], [5, 2, 1400], [25, 2, 1400], [45, 2, 800]],
        [[-15, 3, 500], [5, 3, 800], [25, 3, 800], [45, 3, 500]]
    ], dtype=np.float16)

    w = 15
    poids = np.array([
        [1, w, w, 1],
        [w, w*4, w*4, w],
        [w, w*4, w*4, w],
        [1, w, w, 1]
    ], dtype=np.float16)

    afficher(points, poids)
