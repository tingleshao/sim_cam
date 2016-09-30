# class that rerpesents a system model


# two parts:
# layer architecture
# transmit / cache strategy


class model:

    def __init__(self, name, w, h):
        print "you just created a model!"
        self.name = name
        self.w = w
        self.h = h

    def __str_(self):
        return "a model!"

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_w(self):
        return self.w

    def set_w(self, w):
        self.w = w

    def get_h(self):
        return self.h

    def set_h(self, h):
        self.h = h

    def get_xxx(self):
        return "xxx!"

    def set_xxx(self, xxx):
        self.xxx = xxx
