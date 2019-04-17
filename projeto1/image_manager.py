import cv2
import os
import numpy as np
from image_filter import ImageFilter


class ImageManager:

    @staticmethod
    def create_filtered_image(filter_type, input_file, option, output_file='./results'):
        """
        Cria uma imagem nova, aplicando-se um filtro
        :param filter_type: tipo de filtro. Pode ser h1, h2, h3, h4, h3_h4, g ou  all
        :param input_file: arquivo de imagem de entrada
        :param option: opção de cada filtro. Para os filtros h, pode ser - ou binary, indicando que
                       devem ser transfomrados em imagens binárias. Para o g, indica o desvio padrão da Gaussiana
        :param output_file: arquivo de saída, onde a imagem deve ser escrita.
        """
        image = np.float32(cv2.imread(input_file, 0))

        if filter_type == 'all':
            ImageManager.__create_all_filtered_images(input_file, output_file, image)
        else:
            ImageManager.__create_specific_filter(filter_type, image, output_file, option)

    @staticmethod
    def __create_specific_filter(filter_type, image, output_file, option):
        """
        Trata o caso de ter que criar com um filtro específico e cria o arquivo
        :param filter_type: Pode ser h1, h2, h3, h4, h3_h4, g ou  all
        :param image: imagem a ser filtrada
        :param output_file: arquivo de saída
        :param option: opção dos filtros
        """
        if filter_type == 'g':
            image = ImageFilter.filter_gaussian(image, int(option))
        else:
            binary = option == 'binary'
            if filter_type == 'h1':
                image = ImageFilter.filter_h1(image, binary)
            elif filter_type == 'h2':
                image = ImageFilter.filter_h2(image, binary)
            elif filter_type == 'h3':
                image = ImageFilter.filter_h3(image, binary)
            elif filter_type == 'h4':
                image = ImageFilter.filter_h4(image, binary)
            elif filter_type == 'h3_h4':
                image = ImageFilter.filter_h3_h4(image, binary)

        cv2.imwrite(output_file, image)

    @staticmethod
    def __create_all_filtered_images(input_file, out_dir, image):
        """
        Trata o caso de ter que passar a imagem por todos os filtros
        :param input_file: caminho do arquivo de entrada
        :param out_dir: diretório de saída dos resultados
        :param image: arquivo de imagem
        """
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

        # Gera imagens com filtro gaussiano com diferentes desvios padrão
        for sigma in range(5, 51, 5):
            cv2.imwrite(f"{out_dir}/{base}_g_{sigma}{extension}", ImageFilter.filter_gaussian(image, sigma))
