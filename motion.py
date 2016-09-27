# this is a class that represents the "motion" object
# motion is basically a three-element tuple:
#   motion
#    - window origin
#    - window down right corner
#    - timestamp


class motion:
    def __init__(self, timestamp, start_pt, down_pt):
        self.timestamp = timestamp
        self.start_pt = start_pt
        self.down_pt = down_pt

    def __str__(self):
        return """This is someone's view rectangle at timestamp %d, with start
print (%d, %d), and lower right corner (%d, %d)""" % (self.timestamp,
self.start_pt[0], self.start_pt[1], self.down_pt[0], self.down_pt[1])
