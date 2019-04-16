import cv2
import os
import numpy as np
from projeto1.image_filter import ImageFilter


class ImageManager:

    @staticmethod
    def create_filtered_image(filter_type, input_file, output_file='./results'):
        image = np.float32(cv2.imread(input_file))

        if filter_type == 'all':
            ImageManager.__create_all_filtered_images(input_file, output_file, image)
        else:
            ImageManager.__create_specific_filter(filter_type, image, output_file)

    @staticmethod
    def __create_specific_filter(filter_type, image, output_file):
        if filter_type == 'a':
            image = ImageFilter.filter_a(image)
        elif filter_type == 'b':
            image = ImageFilter.filter_b(image)
        elif filter_type == 'c':
            image = ImageFilter.filter_b(image)
        elif filter_type == 'd':
            image = ImageFilter.filter_b(image)
        elif filter_type == 'c+d':
            image = ImageFilter.filter_c_d(image)

        cv2.imwrite(output_file, image)

    @staticmethod
    def __create_all_filtered_images(input_file, out_dir, image):

        # Descobre o nome do arquivo e a extensão
        filename = os.path.basename(input_file)
        filename_parts = os.path.splitext(filename)
        base = "".join(filename_parts[0:-1])
        extension = filename_parts[-1]

        # Gera as imagens com cada um dos filtros
        cv2.imwrite(f"{out_dir}/{base}_a{extension}", ImageFilter.filter_a(image))
        cv2.imwrite(f"{out_dir}/{base}_b{extension}", ImageFilter.filter_b(image))
        cv2.imwrite(f"{out_dir}/{base}_c{extension}", ImageFilter.filter_c(image))
        cv2.imwrite(f"{out_dir}/{base}_d{extension}", ImageFilter.filter_d(image))
        cv2.imwrite(f"{out_dir}/{base}_c_d{extension}", ImageFilter.filter_c_d(image))
