# this script generates a spread sheet
# format: # of cameras | cam_size | F.R. | B.R. | tiling | scaling | freq. of I frames | (storage size) |

# systems : (tegra | highsilicon) -> Ingest | Storage | transmit | (play at which scale) -> Render |

# generate a csv file

import csv


class generate_spreadsheet:

    @staticmethod
    def write_to_csv():
        print "hi"
        with open('eggs.csv', 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|',
                                    quoting=csv.QUOTE_MINIMAL)
            column_titles = generate_column_titles()
            spamwriter.writerow(column_titles)
            spamwriter.writerow(['Spam', 'Lovely Spam', "Wonderful Spam"])

   @staticmethod
   def generate_column_titles():
       return ['N_of_cams', 'cam_size', 'frame_rate', 'bit_rate', 'tiling', 'scaling', 'I_frame_freq', 'storage_size']


def main():
    generate_spreadsheet.write_to_csv()


if __name__ == "__main__":
    main()
