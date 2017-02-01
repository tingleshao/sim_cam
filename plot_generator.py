 # plot_generator basically is a toolbox class with a lot of static mehtods for
 #   plotting stuff and it does not maintain a state.
import matplotlib.pyplot as plt
plt.rcdefaults()
import matplotlib
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button
from PIL import Image
from PIL import ImageDraw

from view import view
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.mplot3d import Axes3D
from operator import add


class plot_generator:
    def __init__(self):
        print "You just initialized a plot generator."

    @staticmethod
    def plot_views1d(views, model):
        # put the view segs over time above the scene, use a color mapping so
        # we can see the time series
        data = plot_generator.get_data()
        print "plot view 1d data: " + str(data)
        currentAxis = plt.gca()
        max_len = 0
        for i in xrange(len(views)):
            v = views[i]
            curr_len = v.end
            if curr_len > max_len:
                max_len = curr_len
        currentAxis.set_xlim([0, max_len+20])
        currentAxis.set_ylim([0, len(views) * 10 + 10])

        color_lst = plot_generator.generate_color_spectrum(range(len(views)))
 #       color_lst = plot_generator.generate_color_spectrum(range(1))
        for i in xrange(len(views)):
            v = views[i]
            start = v.get_start()
            end = v.get_end()
            seg = plot_generator.get_segment(start, end)
            print start
            print end
            currentAxis.add_patch(Rectangle((v.start,
                                             i*10),
                                             v.start-v.end, 1,
                                             alpha=1, facecolor='none',
                                             edgecolor=color_lst[i]))
        cmap = matplotlib.colors.ListedColormap(color_lst)
        bounds = range(len(views)+1)
        cax = inset_axes(currentAxis, width="4%", height='70%', loc=4)
    #    cbar = matplotlib.colorbar.ColorbarBase(cax, cmap=cmap, boundaries=bounds)
        cbar = matplotlib.colorbar.ColorbarBase(cax, cmap=cmap)
        cax.yaxis.set_ticks_position('left')
        cax.yaxis.set_label_position('left')
    #    cbar.set_label('Income (,000s)')

    @staticmethod
    def get_segment(start, end):
        seg = np.array([start, end])
        return seg

    @staticmethod
    def plot_views(motion, model):
        # put the view boxs over time above the scene, use a color mapping so
        # we can see the time series
        data = plot_generator.get_data()
        print data
        img = Image.fromarray(data) # TODO: later change here to be
        #                               based on the first frame
        draw = ImageDraw.Draw(img)
        currentAxis = plt.gca()
        currentAxis.set_xlim([0, model.get_w()])
        currentAxis.set_ylim([0, model.get_h()])

        color_lst = plot_generator.generate_color_spectrum(range(len(motion)))

        for i in xrange(len(motion)):
            m = motion[i]
            w = m.down_pt[0] - m.start_pt[0]
            h = m.down_pt[1] - m.start_pt[1]
            rect = plot_generator.get_rect(m.start_pt[0], m.start_pt[1], w, h, 0)
        # TODO: consider removing these prints
            print m.start_pt[0]/100.0
            print m.start_pt[1]/100.0
            print w/100.0
            print h/100.0
            currentAxis.add_patch(Rectangle((m.start_pt[0],
                                             m.start_pt[1]),
                                             w, h,
                                             alpha=1, facecolor='none',
                                             edgecolor=color_lst[i]))
        # TODO: here has some strange stupid stuff going on
        # TODO: what are those?

        cmap = matplotlib.colors.ListedColormap(color_lst)
        bounds = range(len(motion)+1)
        cax = inset_axes(currentAxis, width="8%", height='70%', loc=4)
        cbar = matplotlib.colorbar.ColorbarBase(cax, cmap=cmap, boundaries=bounds)
        cax.yaxis.set_ticks_position('left')
        cax.yaxis.set_label_position('left')
        cbar.set_label('Income (,000s)')

    @staticmethod
    def generate_color_spectrum(input_range):
        range_max = input_range[-1]
        color_spec = [i * 255 / range_max for i in input_range]
        print str(['%0.2X' % i for i in color_spec])
        color_str = ['#'+x+'ef39' for x in ['%0.2X' % i for i in color_spec]]
        return color_str

    @staticmethod
    def generate_single_color():
        return None

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

    @staticmethod
    def plot_history(history):
    # plot the history using 3D cubes
        for h in history:
            plot_cube(h)

    @staticmethod
    def plot_tile_cube(tile_ids):
        i_s = [0, 1, 2, 3]
        # similar to plot_cube, except that the alpha for each block is based on tile id
        point_base = np.array([[0, 0, 0],
                               [1, 0, 0],
                               [1, 1, 0],
                               [0, 1, 0],
                               [0, 0, 1],
                               [1, 0, 1],
                               [1, 1, 1],
                               [0, 1, 1]])
        shifts = [[0, 0, 0], [1, 0, 0], [0, 0, -1], [1, 0, -1]]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for i in i_s:
            if i == 0:
                r = [0, 1]
            elif i == 1:
                r = [1, 2]
            elif i == 2:
                r = [0, 1]
            if i == 0:
                X, Y = np.meshgrid([0, 1], [0, 1])
            if i == 1:
                X, Y = np.meshgrid([1, 2], [0, 1])
            if i == 2:
                X, Y = np.meshgrid([0, 1], [0, 1])
            if i == 3:
                X, Y = np.meshgrid([1, 2], [0, 1])
            print "X: " + str(X)
            print "Y: " + str(Y)

            color0 = 1 if 0 in tile_ids else 0.1
            color1 = 1 if 1 in tile_ids else 0.1
            color2 = 1 if 2 in tile_ids else 0.1
            color3 = 1 if 3 in tile_ids else 0.1

            if i == 0:
                ax.plot_surface(X, Y, 1, alpha=color0)
                ax.plot_surface(X, Y, 0, alpha=color0)
                ax.plot_surface(X, 0, Y, alpha=color0)
                ax.plot_surface(X, 1, Y, alpha=color0)
                ax.plot_surface(0, X, Y, alpha=color0)
                ax.plot_surface(1, X, Y, alpha=color0)
            elif i == 1:
                ax.plot_surface(X, Y, 1, alpha=color1)
                ax.plot_surface(X, Y, 0, alpha=color1)
                ax.plot_surface(X, 0, Y, alpha=color1)
                ax.plot_surface(X, 1, Y, alpha=color1)
                ax.plot_surface(2, [[0, 1],[0, 1]], Y, alpha=color1)
                ax.plot_surface(1, [[0, 1],[0, 1]], Y, alpha=color1)
            elif i == 2:
                ax.plot_surface(X, Y, 0, alpha=color2)
                ax.plot_surface(X, Y, -1, alpha=color2)
                ax.plot_surface(X, 0, [[-1, -1],[0, 0]], alpha=color2)
                ax.plot_surface(X, 1, [[-1, -1],[0, 0]], alpha=color2)
                ax.plot_surface(1, X, [[-1, -1],[0, 0]], alpha=color2)
                ax.plot_surface(0, X, [[-1, -1],[0, 0]], alpha=color2)
            elif i == 3:
                ax.plot_surface(X, Y, 0, alpha=color3)
                ax.plot_surface(X, Y, -1, alpha=color3)
                ax.plot_surface(X, 0, [[-1, -1], [0, 0]], alpha=color3)
                ax.plot_surface(X, 1, [[-1, -1],[0, 0]], alpha=color3)
                ax.plot_surface(2, [[0, 1],[0, 1]], [[-1, -1],[0, 0]], alpha=color3)
                ax.plot_surface(1, [[0, 1],[0, 1]], [[-1, -1],[0, 0]], alpha=color3)
            points = np.array([map(add, p, shifts[i])  for p in point_base])
            print points
            ax.scatter3D(points[:,0], points[:,1], points[:,2])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()

    @staticmethod
    def plot_tile_cube_over_time(tilehistory, fig):
        tileidhistory = [[i.id for i in tiles] for tiles in tilehistory]
        level0_tileidhistory = [filter(lambda x: x < 4, tiles) for tiles in tileidhistory]
        callback = Index(level0_tileidhistory, fig)
        axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        bnext = Button(axprev, 'Next')
        bnext.on_clicked(callback.next)
        bprev = Button(axnext, 'Previous')
        bprev.on_clicked(callback.prev)
        plt.show()

    @staticmethod
    def plot_cube(i_s, fig):
        # for a cube, needs to have the 8 points
        point_base = np.array([[0, 0, 0],
                           [1, 0, 0],
                           [1, 1, 0],
                           [0, 1, 0],
                           [0, 0, 1],
                           [1, 0, 1],
                           [1, 1, 1],
                           [0, 1, 1]])
        shifts = [[0, 0, 0], [1, 0, 0], [0, 0, -1], [1, 0, -1]]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for i in i_s:
            if i == 0:
                r = [0, 1]
            elif i == 1:
                r = [1, 2]
            elif i == 2:
                r = [0, 1]
            if i == 0:
                X, Y = np.meshgrid([0, 1], [0, 1])
            if i == 1:
                X, Y = np.meshgrid([1, 2], [0, 1])
            if i == 2:
                X, Y = np.meshgrid([0, 1], [0, 1])
            if i == 3:
                X, Y = np.meshgrid([1, 2], [0, 1])
            print "X: " + str(X)
            print "Y: " + str(Y)
            if i == 0:
                ax.plot_surface(X, Y, 1, alpha=0.5)
                ax.plot_surface(X, Y, 0, alpha=0.5)
                ax.plot_surface(X, 0, Y, alpha=0.5)
                ax.plot_surface(X, 1, Y, alpha=0.5)
                ax.plot_surface(0, X, Y, alpha=0.5)
                ax.plot_surface(1, X, Y, alpha=0.5)
            elif i == 1:
                ax.plot_surface(X, Y, 1, alpha=0.1)
                ax.plot_surface(X, Y, 0, alpha=0.2)
                ax.plot_surface(X, 0, Y, alpha=0.3)
                ax.plot_surface(X, 1, Y, alpha=0.4)
                ax.plot_surface(2, [[0, 1],[0, 1]], Y, alpha=0.5)
                ax.plot_surface(1, [[0, 1],[0, 1]], Y, alpha=0.6)
            elif i == 2:
                ax.plot_surface(X, Y, 0, alpha=0.5)
                ax.plot_surface(X, Y, -1, alpha=0.5)
                ax.plot_surface(X, 0, [[-1, -1],[0, 0]], alpha=0.5)
                ax.plot_surface(X, 1, [[-1, -1],[0, 0]], alpha=0.5)
                ax.plot_surface(1, X, [[-1, -1],[0, 0]], alpha=0.5)
                ax.plot_surface(0, X, [[-1, -1],[0, 0]], alpha=0.5)
            elif i == 3:
                ax.plot_surface(X, Y, 0, alpha=0.5)
                ax.plot_surface(X, Y, -1, alpha=0.5)
                ax.plot_surface(X, 0, [[-1, -1], [0, 0]], alpha=0.5)
                ax.plot_surface(X, 1, [[-1, -1],[0, 0]], alpha=0.5)
                ax.plot_surface(2, [[0, 1],[0, 1]], [[-1, -1],[0, 0]], alpha=0.5)
                ax.plot_surface(1, [[0, 1],[0, 1]], [[-1, -1],[0, 0]], alpha=0.5)
            points = np.array([map(add, p, shifts[i])  for p in point_base])
            print points
            ax.scatter3D(points[:,0], points[:,1], points[:,2])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()

    @staticmethod
    def plot_tile_scale():
        # plot the bytes per second feed into the decoder vs. tiles and scales
        zoom_in = np.array([1440, 1440, 1440, 1440, 1440, 6000])
        zoom_out = np.array([5760, 1440, 1440, 5760, 1440, 5760])
        ind =  np.arange(6)  # 210 211 212 220 221 110
        width = 0.35
        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, zoom_in, width , color='r')
        rects2 = ax.bar(ind+0.35, zoom_out,  width, color='y')

        ax.set_ylabel('bandwidth')
        ax.set_title('requred bandwidth for different tile & scale settings')
        ax.set_xticks(ind+width)
        ax.set_xticklabels(('210', '211', '212', '220', '221', '110'))
        ax.set_ylim(0,9000)
        ax.legend((rects1[0], rects2[0]), ('zoom_in', 'zoom_out'))

        plot_generator.autolabel(rects1, ax)
        plot_generator.autolabel(rects2, ax)

        plt.show()

    @staticmethod
    def autolabel(rects, ax):
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%d' % int(height),
                    ha='center', va='bottom')


