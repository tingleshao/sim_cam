 # plot_generator basically is a toolbox class with a lot of static mehtods for
 #   plotting stuff and it does not maintain a state.
import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection


class plot_generator:

    def __init__(self):
        print "you don't have to call me since I am a toolbox. "

    @staticmethod
    def plot_motion():
        # put the view boxs (over time) above the scene, use a color mapping so
        # we can see the time transition
        return None

    @staticmethod
    def label(xy, text):
        # label function
        y = xy[1] - 0.15
        plt.text(xy[0], y, text, ha="center", family='sans-serif', size=14)

    @staticmethod
    def test_plot_rect():
        # just try things out
        figs, ax = plt.subplots()
        grid = np.mgrid[0.2:0.8:3j, 0.2:0.8:3j].reshape(2, -1).T
        patches = []
        # add a rectangle
        rect = mpatches.Rectangle(grid[1]-[0.025, 0.05], 0.05, 0.1, ec="none")
        patches.append(rect)
        plot_generator.label(grid[1], "Rectangle")

        colors = np.linspace(0, 1, len(patches))
        collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3)
        collection.set_array(np.array(colors))
        ax.add_collection(collection)
#        ax.add_line(line)

        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        plt.axis('equal')
        plt.axis('off')
        plt.show()

if __name__ == '__main__':
    plot_generator.test_plot_rect()
