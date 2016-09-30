# this is the most core part of the camera simulator program
# contains the logic of perfofrming the simulation
#  try to make it as static as possible
from model import model
from motion import motion


class simulator:

    def __init__(self):
        print "you just initialized a simulator!"

    @staticmethod
    def simulate(model, motion, args):
        # do the simulation
        # model: information about the system
        # motion: user view point
        # args: other parameters
        if model.get_name() == 'model0':
            time_length = len(motion)
            total_pixel = model.h * model.w

            h_over_time = []
            d_over_time = []
            header_size = args.get("header")
            trunk_size = args.get("trunk_size")
            curr_t = 0

            for i in xrange(time_length):
                curr_t += 1
                curr_overhead = 0
                if curr_t == trunk_size:
                    curr_t = 0
                    curr_overhead += header_size
                    print "total_pixel: " + str(total_pixel)
                    print "actual_pixel: " + str((motion[i].down_pt[0] - motion[i].start_pt[0]) * (motion[i].down_pt[1] - motion[i].start_pt[1]))
                curr_overhead += total_pixel - (motion[i].down_pt[0] - motion[i].start_pt[0]) * (motion[i].down_pt[1] - motion[i].start_pt[1])
                h_over_time.append(curr_overhead)
                d_over_time.append(0)
        return h_over_time, d_over_time


def test():
    model0 = model("model0", 100, 100)
    m0 = motion(0, (20, 80), (16, 13))
    m1 = motion(1, (10, 70), (16, 20))
    m2 = motion(2, (40, 75), (50, 18))
    m3 = motion(3, (45, 55), (20, 10))
    motions = [m0, m1, m2, m3]
    args = {"header": 10, "trunk_size": 5}
    h_over_time, d_over_time = simulator.simulate(model0, motions, args)
    print "h_over_time: " + str(h_over_time)
    print "d_over_time: " + str(d_over_time)

if __name__ == '__main__':
    test()
