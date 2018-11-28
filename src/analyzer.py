import argparse
import os
import cv2
import json


from base_service import BaseService


class Analyzer(object):
    def __init__(self):
        pass

    def run(self, file_path):
        pass


class ImageDimentionsAnalyzer(Analyzer):
    def __init(self):
        super(ImageDimentionsAnalyzer, self).__init__()


    def run(self, file_path):
        img = cv2.imread(file_path)
        height, width, channels = img.shape

        return {'height':height, 'width':width}

class AvarageColorAnalyzer(Analyzer):
    def __init(self):
        super(AvarageColorAnalyzer, self).__init__()


    def run(self, file_path):
        img = cv2.imread(file_path)
        return {'mean:' ,cv2.mean(img)}


class BrightnessIndicator(Analyzer):
    def __init(self):
        super(BrightnessIndicator, self).__init__()


    def run(self, file_path):
        img = cv2.imread(file_path)
        mean_values = cv2.mean(img)
        brightness = sum([mean_values[0],mean_values[1],mean_values[2]])/3
        return {'brightness': brightness}

class AnalyzerFactory(object):
    @staticmethod
    def get_analyzer(name):
        if name == 'ImageDimentionsAnalyzer':
            return ImageDimentionsAnalyzer()
        elif name == 'AvarageColorAnalyzer':
            return AvarageColorAnalyzer()
        elif name == 'BrightnessIndicator':
            return BrightnessIndicator()
        else:
            print('Analyzer was not found')
            return None


class AnalyzeData(BaseService):
    def __init__(self, input_dir, output_dir):
        super(AnalyzeData, self).__init__(input_dir, output_dir)
        self._analyzers = []

    def run(self):
        self._add_analyzers()

        while True:
            files = os.listdir(self._input_dir)
            for input_file in files:
                file_path = os.path.join(self._input_dir, input_file)
                self._process_file(file_path=file_path)

            break

    def _process_file(self, file_path):
        print('Analyzing ' + file_path)
        data = {}
        data['name'] = file_path
        for analyzer in self._analyzers:
            result = analyzer.run(file_path)

            data[analyzer.__class__.__name__] = result

        self._save_data_to_json(data=data)

    def _save_data_to_json(self, data):
        print('saving data: ', data)

        with open('data.json', 'w') as fp:
            json.dump(data, fp)

    def _add_analyzers(self):
        self._analyzers.append(AnalyzerFactory.get_analyzer(name='ImageDimentionsAnalyzer'))
        self._analyzers.append(AnalyzerFactory.get_analyzer(name='AvarageColorAnalyzer'))
        self._analyzers.append(AnalyzerFactory.get_analyzer(name='BrightnessIndicator'))


def run(args):
    projector = AnalyzeData(input_dir=args.in_dir,
                          output_dir=args.out_dir)

    projector.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--in-dir', help='Path to input dir', nargs='?')
    parser.add_argument('--out-dir', help='Path to output dir', nargs='?')
    args = parser.parse_args()

    run(args)
