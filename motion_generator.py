# This class generates the motion (the user's view point) as the absolute view
#   window size.
# All different kinds of probability models can be given as argumentss to enable
#   different types of motion
# (Consider later: maybe besides giving the probablity model, an alternative way
# of doing  this could be specificing the application, such as "survelliance",
# "football game watching", etc.)
from numpy import random as random


class motion_generator:
    def __init__(self):
        self.distribution = "independent"
        self.w = w
        self.h = h
        print "motion generator generated?! Let's figure out"

    def set_distribution(self):
        self.distribution = distribution

    def set_w(self):
        self.w = w

    def set_h(self):
        self.h = h

    def generate_motion(self, motion_duration):
        # generates and returns a list of motion
        if self.distribution == "independent":
            x_s = [int i for i in random.rand(2) * w]
            x_s.sort()
            y_s = [int i for i in random.rand(2) * h]
            y_s.sort()
            start_x, end_x = x_s
            start_y, end_y = y_s
            return [motion(i, (start_x, start_y), (end_x, end_y)) for i in xrange(motion_duration)]
        if self.dsitribution == "gaussian":
            # do some 2D gaussian random sampling
            return []
        else:
            print "unknown distribution!"
            return None
