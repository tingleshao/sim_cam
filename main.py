# sim_cam
# the purpose for writing this software is to enable fast simulation of
# Aqueti camera system behavior

# The progam would take a list of parameters, include
#   available bandwidth w: the allowable bandwidth for the system to transmit
#     video data from server side to the client side.
#   alpha (a): the weight for the pixel overhead (H) term of the loss function
#   beta (b): the weight for the average delay (D) term of the loss function
#     (FYI, loss function: f(x) = aH + bD )
#      H = xxx
#      D = xxx
#   h: the size of the additional data append to each H264 trunk of data,
#   basically can be understood as header.

# (***) There should be multiple structural configurations about how the video
# stream is prepared.
# The proposed plan is: having three layers. Each later consists of 4 tiles (2x2)
# The current simulation program hard coded different video preparation structures
# a) single layer 2x2
# b) two layers 2x2
# c) three layters 2x2
# d) xxx (planned in the future)

# Besides the structure, there is also a choice in strategy on how to stream &
# cache the tiles. Currently I can think of 4 strategies:
# a) trivial strategy: transmit the 4 tiles for current view current layer
# b) trivial strategy 2: tranmit all the 20 tiles for two layers configuration
# c) better strategy: on L1, transmit the 4 tiles and the related tiles on L2;
#      on L2, transmit the 4 tiles and related tiles on L1
# d) better strategy: on L1, only transmit the 4 tiles; on L2, trnasmit the 4
#      tiles and related tiles on L1

# and outputs the system performance metric in terms of pixel overhead H and
# expected delay D as a function of time t

# if the user likes, the program can also plot the result as a curve
# if the user likes, the prgoram can also outputs a single value: aH + bD to
# simply indicate the overall system performance based on a and b.

# main python program that works as the entry point for the simulation software

import argparse


def main():
    print "hello world, this is sim_cam main program"
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbosity", help="""increase output verbosity""",
                        action="store_true")
    parser.add_argument("-w", help="""the allowable bandwidth for the system
                        to transmit video data from server side to the client
                        side""", type=int)
    parser.add_argument("-a", help="""the weight for the pixel overhead term
                        of the loss function""", type=int)
    parser.add_argument("-b", help="""the weight for the average delay term of
                        the loss function""", type=int)
    parser.add_argument("-h", help="""size of the H264 header""", type=int)
    args = parser.parse_args()
    if args.verbosity:
        print "verbosity turned on"

if __name__ == '__main__':
    main()
