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


class model_new:

    def __init__(self, name, w, h, n_of_cams, frame_rate, bit_rate, tiling,
                 scaling, I_freq, storage_size):
        print "you just created a model!"
        self.name = name
        self.w = w
        self.h = h
        self.n_of_cams = n_of_cams
        self.fr = frame_rate
        self.br = bit_rate
        self.tiling = tiling
        self.scaling = scaling
        self.I_freq = I_freq
        self.storage_size = storage_size

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

    def get_n_of_cams(self):
        return self.n_of_cams

    def set_n_of_cams(self, n):
        self.n_of_cams = n

    def get_frame_rate(self):
        return self.fr

    def set_frame_rate(self, fr):
        self.fr = fr

    def get_bit_rate(self):
        return self.br

    def set_bit_rate(self, br):
        self.br = br

    def get_tiling(self):
        return self.tiling

    def set_tiling(self, tiling):
        self.tiling = tiling

    def get_scaling(self):
        return self.scaling

    def set_scaling(self, scaling):
        self.scaling = scaling

    def get_I_freq(self):
        return self.I_freq

    def set_I_freq(self, I_freq):
        self.I_freq = I_freq

    def get_storage_size(self):
        return self.storage_size

    def set_storage_size(self, storage_size):
        self.storage_size = storage_size
