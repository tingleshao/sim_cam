the_simulator.simulate(model, motion, args)
# this is the most core part of the camera simulator program
# contains the logic of perfofrming the simulation
#  try to make it as static as possible


class simulator:

    def __init__(self):
        print "you just initialized a simulator!"

    def simulate(model, motion, args):
        # do the simulation
        # model: information about the system
        # motion: user view point
        # args: other parameters
        time_length = len(motion)
        total_pixel = model.h * model.w
