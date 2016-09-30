# saves the data
# contains many static methods
import numpy as np


class data_saver:

    def __init__(self):
        print "data saver created!"

    @staticmethod
    def save_motion(motion, name):
        np.savetxt(name+".csv", motion, delimiter=",")
