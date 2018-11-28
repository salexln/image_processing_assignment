import argparse
import os
import numpy as np
# import imageio as im
import cv2


from nfov import NFOV

class Projector(object):
    def __init__(self, input_dir, output_dir):
        self._input_dir = input_dir
        self._output_dir = output_dir
        self._nfov = NFOV()
        self._center_point = np.array([0.5, .5])


    def run(self):
        while True:
            files = os.listdir(self._input_dir)
            for input_file in files:
                file_path = os.path.join(self._input_dir, input_file)
                self._process_file(file_path=file_path)

            break

    def _process_file(self, file_path):
        try:
            print('Processing ' + file_path)
            projected_data = self._project_file(file_path)
            file_name = 'projected_' + file_path.split('/')[-1]

            self._save_data_to_file(image_data=projected_data,
                                    file_name=file_name)
            self._remove_file(file_to_remove=file_path)
        except Exception as e:
            print('Failed to process file')

    def _project_file(self, file_path):
        print(file_path)
        # img = im.imread(file_path)
        img = cv2.imread(file_path)
        return self._nfov.toNFOV(img, self._center_point)

    def _save_data_to_file(self, image_data, file_name):
        cv2.imwrite(self._output_dir + '/' + file_name, image_data)

    def _remove_file(self, file_to_remove):
        try:
            os.remove(file_to_remove)
        except:
            print('Failed to remove file')


def run(args):
    projector = Projector(input_dir=args.in_dir,
                          output_dir=args.out_dir)

    projector.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--in-dir', help='Path to input dir', nargs='?')
    parser.add_argument('--out-dir', help='Path to output dir', nargs='?')
    args = parser.parse_args()

    run(args)
