# this is the most core part of the camera simulator program
# contains the logic of perfofrming the simulation
#  try to make it as static as possible
from model import model
from motion import motion
from tile import tile
from logger import logger

class simulator:

    def __init__(self):
        print "you just initialized a simulator!"

    # TODO: change the h number to be the ration (p0-p1) / p0 ...
    @staticmethod
    def simulate(model, motion, args):
        # do the simulation
        # model: information about the system
        # motion: user view point
        # args: other parameters
        h_over_time = []
        d_over_time = []
        if model.get_name() == 'model0':
            time_length = len(motion)
            total_pixel = model.h * model.w
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
                curr_overhead += simulator.compute_ratio_overhead(total_pixel, (motion[i].down_pt[0] - motion[i].start_pt[0]) * (motion[i].down_pt[1] - motion[i].start_pt[1]))
                h_over_time.append(curr_overhead)
                d_over_time.append(0)

        elif model.get_name() == 'model3':
            curr_bdwh = 10000
            ahead_limit = 2
            # model3: 2 layers, only transmit the required tiles in any level, also transmit related tiles in the other level
            time_length = len(motion)
            total_pixel = 1
            header_size = args.get("header")
            trunk_size = args.get("trunk_size")
            # keep an map to save all the transmitted data for the current time
            # for any time period x, we keep an array of recived tile index
            # so that at any time point
            #   we can predict if we need to transmit the tile or not
            transmitted_windows_map = {}

            for i in xrange(time_length):
                curr_overhead = 0
                curr_view = motion[i]
                tiles = simulator.get_tiles(curr_view, model)
                # update the transmitted_windows_map
                transmitted_tiles = []
                print "tiles: " + str(tiles)
                for tile in tiles:
                    if tile.get_id() not in transmitted_windows_map.keys():
                         transmitted_windows_map[tile.get_id()] = trunk_size
                         transmitted_tiles.append(tile)
                         print transmitted_windows_map
                # reduce life time for all tiles
                for tile_id in transmitted_windows_map.keys():
                    if transmitted_windows_map[tile_id] == 1:
                        transmitted_windows_map.pop(tile_id, None)
                    else:
                        transmitted_windows_map[tile_id] = transmitted_windows_map[tile_id] - 1

                actual_pixel = curr_view.get_pixels() # actual number of pixels get displayed
                print "total_pixel: " + str(total_pixel)
                print "actual_pixel: " + str(actual_pixel)
                curr_overhead += simulator.compute_ratio_overhead(total_pixel, actual_pixel)
                h_over_time.append(curr_overhead)
                d_over_time.append(0)

        elif model.get_name() == 'model4':
            # XXX: I am doing this for the aggressive transmission ( the most common one )
            time_length = len(motion)
            total_pixel = 1
            header_size = args.get("header")
            trunk_size = args.set("trunk_size")
            transmitted_windows_map = {}
            for i in xrange(time_length):
                curr_overhead = 0
                curr_view = motion[i]
                tiles = simulator.get_tiles(curr_view, model)
                transmitted_tiles = []
                print "tiles: " + str(tiles)
                for tile in tiles:
                    if tile.get(id) not in transmitted_windows_map.keys():
                        transmitted_windows_map[tile.get_id()] = trunk_size
                        transmitted_tiles.append(tile)
                        print transmitted_windows_map
                for tile_id in transmitted_windows_map.keys():
                    if transmitted_windows_map[tile_id] == 1:
                        transmitted_windows_map.pop(tile_id, None)
                    else:
                        transmitted_windows_map[tile_id] = transmitted_windows_map[tile_id] - 1

                total_pixel = simulator.get_transmitted_pixels(transmitted_tiles, trunk_size, model.get_w(), model.get_h())
                curr_bdwh, total_pixel = comsume_remaining_bandwidth(curr_bdwh, total_pixel, transmitted_windows_map, transmitted_tiles)
                actual_pixel = curr_view.get_pixels() # actual number of pixels get displayed
                print "total_pixel: " + str(total_pixel)
                print "actual_pixel: " + str(actual_pixel)
                curr_overhead += simulator.compute_ratio_overhead(total_pixel, actual_pixel)
                h_over_time.append(curr_overhead)
                d_over_time.append(0)

  # TODO: can we put the strategy into a JSON?
        return h_over_time, d_over_time


    @staticmethod
    def compute_minus_overhead(total_pixel, actual_pixel):
        return total_pixel - actual_pixel

    @staticmethod
    def compute_ratio_overhead(total_pixel, actual_pixel):
        return float(total_pixel - actual_pixel) / float(actual_pixel)

    @staticmethod
    def get_tiles(curr_view, model):
        model_w = model.get_w()
        model_h = model.get_h()
        # for now assume two tiles  TODO:  same w-h ratio as the model (could not be true!, then the model has to specify a tile size)
        tiles = []
        if curr_view.get_w() < model_w/2:
            print "ws:"
            print curr_view.get_w()
            print model_w
            level = 1
        else:
            level = 0
        if level == 0:
            tiles = [tile(0), tile(1), tile(2), tile(3)]
            level1_tile_w = model_w / 4
            level1_tile_h = model_h / 4
            for x in xrange(4):
                for y in xrange(4):
                    curr_tile_upper_left = [level1_tile_w * x, level1_tile_h * y]
                    curr_tile_lower_right = [curr_tile_upper_left[0] + level1_tile_w, curr_tile_upper_left[1] + level1_tile_h]
                    if simulator.are_rects_overlap(curr_tile_upper_left, curr_tile_lower_right, curr_view.get_start_pt(), curr_view.get_down_pt()):
                        tiles.append(tile(4+4*y+x))
        elif level == 1:
            level1_tile_w = model_w / 4
            level1_tile_h = model_h / 4
            for x in xrange(4):
                for y in xrange(4):
                    # see if this tile has any overlapping with the curr_view
                    curr_tile_upper_left = [level1_tile_w * x, level1_tile_h * y]
                    curr_tile_lower_right = [curr_tile_upper_left[0] + level1_tile_w, curr_tile_upper_left[1] + level1_tile_h]
                    if simulator.are_rects_overlap(curr_tile_upper_left, curr_tile_lower_right, curr_view.get_start_pt(), curr_view.get_down_pt()):
                        tiles.append(tile(4+4*y+x))
                    else:
                        logger.debug_print("debug", "no overlapping!")
            # depends on the x, y, also allocate the tiles on level 0
            level0_tile_w = model_w / 2
            level0_tile_h = model_h / 2
            for x in xrange(2):
                for y in xrange(2):
                    curr_tile_upper_left = [level0_tile_w * x, level0_tile_h * y]
                    curr_tile_lower_right = [curr_tile_upper_left[0] + level0_tile_w, curr_tile_upper_left[1] + level0_tile_h]
                    if simulator.are_rects_overlap(curr_tile_upper_left, curr_tile_lower_right, curr_view.get_start_pt(), curr_view.get_down_pt()):
                        tiles.append(tile(2*y+x))
        return tiles

    @staticmethod
    def are_rects_overlap(l1, r1, l2, r2):
        true_l1 = [l1[0], r1[1]]
        true_r1 = [r1[0], l1[1]]
        true_l2 = [l2[0], r2[1]]
        true_r2 = [r2[0], l2[1]]
        if (true_l1[0] > true_r2[0] or true_l2[0] > true_r1[0]):
            return False
        if (true_l1[1] < true_r2[1] or true_l2[1] < true_r1[1]):
            return False
        return True

    @staticmethod
    def get_transmitted_pixels(tiles, trunk_size, model_w ,model_h):
        #  if condition on levels
        level0_w = model_w / 2
        level0_h = model_h / 2
        level1_w = level0_w / 2
        level1_h = level0_h / 2
        total_pixels = 0

        print tiles
        for tile in tiles:
            if tile.get_id() < 4: #level0
                total_pixels += level0_w * level0_h
            elif tile.get_id() < 20:
                total_pixels += level1_w * level1_h
        return total_pixels

    def xxx():
        return "xxx"

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