class Index(object):
    ind = 0

    def __init__(self, tileidhistory, fig):
        self.tileidhistory = tileidhistory
        print "\n\n\ntile id history: \n" + str(tileidhistory) + "\n\n\n"
        self.ind = 0
        self.fig = fig

    @staticmethod
    def plot_tile_cube(tile_ids, fig):
        i_s = [0, 1, 2, 3]
        # similar to plot_cube, except that the alpha for each block is based on tile id
        point_base = np.array([[0, 0, 0],
                               [1, 0, 0],
                               [1, 1, 0],
                               [0, 1, 0],
                               [0, 0, 1],
                               [1, 0, 1],
                               [1, 1, 1],
                               [0, 1, 1]])
        shifts = [[0, 0, 0], [1, 0, 0], [0, 0, -1], [1, 0, -1]]
        ax = fig.add_subplot(223, projection='3d')
        for i in i_s:
            if i == 0:
                r = [0, 1]
            elif i == 1:
                r = [1, 2]
            elif i == 2:
                r = [0, 1]
            if i == 0:
                X, Y = np.meshgrid([0, 1], [0, 1])
            if i == 1:
                X, Y = np.meshgrid([1, 2], [0, 1])
            if i == 2:
                X, Y = np.meshgrid([0, 1], [0, 1])
            if i == 3:

                X, Y = np.meshgrid([1, 2], [0, 1])
            print "X: " + str(X)
            print "Y: " + str(Y)

            color0 = 1 if 0 in tile_ids else 0.1
            color1 = 1 if 1 in tile_ids else 0.1
            color2 = 1 if 2 in tile_ids else 0.1
            color3 = 1 if 3 in tile_ids else 0.1

            if i == 0:
                ax.plot_surface(X, Y, 1, alpha=color0)
                ax.plot_surface(X, Y, 0, alpha=color0)
                ax.plot_surface(X, 0, Y, alpha=color0)
                ax.plot_surface(X, 1, Y, alpha=color0)
                ax.plot_surface(0, X, Y, alpha=color0)
                ax.plot_surface(1, X, Y, alpha=color0)
            elif i == 1:
                ax.plot_surface(X, Y, 1, alpha=color1)
                ax.plot_surface(X, Y, 0, alpha=color1)
                ax.plot_surface(X, 0, Y, alpha=color1)
                ax.plot_surface(X, 1, Y, alpha=color1)
                ax.plot_surface(2, [[0, 1],[0, 1]], Y, alpha=color1)
                ax.plot_surface(1, [[0, 1],[0, 1]], Y, alpha=color1)
            elif i == 2:
                ax.plot_surface(X, Y, 0, alpha=color2)
                ax.plot_surface(X, Y, -1, alpha=color2)
                ax.plot_surface(X, 0, [[-1, -1],[0, 0]], alpha=color2)
                ax.plot_surface(X, 1, [[-1, -1],[0, 0]], alpha=color2)
                ax.plot_surface(1, X, [[-1, -1],[0, 0]], alpha=color2)
                ax.plot_surface(0, X, [[-1, -1],[0, 0]], alpha=color2)
            elif i == 3:
                ax.plot_surface(X, Y, 0, alpha=color3)
                ax.plot_surface(X, Y, -1, alpha=color3)
                ax.plot_surface(X, 0, [[-1, -1], [0, 0]], alpha=color3)
                ax.plot_surface(X, 1, [[-1, -1],[0, 0]], alpha=color3)
                ax.plot_surface(2, [[0, 1],[0, 1]], [[-1, -1],[0, 0]], alpha=color3)
                ax.plot_surface(1, [[0, 1],[0, 1]], [[-1, -1],[0, 0]], alpha=color3)
            points = np.array([map(add, p, shifts[i])  for p in point_base])
            print points
            ax.scatter3D(points[:,0], points[:,1], points[:,2])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

    def next(self, event):
        self.ind += 1
        self.plot_tile_cube(self.tileidhistory[self.ind%4], self.fig)
        plt.draw()

    def prev(self, event):
        self.ind -= 1
        self.plot_tile_cube(self.tileidhistory[self.ind%4], self.fig)
        plt.draw()


if __name__ == '__main__':
    #plot_generator.test_plot_rect()
    #plot_generator.test_plot_motion()
 #   plot_generator.plot_cube([0, 1, 2, 3])
#    plot_generator.plot_tile_cube([0, 2])
    plot_generator.plot_tile_scale()
