# This is the test for the simulation program
import main as main
import sys
from data_saver import data_saver
import numpy as np
import matplotlib.pyplot as plt
from model import model
from motion import motion
from simulator import simulator
from plot_generator import plot_generator

# TODO: later change this name "motion" to "view"
def test(test_number):
    # Test 0: 1 Layer, 2x2, 1024 x 768
    # Trivial strategy 1
    if test_number == 0:
        model0 = model("model0", 150, 100)
        m0 = motion(0, (1,1), (149, 149*2/3))
        m1 = motion(1, (19,13), (19+111, 13+(111*2/3)))
        m2 = motion(2, (56, 20), (56+65, 20+(65*2/3)))
        m3 = motion(3, (80, 30), (80+30, 30+20))

        motions = [m0, m1, m2, m3]
        plot_generator.plot_motion(motions, model0)
        args = {"header": 10, "trunk_size": 5}
        h_over_time, d_over_time = simulator.simulate(model0, motions, args)
        print "h_over_time: " + str(h_over_time)
        print "d_over_time: " + str(d_over_time)

        plt.plot(h_over_time, 'bo-')
        plt.show()
        #main.run()

    # Test 1: 2 Layers
    # Trivial strategy 1
    elif test_number == 1:
        main.run()

    # Test 2: 1 Layer
    # Trivial stategy 2
    elif test_number == 2:
        #model0 = model()
        main.run()

    # Test 3: 2 Layers
    # Trivial strategy 2
    elif test_number == 3:
        model3 = model("model3", 150, 100)
        m0 = motion(0, (1,1), (149, 149*2/3))
        m1 = motion(1, (19,13), (19+111, 13+(111*2/3)))
        m2 = motion(2, (56, 20), (56+65, 20+(65*2/3)))
        m3 = motion(3, (80, 30), (80+30, 30+20))
        #main.run()
        motions = [m0, m1, m2, m3]
        plot_generator.plot_motion(motions, model3)

        args = {"header": 10, "trunk_size": 2}
        h_over_time, d_over_time = simulator.simulate(model3, motions, args)

        print "h_over_time: " + str(h_over_time)
        print "d_over_time: " + str(d_over_time)

        plt.plot(h_over_time, 'bo-')
        plt.show()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        test_number = int(sys.argv[1])
        test(test_number)
