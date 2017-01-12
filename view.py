# this is a class that represents the "motion" object
# motion is basically a three-element tuple:
#   motion
#    - window origin
#    - window down right corner
#    - timestamp


class view:
    def __init__(self, timestamp, start_pt, down_pt):
        self.timestamp = timestamp
        self.start_pt = start_pt
        self.down_pt = down_pt

    def __str__(self):
        return """This is someone's view rectangle at timestamp %d, with start
print (%d, %d), and lower right corner (%d, %d)""" % (self.timestamp,
self.start_pt[0], self.start_pt[1], self.down_pt[0], self.down_pt[1])

    def get_start_pt(self):
        return self.start_pt

    def get_down_pt(self):
        return self.down_pt

    def get_w(self):
        return self.down_pt[0] - self.start_pt[0]

    def get_h(self):
        return self.down_pt[1] - self.start_pt[1]

    def get_number_of_pixels(self):
        return self.get_w() * self.get_h()

    def get_timestamp(self):
        return self.timestamp



class view1d:
    def __init__(self, timestamp, start, end):
        self.timestamp = timestamp
        self.start = start
        self.end = end

    def __str__(self):
        return """view 1d, timestamp: (%d), start: (%d), end: (%d)""" % (self.timestamp, self.start, self.end)

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_timestamp(self):
        return self.timestamp

    def get_number_of_pixels(self):
        return self.end - self.start


def test():
    m0 = view(0, (0, 0), (100, 100))
    print str(m0)


if __name__ == '__main__':
    test()
