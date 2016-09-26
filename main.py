# sim_cam
# the purpose for writing this software is to enable fast simulation of
# Aqueti camera system behavior

# The progam would take a list of parameters, include
#   available bandwidth w
#   xxx

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
    parser.add_argument("--verbosity", help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()
    if args.verbosity:
        print "verbosity turned on"

if __name__ == '__main__':
    main()
