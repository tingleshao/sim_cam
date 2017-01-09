# class that represent a  tile

class tile:
    def __init__(self, id):
        print "you just initialized tile: " + str(id)
        self.id = id

    def get_id(self):
        return self.id


class tile1d(tile):
    def __init__(self, id, start, l):
        print "you just initialized a 1d tile"  + str(id)
        self.id = id
        self.start = start
        self.l = l

    def __init__(self, start, end):
        self.__init__(0, start, end-start)

    def get_start(self):
        return self.start

    def get_end(self):
        return self.start + l

    def get_l(self):
        return self.l
