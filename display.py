import matplotlib.pyplot as plt
import numpy as np


def setGrid(pbounds, resolution):
    global xy, X, Y, n_dim
    n_dim = resolution
    
    # Setup the grid to plot on
    x = np.linspace(pbounds['x'][0], pbounds['x'][1], n_dim)
    y = np.linspace(pbounds['x'][0], pbounds['x'][1], n_dim)
    xy = np.array([[x_i, y_j] for y_j in y for x_i in x])
    X, Y = np.meshgrid(x, y)
    return X, Y

def getTargetsFromGP(optimizer):
    global Z

    # Evaluate the actual functions on the grid
    Z = np.reshape(optimizer._gp.sample_y(xy), (-1, n_dim))
    return Z

def getTargetsFromFunc(target_function):
    global Z
    Z = np.empty(len(xy))

    # Evaluate the actual functions on the grid
    for i in range(len(xy)):
        Z[i] = target_function(xy[i,0], xy[i,1])
    Z = np.reshape(Z, (-1, n_dim))
    return Z

def contourPlot(optimizer):
    # plots the contours defined by Z, along with the points held by the optimizer
    titleText = "Target"
    
    fig, axs = plt.subplots(constrained_layout=True, figsize=(6,6))

    axs.set_aspect("equal")
    axs.set_title(titleText)
    axs.set_xlabel('x')
    axs.set_ylabel('y')

    # Extract & unpack the optimization results
    max_ = optimizer.max
    res = optimizer.res
    x_ = np.array([r["params"]['x'] for r in res])
    y_ = np.array([r["params"]['y'] for r in res])

    Z_est = optimizer._gp.predict(xy).reshape(Z.shape)

    target_vbounds = np.min([Z, Z_est]), np.max([Z, Z_est])

    cp = axs.contourf(X, Y, Z, cmap=plt.cm.viridis, vmin=target_vbounds[0], vmax=target_vbounds[1])
    fig.colorbar(cp)

    axs.scatter(x_, y_, c='red', s=80, edgecolors='black')
    axs.scatter(max_["params"]['x'], max_["params"]['y'], s=80, c='green', edgecolors='black')

    plt.savefig('output.png')
    plt.show()

    return 0