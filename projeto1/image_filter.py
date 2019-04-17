import cv2
import numpy as np


class ImageFilter:

    @staticmethod
    def __normalize_image(image):
        """
        Normaliza uma imagem no intervalo de 0 a 255
        :param image: imagem a ser desenhada no arquivo
        """
        new_image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
        return new_image

    @staticmethod
    def __binary_normalization_image(image):
        """
        Transforma a imagem em binária. Qualquer valor abaixo de 128 é transformado em 0; caso contrário, em 255.
        :param image: imagem a ser transformada
        :return: imagem com intensidades exclusivas de 0 e 255
        """
        ret, new_img = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
        return new_img

    @staticmethod
    def __normalize_image_binary_option(image, binary):
        """
        Normaliza uma imagem levando em consideração se vai ser binária
        :param image: imagem a ser transformada
        :param binary: indica se a imagem tem que ser em preto e branco
        :return: imagem transformada
        """
        if binary:
            new_image = ImageFilter.__binary_normalization_image(image)
        else:
            new_image = ImageFilter.__normalize_image(image)
        return new_image

    @staticmethod
    def filter_h1(image, binary=True):
        """
        Filtra uma imagem com um filtro passa-alta
        :param image: imagem a ser filtrada
        :param binary: indica se a imagem deve ser em preto e branco
        :return: imagem filtrada, normalizada no intervalo de 0 a 255
        """
        matrix = [[0,  0, -1,  0, 0],
                  [0, -1, -2, -1, 0],
                  [-1, -2, 16, -2, -1],
                  [0, -1, -2, -1, 0],
                  [0,  0, -1,  0, 0]]
        matrix = np.array(matrix)
        new_image = cv2.filter2D(image, -1, matrix)
        return ImageFilter.__normalize_image_binary_option(new_image, binary)

    @staticmethod
    def filter_h2(image, binary=False):
        """
        Filtra uma imagem com um filtro passa-baixa
        :param image: imagem a ser filtrada
        :param binary: indica se a imagem deve ser em preto e branco
        :return: imagem filtrada, normalizada no intervalo de 0 a 255
        """
        matrix = [[1,  4, 6,  4, 1],
                  [4, 16, 24, 16, 4],
                  [6, 24, 36, 24, 6],
                  [4, 16, 24, 16, 4],
                  [1,  4, 6,  4, 1]]
        matrix = np.array(matrix) / 256
        new_image = cv2.filter2D(image, -1, matrix)
        return ImageFilter.__normalize_image_binary_option(new_image, binary)

    @staticmethod
    def filter_h3(image, binary=True):
        """
        Filtra uma imagem com um filtro passa-alta que mantém os traços verticais
        :param image: imagem a ser filtrada
        :param binary: indica se a imagem deve ser em preto e branco
        :return: imagem filtrada, normalizada no intervalo de 0 a 255
        """
        matrix = [[-1, 0, 1],
                  [-2, 0, 2],
                  [-1, 0, 1]]
        matrix = np.array(matrix)
        new_image = cv2.filter2D(image, -1, matrix)
        return ImageFilter.__normalize_image_binary_option(new_image, binary)

    @staticmethod
    def filter_h4(image, binary=True):
        """
        Filtra uma imagem com um filtro passa-alta que mantém os traços horizontais
        :param image: imagem a ser filtrada
        :param binary: indica se a imagem deve ser em preto e branco
        :return: imagem filtrada, normalizada no intervalo de 0 a 255
        """
        matrix = [[-1, -2, -1],
                  [0, 0, 0],
                  [1, 2, 1]]
        matrix = np.array(matrix)
        new_image = cv2.filter2D(image, -1, matrix)
        return ImageFilter.__normalize_image_binary_option(new_image, binary)

    @staticmethod
    def filter_h3_h4(image, binary=True):
        """
        Filtra uma imagem com um filtro passa-alta, combinando traços horizontais e verticais
        :param image: imagem a ser filtrada
        :param binary: indica se a imagem deve ser em preto e branco
        :return: imagem filtrada, normalizada no intervalo de 0 a 255
        """
        image_1 = ImageFilter.filter_h3(image)
        image_2 = ImageFilter.filter_h4(image)
        new_image = np.hypot(image_1, image_2)
        return ImageFilter.__normalize_image_binary_option(new_image, binary)

    @staticmethod
    def filter_gaussian(image, sigma):
        """
        Filtra uma imagem com um filtro Gaussiano no domínio da frequência
        :param image: imagem a ser filtrada
        :param sigma: desvio padrão do filtro Gaussiano
        :return: imagem filtrada
        """
        # Calcula a transformada e translada a faixa-zero para o centro
        fourier = np.fft.fft2(image)
        fourier_translated = np.fft.fftshift(fourier)

        # Aplica o filtro Gaussiano
        linear_gaussian = cv2.getGaussianKernel(image.shape[0], sigma)
        kernel = np.dot(linear_gaussian, linear_gaussian.T)
        fourier_translated = fourier_translated * kernel

        # Volta do espectro para a imagem
        fourier_untranslated = np.fft.ifftshift(fourier_translated)
        new_image = np.fft.ifft2(fourier_untranslated)
        new_image = np.abs(new_image)
        return ImageFilter.__normalize_image(new_image)
