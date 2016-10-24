# this script generates a spread sheet
# format: # of cameras | cam_size | F.R. | B.R. | tiling | scaling | freq. of I frames | (storage size) |
# systems : (tegra | highsilicon) -> Ingest | Storage | transmit | (play at which scale) -> Render |
# generate a csv file

import csv
from model_reader import model_reader as mr

class generate_spreadsheet:

    @staticmethod
    def write_to_csv():
        with open('eggs.csv', 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|',
                                    quoting=csv.QUOTE_MINIMAL)
            column_titles = generate_spreadsheet.generate_column_titles()
            spamwriter.writerow(column_titles)
            spamwriter.writerow(['Spam', 'Lovely Spam', "Wonderful Spam"])
            spamwriter.writerow(generate_spreadsheet
                                .read_from_model("models/model0_new.json"))

    @staticmethod
    def generate_column_titles():
        # storage_size is in unit of MB
        return ['N_of_cams', 'cam_size', 'frame_rate', 'bit_rate', 'tiling',
                'scaling', 'I_frame_freq', 'storage_size']

    @staticmethod
    def read_from_model(model_filename):
        model_obj = mr.read_model_new(model_filename)
        return [model_obj.get_n_of_cams(),
                model_obj.get_w() * model_obj.get_h(),
                model_obj.get_frame_rate(), model_obj.get_bit_rate(),
                model_obj.get_tiling(), model_obj.get_scaling(),
                model_obj.get_I_freq(), model_obj.get_storage_size()]


def main():
    generate_spreadsheet.write_to_csv()


if __name__ == "__main__":
    main()
