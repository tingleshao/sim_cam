# class that rerpesents a system model

# two parts:
# layer architecture
# transmit / cache strategy

from model import model


class model1d(model):
    def __init__(self, name, l, total_size):
        print "you just created a 1D model!"
        self.name = name
        self.l = l
        self.total_size = total_size

#    def __init__(self, name, l):
#        print "you just created a 1D model!"
#        self.name = name
#        self.l = l

    def __str_(self):
        return "a 1D model!"

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_l(self):
        return self.l

    def set_l(self, l):
        self.l = l

    def get_total_size(self):
        return self.total_size



class model1d_new(model):
    def __init__(self, name, l, n_of_cams, frame_rate, bit_rate, tiling,
                 scaling, I_freq, storage_size):
        print "you just created a 1D model!"
        self.name = name
        self.l = l
        self.n_of_cams = n_of_cams
        self.fr = frame_rate
        self.br = bit_rate
        self.tiling = tiling
        self.scaling = scaling
        self.I_freq = I_freq
        self.storage_size = storage_size

    def __str_(self):
        return "a 1D model!"

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_l(self):
        return self.l

    def set_l(self, l):
        self.l = l

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
