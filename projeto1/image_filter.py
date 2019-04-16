import cv2
import numpy as np


class ImageFilter:

    @staticmethod
    def __normalize_image_if_required(image, normalize):
        """
        Normaliza e escreve uma imagem
        :param image: imagem a ser desenhada no arquivo
        """
        if normalize:
            scale = 255.0 / image.max()
            image = scale * image
        return image

    @staticmethod
    def filter_a(image, normalize=True):
        """
        Filtra uma imagem
        :param image: imagem a ser filtrada
        :param normalize: indica se a imagem deve ser normalizada. Por padrão, ela é normalizada.
        :return: imagem filtrada, podendo estar normalizada no intervalo de 0 a 255
        """
        matrix = [[0,  0, -1,  0, 0],
                  [0, -1, -2, -1, 0],
                  [-1, -2, 16, -2, -1],
                  [0, -1, -2, -1, 0],
                  [0,  0, -1,  0, 0]]
        matrix = np.array(matrix)
        new_image = cv2.filter2D(image, -1, matrix)
        return ImageFilter.__normalize_image_if_required(new_image, normalize)

    @staticmethod
    def filter_b(image, normalize=True):
        """
        Filtra uma imagem
        :param image: imagem a ser filtrada
        :param normalize: indica se a imagem deve ser normalizada. Por padrão, ela é normalizada.
        :return: imagem filtrada, podendo estar normalizada no intervalo de 0 a 255
        """
        matrix = [[1,  4, 6,  4, 1],
                  [4, 16, 24, 16, 4],
                  [6, 24, 36, 24, 6],
                  [4, 16, 24, 16, 4],
                  [1,  4, 6,  4, 1]]
        matrix = np.array(matrix) / 256
        new_image = cv2.filter2D(image, -1, matrix)
        return ImageFilter.__normalize_image_if_required(new_image, normalize)

    @staticmethod
    def filter_c(image, normalize=True):
        """
        Filtra uma imagem
        :param image: imagem a ser filtrada
        :param normalize: indica se a imagem deve ser normalizada. Por padrão, ela é normalizada.
        :return: imagem filtrada, podendo estar normalizada no intervalo de 0 a 255
        """
        matrix = [[-1, 0, 1],
                  [-2, 0, 2],
                  [-1, 0, 1]]
        matrix = np.array(matrix)
        new_image = cv2.filter2D(image, -1, matrix)
        return ImageFilter.__normalize_image_if_required(new_image, normalize)

    @staticmethod
    def filter_d(image, normalize=True):
        """
        Filtra uma imagem
        :param image: imagem a ser filtrada
        :param normalize: indica se a imagem deve ser normalizada. Por padrão, ela é normalizada.
        :return: imagem filtrada, podendo estar normalizada no intervalo de 0 a 255
        """
        matrix = [[-1, -2, -1],
                  [0, 0, 0],
                  [1, 2, 1]]
        matrix = np.array(matrix)
        new_image = cv2.filter2D(image, -1, matrix)
        return ImageFilter.__normalize_image_if_required(new_image, normalize)

    @staticmethod
    def filter_c_d(image, normalize=True):
        """
        Filtra uma imagem
        :param image: imagem a ser filtrada
        :param normalize: indica se a imagem deve ser normalizada. Por padrão, ela é normalizada.
        :return: imagem filtrada, podendo estar normalizada no intervalo de 0 a 255
        """
        image_c = ImageFilter.filter_c(image, False)
        image_d = ImageFilter.filter_d(image, False)
        new_image = np.sqrt(np.square(image_c) + np.square(image_d))
        return ImageFilter.__normalize_image_if_required(new_image, normalize)
