# model reader is used for reading a model from a JSON file and
# generate a model object

from model import model, model_new
#from model import model_new
from logger import logger
import json
from pprint import pprint
from motion import motion

class model_reader:

    def __init__(self):
        logger.debug_print("debug", "you just created a model reader!")

    @staticmethod
    def read_model(file_name):
        with open(file_name) as model_file:
            model_data = json.load(model_file)
        pprint(model_data)
        model_obj = model(model_data["name"], model_data["width"], model_data["height"])
        return model_obj

    @staticmethod
    def read_model_new(file_name):
        with open(file_name) as model_file:
            model_data = json.load(model_file)
        pprint(model_data)
        model_obj = model_new(model_data["name"], model_data["width"],
                              model_data["height"], model_data["n_of_cams"],
                              model_data["frame_rate"], model_data["bit_rate"],
                              model_data["tiling"], model_data["scaling"],
                              model_data["I_frame_freq"],
                              model_data["storage_size"])
        return model_obj

    @staticmethod
    def read_motions(file_name):
        with open(file_name) as model_file:
            model_data = json.load(model_file)
        pprint(model_data)
        motions = []
        for m in model_data["motions"]:
            motions.append(motion(m["timestamp"], (m["start_pt"]['x'], m["start_pt"]['y']),
             (m['down_pt']['x'], m['down_pt']['y'])))
        return motions

    @staticmethod
    def test():
        model_reader.read_model('models/model0.json')


if __name__ == '__main__':
    model_reader.test()
