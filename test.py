# This is the test for the simulation program
import main as main
import matplotlib.pyplot as plt
import numpy as np
import sys
from data_saver import data_saver
from model import model
from model_reader import model_reader
from view import view
from view import view1d
from plot_generator import plot_generator
from simulator import simulator


def test(test_number):
    # Test 0: 1 Layer, 2x2, 1024 x 768
    # Trivial strategy 1
    if test_number == 0:
        # read model data and view data
        model0 = model_reader.read_model('models/model0.json')
        motions = model_reader.read_views('models/model0.json')
        plt.subplot(2,2,1)
        # plot view data as a cascade of rectangles
        plot_generator.plot_motion(motions, model0)
        args = {"header": 10, "chunk_size": 5}
        # simulate the system behavior (including h over time and d over time)
        h_over_time, d_over_time, his, tilehistory = simulator.simulate(model0, motions, args)
        print "h_over_time: " + str(h_over_time)
        print "d_over_time: " + str(d_over_time)
        plt.subplot(2,2,2)
        plt.plot(h_over_time, 'bo-')
        plt.show()

    # Test 3: 2 Layers
    # Trivial strategy 2
    elif test_number == 1:
        model3 = model_reader.read_model('models/model3.json')
        print "model3 name: " + model3.get_name()
        motions = model_reader.read_views('models/model3.json')
        plot_generator.plot_motion(motions, model3)
        args = {"header": 10, "chunk_size": 2}
        h_over_time, d_over_time, his, tilehistory = simulator.simulate(model3, motions, args)
        print "h_over_time: " + str(h_over_time)
        print "d_over_time: " + str(d_over_time)
        plt.plot(h_over_time, 'bo-')
        plt.show()

    elif test_number == 2:
        model4 = model_reader.read_model('models/model4.json')
        print "model4 name: " + model4.get_name()
        motions = model_reader.read_views('models/model4.json')
        fig = plt.figure()
        fig.add_subplot(2,2,1)
        plot_generator.plot_motion(motions, model4)
        args = {"header": 10, "chunk_size": 2}
        h_over_time, d_over_time, his, tilehistory = simulator.simulate(model4, motions, args)
        print "h_over_time: " + str(h_over_time)
        print "d_over_time: " + str(d_over_time)
        fig.add_subplot(2,2,2)
        plt.plot(h_over_time, 'bo-')
        firstframe_level0_tiles = filter(lambda x: x < 4, [i.id for i in tilehistory[3]])
        print "tilehistory: " + str(tilehistory)
        print firstframe_level0_tiles
        plot_generator.plot_tile_cube_over_time(tilehistory, fig)
        plt.show()

    # 1D case
    elif test_number == 3 or test_number == 4:
        # read model1d model and views
        model1d = model_reader.read_model1d('models/model1d.json') if test_number == 3 else model_reader.read_model1d('models/model0_1d.json')
        views = model_reader.read_views1d('models/model1d.json') if test_number == 3 else model_reader.read_views1d('models/model0_1d.json')
        # plot the views
        fig = plt.figure()
        fig.add_subplot(2,2,1)
        plot_generator.plot_views1d(views, model1d)
        # run simulation
        args = {"header": 10, "chunk_size": 2} # TODO: what are those?
        h_over_time, d_over_time, his, tilehistory = simulator.simulate(model1d, views, args)
        print "h_over_time: " + str(h_over_time)
        print "d_over_time: " + str(d_over_time)
        fig.add_subplot(2,2,2)
        plt.plot(h_over_time, 'bo-')
        firstframe_level0_tiles = filter(lambda x: x < 4, [i.id for i in tilehistory[3]])
        print "tile history: " + str(tilehistory)
        print firstframe_level0_tiles
        plot_generator.plot_tile_cube_over_time(tilehistory, fig)
        plt.show()

    # 1D case large population simulation
    # in this case, the slice size s is still read from a json file
    # but, the views are generated from a probability distribution instead of reading from a json file
    elif test_number == 5 or test_number == 6:
        model1d = model_reader.read_model1d('models/model1d.json') if test_number == 5 else model_reader.read_model1d('models/model0_1d.json')
        views = model_reader.generate_views1d(10, 10, 2, 150)
        # plot the views
        fig = plt.figure()
        fig.add_subplot(2,2,1)
        plot_generator.plot_views1d(views, model1d)
        # run simulation
        args = {"header": 10, "chunk_size": 2} # TODO: what are those?
        h_over_time, d_over_time , his, tilehistory = simulator.simulate(model1d, views, args)
        print "h_over_time: " + str(h_over_time)
        print "d_over_time: " + str(d_over_time)
        fig.add_subplot(2,2,2)
        plt.plot(h_over_time, 'bo-')
        firstframe_level0_tiles = filter(lambda x: x < 4, [i.id for i in tilehistory[3]])
        print "tile history: " + str(tilehistory)
        print firstframe_level0_tiles
        plot_generator.plot_tile_cube_over_time(tilehistory, fig)
        plt.show()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        test_number = int(sys.argv[1])
        test(test_number)
