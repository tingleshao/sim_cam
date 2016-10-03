# class that represent a  tile

class tile:
    def __init__(self, id):
        print "you just initialized tile: " + str(id)
        self.id = id

    def get_id(self):
        return self.id
