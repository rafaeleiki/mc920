import cv2
import os
import numpy as np
from image_filter import ImageFilter


class ImageManager:

    @staticmethod
    def create_filtered_image(filter_type, input_file, output_file='./results', sigma='30'):
        image = np.float32(cv2.imread(input_file, 0))

        sigma = int(sigma)

        if filter_type == 'all':
            ImageManager.__create_all_filtered_images(input_file, output_file, image)
        else:
            ImageManager.__create_specific_filter(filter_type, image, output_file, sigma)

    @staticmethod
    def __create_specific_filter(filter_type, image, output_file, sigma):
        if filter_type == 'h1':
            image = ImageFilter.filter_h1(image)
        elif filter_type == 'h2':
            image = ImageFilter.filter_h2(image)
        elif filter_type == 'h3':
            image = ImageFilter.filter_h3(image)
        elif filter_type == 'h4':
            image = ImageFilter.filter_h4(image)
        elif filter_type == 'h3_h4':
            image = ImageFilter.filter_h3_h4(image)
        elif filter_type == 'g':
            image = ImageFilter.filter_gaussian(image, sigma)

        cv2.imwrite(output_file, image)

    @staticmethod
    def __create_all_filtered_images(input_file, out_dir, image):

        # Descobre o nome do arquivo e a extensão
        filename = os.path.basename(input_file)
        filename_parts = os.path.splitext(filename)
        base = "".join(filename_parts[0:-1])
        extension = filename_parts[-1]

        # Gera as imagens com cada um dos filtros
        cv2.imwrite(f"{out_dir}/{base}_h1{extension}", ImageFilter.filter_h1(image))
        cv2.imwrite(f"{out_dir}/{base}_h2{extension}", ImageFilter.filter_h2(image))
        cv2.imwrite(f"{out_dir}/{base}_h3{extension}", ImageFilter.filter_h3(image))
        cv2.imwrite(f"{out_dir}/{base}_h4{extension}", ImageFilter.filter_h4(image))
        cv2.imwrite(f"{out_dir}/{base}_h3_h4{extension}", ImageFilter.filter_h3_h4(image))

        # Gera imagens com filtro gaussiano com diferentes sigmas,
        # de 5 em 5 até 10x menor que o tamanho da imagem
        for sigma in range(5, 51, 5):
            cv2.imwrite(f"{out_dir}/{base}_g_{sigma}{extension}", ImageFilter.filter_gaussian(image, sigma))
