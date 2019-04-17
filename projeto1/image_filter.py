import cv2
import numpy as np


class ImageFilter:

    @staticmethod
    def __normalize_image(image):
        """
        Normaliza e escreve uma imagem
        :param image: imagem a ser desenhada no arquivo
        """
        new_image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
        return new_image

    @staticmethod
    def filter_h1(image):
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
        return ImageFilter.__normalize_image(new_image)

    @staticmethod
    def filter_h2(image):
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
        return ImageFilter.__normalize_image(new_image)

    @staticmethod
    def filter_h3(image):
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
        return ImageFilter.__normalize_image(new_image)

    @staticmethod
    def filter_h4(image):
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
        return ImageFilter.__normalize_image(new_image)

    @staticmethod
    def filter_h3_h4(image):
        """
        Filtra uma imagem
        :param image: imagem a ser filtrada
        :param normalize: indica se a imagem deve ser normalizada. Por padrão, ela é normalizada.
        :return: imagem filtrada, podendo estar normalizada no intervalo de 0 a 255
        """
        image_1 = ImageFilter.filter_h3(image)
        image_2 = ImageFilter.filter_h4(image)
        new_image = np.hypot(image_1, image_2)
        return ImageFilter.__normalize_image(new_image)

    @staticmethod
    def filter_gaussian(image, sigma=30):
        # Calcula a transformada e translada a faixa-zero para o centro
        fourier = np.fft.fft2(image)
        fourier_translated = np.fft.fftshift(fourier)

        # Aplica o filtro Gaussiano
        linear_gaussian = cv2.getGaussianKernel(image.shape[0], sigma)
        kernel = np.dot(linear_gaussian, linear_gaussian.T)
        fourier_translated = fourier_translated * kernel

        # Volta para a imagem
        fourier_untranslated = np.fft.ifftshift(fourier_translated)
        new_image = np.fft.ifft2(fourier_untranslated)
        new_image = np.abs(new_image)
        return ImageFilter.__normalize_image(new_image)
