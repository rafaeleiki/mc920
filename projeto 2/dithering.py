import numpy as np


class Dithering:

    @staticmethod
    def floyd_steinberg(image, alternate=True, threshold=128):
        """
        Aplica a técnica de pontilhado por difusão de erro de Floyd-Steinberg
        :param image: Matriz da imagem original
        :param alternate: Define se a ordem de passagem na matriz vai ser padrão ou alternada (por padrão, alternada)
        :param threshold: Limiar a ser considerado para o pixel ser branco ou preto
        :return: nova imagem gerada com a técnica de pontilhado
        """

        # Gera a nova imagem
        (height, width) = image.shape
        new_image = np.zeros((height + 1, width + 2), np.float32)
        new_image[0:-1, 1:-1] = image

        # Percorre as linhas
        for row in range(0, height):

            # Define se a linha vai ser percorrida diretamente ou de forma alternada
            if not alternate or row % 2 == 0:
                order = 1
                col_range = range(1, width, 1)
            else:
                order = -1
                col_range = range(width, 0, -1)

            # Percorre cada coluna da linha
            for col in col_range:

                # Calcula o novo valor do pixel
                old_value = new_image[row, col]
                new_value = 255 if old_value > threshold else 0
                new_image[row, col] = new_value

                # Distribui o erro
                error = old_value - new_value
                new_image[row, col + order] = new_image[row, col + order] + (error * 7) / 16
                new_image[row + 1, col - order] = new_image[row + 1, col - order] + (error * 3) / 16
                new_image[row + 1, col] = new_image[row + 1, col] + (error * 5) / 16
                new_image[row + 1, col + order] = new_image[row + 1, col + order] + (error * 1) / 16

        return new_image[0:-1, 1:-1]

    @staticmethod
    def ordered_dithering(image):
        """
        Aplica a técnica de pontilhamento ordenado com matriz 3x3 numa imagem
        :param image: matriz da imagem a ser aplicada a técnica
        :return: nova imagem processada, com dimensões 3 vezes maiores que a original
        """
        # Define o padrão para cada nível de cinza
        level0 = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        level1 = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
        level2 = np.array([[0, 0, 0], [1, 1, 0], [0, 0, 0]])
        level3 = np.array([[0, 0, 0], [1, 1, 0], [0, 1, 0]])
        level4 = np.array([[0, 0, 0], [1, 1, 1], [0, 1, 0]])
        level5 = np.array([[0, 0, 1], [1, 1, 1], [0, 1, 0]])
        level6 = np.array([[0, 0, 1], [1, 1, 1], [1, 1, 0]])
        level7 = np.array([[1, 0, 1], [1, 1, 1], [1, 1, 0]])
        level8 = np.array([[1, 0, 1], [1, 1, 1], [1, 1, 1]])
        level9 = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])

        levels = [level0, level1, level2, level3, level4, level5, level6, level7, level8, level9]

        return Dithering.__generic_ordered_dithering(image, levels, 3)

    @staticmethod
    def ordered_dithering_bayer(image):
        """
        Aplica a técnica de pontilhamento ordenado com a matriz de Bayer (4x4)
        :param image:  matriz da imagem a ser aplicada a técnica
        :return: nova imagem processada, com dimensões 4 vezes maiores que a original
        """
        # Define o padrão para cada nível de cinza da escala
        level0 = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        level1 = np.array([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        level2 = np.array([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0]])
        level3 = np.array([[1, 0, 0, 0], [0, 0, 0, 0], [1, 0, 1, 0], [0, 0, 0, 0]])
        level4 = np.array([[1, 0, 1, 0], [0, 0, 0, 0], [1, 0, 1, 0], [0, 0, 0, 0]])
        level5 = np.array([[1, 0, 1, 0], [0, 1, 0, 0], [1, 0, 1, 0], [0, 0, 0, 0]])
        level6 = np.array([[1, 0, 1, 0], [0, 1, 0, 0], [1, 0, 1, 0], [0, 0, 0, 1]])
        level7 = np.array([[1, 0, 1, 0], [0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1]])
        level8 = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1]])
        level9 = np.array([[1, 0, 1, 0], [1, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1]])
        level10 = np.array([[1, 0, 1, 0], [1, 1, 0, 1], [1, 0, 1, 0], [0, 1, 1, 1]])
        level11 = np.array([[1, 0, 1, 0], [1, 1, 0, 1], [1, 0, 1, 0], [1, 1, 1, 1]])
        level12 = np.array([[1, 0, 1, 0], [1, 1, 1, 1], [1, 0, 1, 0], [1, 1, 1, 1]])
        level13 = np.array([[1, 1, 1, 0], [1, 1, 1, 1], [1, 0, 1, 0], [1, 1, 1, 1]])
        level14 = np.array([[1, 1, 1, 0], [1, 1, 1, 1], [1, 0, 1, 1], [1, 1, 1, 1]])
        level15 = np.array([[1, 1, 1, 0], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])
        level16 = np.array([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])

        levels = [level0, level1, level2, level3, level4, level5, level6, level7, level8,
                  level9, level10, level11, level12, level13, level14, level15, level16]

        return Dithering.__generic_ordered_dithering(image, levels, 4)

    @staticmethod
    def __generic_ordered_dithering(image, levels, matrix_size):
        """
        Realiza o processo de pontilhamento ordenado
        :param image: imagem a ser aplicada a técnica
        :param levels: padrões associados aos níveis de cinza originais
        :param matrix_size: tamanho da matriz do pontilhamento ordenado
        :return: nova imagem, processada
        """
        max_level = matrix_size * matrix_size

        # Cria a nova imagem
        (old_height, old_width) = image.shape
        new_image = np.zeros((old_height * matrix_size, old_width * matrix_size), np.uint8)

        # Percorre a matriz original, substituindo os pixels pela matriz com o padrão correspondente
        for row in range(old_height):
            for col in range(old_width):
                normalized_pixel = int(round(image[row, col] * max_level / 255))
                new_row = matrix_size * row
                new_col = matrix_size * col
                new_image[new_row: new_row + matrix_size, new_col: new_col + matrix_size] = levels[normalized_pixel]

        return new_image
