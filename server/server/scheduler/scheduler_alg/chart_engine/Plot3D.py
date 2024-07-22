import matplotlib.pyplot as plt
import numpy as np


from matplotlib import cm
from matplotlib.ticker import LinearLocator


def create_3d_plot(data, labels, title):
    # X = data[0]
    # Y = data[1]
    # Z = data[2]
    #
    #
    # fig = plt.figure()
    # ax = plt.axes(projection='3d')
    # ax.plot_trisurf(X, Y, Z, linewidth=0, antialiased=False)
    # ax.set_title(title)
    #
    # # ax.xlabel(labels[0])
    # # ax.ylabel(labels[1])
    # # ax.zlabel(labels[2])
    #
    # plt.show()

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    # Make data.
    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X ** 2 + Y ** 2)
    Z = np.sin(R)

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.02f}')

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()