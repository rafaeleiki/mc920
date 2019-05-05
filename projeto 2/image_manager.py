import cv2
from dithering import Dithering


class ImageManager:

    @staticmethod
    def create_dithering(input_file_path, output_file_path, type, filename='result'):
        image = cv2.imread(input_file_path, 0)

        if type == 'all':
            ImageManager.create_all(image, output_file_path, filename)
        else:
            if type == 'bayer':
                new_image = Dithering.ordered_dithering_bayer(image)
            elif type == 'ordered_dithering':
                new_image = Dithering.ordered_dithering(image)
            elif type == 'floyd_steinberg':
                new_image = Dithering.floyd_steinberg(image, False)
            elif type == 'floyd_steinberg_alternate':
                new_image = Dithering.floyd_steinberg(image, True)

            ImageManager.write_pbm_file(new_image, output_file_path)

    @staticmethod
    def create_all(image, output_dir, filename):
        new_image = Dithering.ordered_dithering_bayer(image)
        ImageManager.write_pbm_file(new_image, output_dir + filename + '_bayer.pbm')

        new_image = Dithering.ordered_dithering(image)
        ImageManager.write_pbm_file(new_image, output_dir + filename + '_ordered_dithering.pbm')

        new_image = Dithering.floyd_steinberg(image, False)
        ImageManager.write_pbm_file(new_image, output_dir + filename + '_floyd_steinberg.pbm')

        new_image = Dithering.floyd_steinberg(image, True)
        ImageManager.write_pbm_file(new_image, output_dir + filename + '_floyd_steinberg_alternate.pbm')

    @staticmethod
    def write_pbm_file(image, output_path):
        cv2.imwrite(output_path, image)
