 # plot_generator basically is a toolbox class with a lot of static mehtods for
 #   plotting stuff and it does not maintain a state.
import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np
import matplotlib
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

from PIL import  Image
from PIL import  ImageDraw
#import Image
#import ImageDraw

from matplotlib.patches import Rectangle

from motion import motion

class plot_generator:

    def __init__(self):
        print "you don't have to call me since I am a toolbox. "

    @staticmethod
    def plot_motion(motion, model):
        # put the view boxs (over time) above the scene, use a color mapping so
        # we can see the time transition
        data = plot_generator.get_data()
        print data
        img = Image.fromarray(data) # TODO: later change here to be
        #                               based on the first frame
        draw = ImageDraw.Draw(img)

        currentAxis = plt.gca()
        currentAxis.set_xlim([0, model.get_w()])
        currentAxis.set_ylim([0, model.get_h()])

#        currentAxis.set_xlim([0, 100])
    #    currentAxis.set_ylim([0, 100])
#        currentAxis.add_patch(Rectangle((0.4, 0.4), 0.2, 0.2,
#                                         alpha=1, facecolor='none'))
        color_lst = plot_generator.generate_color_spectrum(range(len(motion)))

        for i in xrange(len(motion)):
        #    plot_single_motion(motion[i], i, len(motion))
            m = motion[i]
            w = m.down_pt[0] - m.start_pt[0]
            h = m.down_pt[1] - m.start_pt[1]
            rect = plot_generator.get_rect(m.start_pt[0], m.start_pt[1], w, h, 0)
            print m.start_pt[0]/100.0
            print m.start_pt[1]/100.0
            print w/100.0
            print h/100.0
            currentAxis.add_patch(Rectangle((m.start_pt[0],
                                             m.start_pt[1]),
                                             w, h,
                                             alpha=1, facecolor='none',
                                             edgecolor=color_lst[i]))
            #draw.polygon([tuple(p) for p in rect], fill = 0)

    #    new_data = np.asarray(img)
    #    plt.imshow(new_data, cmap=plt.cm.gray)

        cmap = matplotlib.colors.ListedColormap(color_lst)
        bounds=range(len(motion)+1)
        cax = inset_axes(currentAxis, width="4%", height='70%', loc=4)
        cbar = matplotlib.colorbar.ColorbarBase(cax, cmap=cmap, boundaries=bounds)
        cax.yaxis.set_ticks_position('left')
        cbar.ax.set_yticklabels([str(i) for i in range(len(motion)+1)])
        cax.yaxis.set_label_position('left')
        cbar.set_label('time stamp')
        plt.show()

        return None

    @staticmethod
    def generate_color_spectrum(input_range):
        range_max = input_range[-1]
        color_spec = [i * 255 / range_max for i in input_range]
        print str(['%0.2X' % i for i in color_spec])
        color_str = ['#'+x+'ef39' for x in ['%0.2X' % i for i in color_spec]]
        return color_str

    @staticmethod
    def label(xy, text):
        # label function
        y = xy[1] - 0.15
        plt.text(xy[0], y, text, ha="center", family='sans-serif', size=14)

    @staticmethod
    def plot_single_motion(m, t, t_scale):
        # plot single motion (a rectangle)
        grid = np.mgrid[0.2:0.8:3j, 0.2:0.8:3j].reshape(2, -1).T
        patches = []
        rect = mpatches.Rectangle(grid[1]-[])
        patches.append(rect)
        colors = np.linspace(0, 1, len(patches))

        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        plt.axis('equal')
        plt.axis('off')
        plt.show()

    @staticmethod
    def get_rect(x, y, width, height, angle):
        rect = np.array([(0, 0), (width, 0), (width, height), (0, height), (0, 0)])
        theta = (np.pi / 180.0) * angle
        R = np.array([[np.cos(theta), -np.sin(theta)],
                      [np.sin(theta), np.cos(theta)]])
        offset = np.array([x, y])
        transformed_rect = np.dot(rect, R) + offset
        return transformed_rect

    @staticmethod
    def get_data():
        """Make an array for the demonstration."""
        X, Y = np.meshgrid(np.linspace(0, np.pi, 512), np.linspace(0, 2, 512))
        z = (np.sin(X) + np.cos(Y)) ** 2 + 0.25
        data = (255 * (z / z.max())).astype(int)
        data = np.uint8(data)
        return data

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

    @staticmethod
    def test_plot_motion():
        m0 = motion(0, (20, 80), (16, 13))
        m1 = motion(1, (10, 80), (16, 13))
        m2 = motion(2, (40, 80), (50, 13))
        motion_lst = [m0, m1, m2]
        plot_generator.plot_motion(motion_lst)




if __name__ == '__main__':
    #plot_generator.test_plot_rect()
    plot_generator.test_plot_motion()
