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
        if model.name == 'model0':
            time_length = len(motion)
            total_pixel = model.h * model.w

            h_over_time = []
            d_over_time = []
            header_size = args.header
            timeperiod = args.period
            curr_t = 0
            for i in xrange(time_length):
                curr_t += 1
                if curr_t == timeperiod:
                    curr_t = 0
                    curr_overhead += header_size
                    curr_overhead = total_pixel - (motion[i].down_pt[0] - motion[i].start_pt[0]) * (motion[i].down_pt[1] - motion[i].start_pt[1])
                h_over_time.append(curr_overhead)
                d_over_time.append(0)
        return h_over_time, d_over_time
