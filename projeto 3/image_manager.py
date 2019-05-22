import cv2
from morphological import Morphological


class ImageManager:

    @staticmethod
    def analyze_image(input_file_path, output_file_path, use_morphological=True):
        image = cv2.imread(input_file_path, 0)
        image, lines_count, words_count = Morphological.analyze_text_image(image, use_morphological)
        cv2.imwrite(output_file_path, image)
        print("{}: {} linhas e {} palavras encontradas".format(output_file_path, lines_count, words_count))
