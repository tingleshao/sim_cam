# class that represent a tile or a 1d tile (segment)

class tile:
    def __init__(self, id):
        print "you just initialized tile: " + str(id)
        self.id = id

    def get_id(self):
        return self.id


class tile1d(tile):
    def __init__(self, start, end):
        self.start = start
        self.l = end-start
        self.id = 0

    def get_start(self):
        return self.start

    def get_end(self):
        return self.start + l

    def get_l(self):
        return self.l
