# this is the most core part of the camera simulator program
# contains the logic of perfofrming the simulation
#  try to make it as static as possible

# Definitions:
# Motion -> View
# Motions -> List of Views
# Model -> Strategy
# args: -> system status


from model import model
from model1d import model1d_new
from model1d import model1d
from motion import view
from tile import tile, tile1d
from logger import logger

class simulator:

    def __init__(self):
        print "you just initialized a simulator!"

    # TODO: change the h number to be the ratio (p0-p1) / p0 ...
    @staticmethod
    def simulate(model, motion, args):
        # do the simulation
        # model: information about the system
        # motion: user view region
        # args: other parameters
        h_over_time = []
        d_over_time = []
        # history format:
        # at current time point, which set of tiles hase been transmitted (with lifetime)
        history_lst = []
        tile_history = []

        time_length = len(motion)
        header_size = args.get("header")
        chunk_size = args.get("chunk_size")
        print "simulating " + model.get_name()
        if model.get_name() == 'model0':
            total_pixel = model.h * model.w
            curr_t = 0
            for i in xrange(time_length):
                curr_t += 1
                curr_overhead = 0
                if curr_t == chunk_size:
                    curr_t = 0
                    curr_overhead += header_size
                    print "total_pixel: " + str(total_pixel)
                    print "actual_pixel: " + str((motion[i].down_pt[0] - motion[i].start_pt[0]) * (motion[i].down_pt[1] - motion[i].start_pt[1]))
                curr_overhead += simulator.compute_ratio_overhead(total_pixel, (motion[i].down_pt[0] - motion[i].start_pt[0]) * (motion[i].down_pt[1] - motion[i].start_pt[1]))
                h_over_time.append(curr_overhead)
                d_over_time.append(0)
                curr_history = []
                for i in xrange(20):
                    curr_history.append([i, 1])
                history_lst.append(curr_history)

        elif model.get_name() == 'model3':
            # model3: 2 layers, only transmit the required tiles in any level, also transmit related tiles in the other level
            total_pixel = 1
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
                    # if current storage does not have this tile, transmit it
                    if tile.get_id() not in transmitted_windows_map.keys():
                         transmitted_windows_map[tile.get_id()] = chunk_size
                         transmitted_tiles.append(tile)
                         print transmitted_windows_map
                # reduce life time for all tiles
                for tile_id in transmitted_windows_map.keys():
                    if transmitted_windows_map[tile_id] == 1:
                        transmitted_windows_map.pop(tile_id, None)
                    else:
                        transmitted_windows_map[tile_id] = transmitted_windows_map[tile_id] - 1
                curr_history = []
                for t in set(transmitted_windows_map):
                    curr_history.append([t, transmitted_windows_map[t]])
                history_lst.append(curr_history)
                total_pixel = simulator.get_transmitted_pixels(transmitted_tiles, chunk_size, model.get_w(), model.get_h())
                actual_pixel = curr_view.get_pixels() # actual number of pixels get displayed
                print "total_pixel: " + str(total_pixel)
                print "actual_pixel: " + str(actual_pixel)
                curr_overhead += simulator.compute_ratio_overhead(total_pixel, actual_pixel)
                h_over_time.append(curr_overhead)
                d_over_time.append(0)

        # model 4 is for the aggressive transmission ( the most common one )
        # the difference between this and model3 strategy is that this one enforces transmission that catches
        # current and the next frame
        elif model.get_name() == 'model4':
            ahead_limit = 2
            total_pixel = 1
            transmitted_windows_map = {}
            for i in xrange(time_length):
                curr_overhead = 0
                curr_view = motion[i]
                tiles = simulator.get_tiles(curr_view, model) # get list of tiles to be displayed
                transmitted_tiles = [] # list of tiles to be transmitted
                print "tiles to be displayed: " + str(tiles)
                for tile in tiles:
                    # if current memory does not have this tile and 1 frame later
                    # (assume the tile length is 2), we need transmit it
                    if tile.get_id() not in transmitted_windows_map.keys():
                        transmitted_windows_map[tile.get_id()] = chunk_size
                        transmitted_tiles.append(tile)
                    #    print transmitted_windows_map
                    elif transmitted_windows_map[tile.get_id()] < ahead_limit:
                        transmitted_windows_map[tile.get_id()] += chunk_size
                        transmitted_tiles.append(tile)
                # descrease tile lifetime
                for tile_id in transmitted_windows_map.keys():
                    if transmitted_windows_map[tile_id] == 1:
                        transmitted_windows_map.pop(tile_id, None)
                    else:
                        transmitted_windows_map[tile_id] = transmitted_windows_map[tile_id] - 1
                    curr_history = []
                # record a history
                for t in set(transmitted_windows_map):
                    curr_history.append([t, transmitted_windows_map[t]])
                history_lst.append(curr_history)
                tile_history.append(transmitted_tiles)
                total_pixel = simulator.get_transmitted_pixels(transmitted_tiles, chunk_size, model.get_w(), model.get_h())
       #         curr_bdwh, total_pixel = comsume_remaining_bandwidth(curr_bdwh, total_pixel, transmitted_windows_map, transmitted_tiles)
                actual_pixel = curr_view.get_number_of_pixels() # actual number of pixels get displayed
                print "total_pixel: " + str(total_pixel)
                print "actual_pixel: " + str(actual_pixel)
                curr_overhead += simulator.compute_ratio_overhead(total_pixel, actual_pixel)
                h_over_time.append(curr_overhead)
                d_over_time.append(0)
        # write a 1D model to verify
        # model is 1D, we try different tile size, with a pariticular view series
        # TODO: make sure this is correct
        elif model.get_name() == '1D':
            transmitted_windows_map = {}
            for i in xrange(time_length):
                curr_overhead = 0
                curr_view = motion[i]
                # TODO: change here
                tiles = simulator.get_tiles1d(curr_view, model)
                transmitted_tiles = []
                print "tiles: " + str(tiles)
                for tile in tiles:
                    # if current memory does not keep this tile for now and 1 frame later, transmit it
            #        if tile.get_id() not in transmitted_windows_map.keys():
                        transmitted_windows_map[tile.get_id()] = chunk_size
                        transmitted_tiles.append(tile)
                        print transmitted_windows_map
            #        elif transmitted_windows_map[tile.get_id()] < ahead_limit:
            #            transmitted_windows_map[tile.get_id()] += chunk_size
            #            transmitted_tiles.append(tile)
                for tile_id in transmitted_windows_map.keys():
                    if transmitted_windows_map[tile_id] == 1:
                        transmitted_windows_map.pop(tile_id, None)
                    else:
                        transmitted_windows_map[tile_id] = transmitted_windows_map[tile_id] - 1
                    curr_history = []
                for t in set(transmitted_windows_map):
                    curr_history.append([t, transmitted_windows_map[t]])
                history_lst.append(curr_history)
                tile_history.append(transmitted_tiles)

                total_pixel = simulator.get_transmitted_pixels1d(transmitted_tiles, chunk_size, model.get_l())
       #         curr_bdwh, total_pixel = comsume_remaining_bandwidth(curr_bdwh, total_pixel, transmitted_windows_map, transmitted_tiles)
                actual_pixel = curr_view.get_number_of_pixels() # actual number of pixels get displayed
                print "total_pixel: " + str(total_pixel)
                print "actual_pixel: " + str(actual_pixel)
                curr_overhead += simulator.compute_ratio_overhead(total_pixel, actual_pixel)
                h_over_time.append(curr_overhead)
                d_over_time.append(0)


  # TODO: can we put the strategy into a JSON?
        return h_over_time, d_over_time, history_lst, tile_history

    @staticmethod
    def compute_minus_overhead(total_pixel, actual_pixel):
        return total_pixel - actual_pixel


    @staticmethod
    def compute_ratio_overhead(total_pixel, actual_pixel):
        return float(total_pixel - actual_pixel) / float(actual_pixel)


    @staticmethod
    def get_tiles1d(curr_view, model):
        model_l = model.get_l()
        tiles = []
        number_of_tiles = model.get_total_size() / model.get_l()
        l = model.get_l()
        for i in xrange(number_of_tiles):
            start = i * l
            end = (i+1) * l
            if curr_view.get_start() <= start:
                if curr_view.get_end() > start:
                    tiles.append(tile(start, end))
            elif curr_view.get_start() < end:
                tiles.append(tile1d(start, end))
        return tiles

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
    def get_transmitted_pixels1d(tiles, chunk_size, model_l):
        print tiles
        total_pixels = 0
        for tile in tiles:
            total_pixels += tile.get_l()
        return total_pixels


    @staticmethod
    def get_transmitted_pixels(tiles, chunk_size, model_w ,model_h):
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


    @staticmethod
    def get_history():
        # supporse to return the record history
        # history format:
        return None


def test():
    model0 = model("model0", 100, 100)
    m0 = motion(0, (20, 80), (16, 13))
    m1 = motion(1, (10, 70), (16, 20))
    m2 = motion(2, (40, 75), (50, 18))
    m3 = motion(3, (45, 55), (20, 10))
    motions = [m0, m1, m2, m3]
    args = {"header": 10, "chunk_size": 5}
    h_over_time, d_over_time = simulator.simulate(model0, motions, args)
    print "h_over_time: " + str(h_over_time)
    print "d_over_time: " + str(d_over_time)


if __name__ == '__main__':
    test()
