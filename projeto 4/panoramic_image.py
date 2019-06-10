import cv2
import numpy as np


class PanoramicImage:

    def __init__(self, image_path=None):
        self.image_path = image_path

        if image_path is not None:
            self.image = self.original_image = cv2.imread(image_path)
            self.key_points = None
            self.descriptor = None

    def reset_to_original_image(self) -> None:
        """
        Reseta a imagem atualmente sendo trabalhada para a original
        """
        self.image = self.original_image

    def to_gray_scale(self):
        """
        Cria uma versão em preto e branco da imagem
        :return: imagem em preto e branco
        """
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def ransac_matrix(self, other_image: 'PanoramicImage', matches):
        """
        Estima a matriz de homografia
        :param other_image: imagem a ser comparada
        :param matches: semelhanças encontradas
        :return: matriz de homografia
        """
        points1 = np.float32([self.key_points[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        points2 = np.float32([other_image.key_points[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        homography_matrix, _ = cv2.findHomography(points1, points2, cv2.RANSAC, 5.0)
        return homography_matrix

    def merge_panoramic(self, other_image: 'PanoramicImage', homography_matrix) -> 'PanoramicImage':
        """
        Casa duas imagens para formar uma foto panorâmica
        :param other_image: imagem a casar
        :param homography_matrix: matriz de homografia
        :return: imagem panorâmica
        """
        rows_1 = self.image.shape[0]
        cols_1 = self.image.shape[1]
        rows_2 = other_image.image.shape[0]
        cols_2 = other_image.image.shape[1]

        result_image_rows = rows_1 + rows_2
        result_image_cols = cols_1 + cols_2

        result = cv2.warpPerspective(self.image, homography_matrix, (result_image_cols, result_image_rows))
        result[0:rows_2, 0:cols_2] = other_image.image

        panoramic_image = PanoramicImage()
        panoramic_image.image = result

        return panoramic_image

    def image_matches(self, other_image: 'PanoramicImage', max_draw=15) -> 'PanoramicImage':
        """
        Desenha as duas imagens e suas semelhanças
        :param other_image: imagem a ser comparada
        :param max_draw: quantidade máxima de semelhanças a serem desenhadas
        :return: imagem com retas entre seus pontos de semelhança
        """
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(self.descriptor, other_image.descriptor)

        result = np.zeros(shape=(self.image.shape[0], self.image.shape[1] + other_image.image.shape[1]))
        result = cv2.drawMatches(self.image, self.key_points, other_image.image, other_image.key_points, matches[:max_draw], result, flags=2)

        image_matches = PanoramicImage()
        image_matches.image = result

        return image_matches

    def save(self) -> None:
        """
        Salva a imagem atual no path dela
        """
        cv2.imwrite(self.image_path, self.image)

    def crop_borders(self) -> None:
        """
        Remove as bordas pretas a direita e inferior da imagem panorâmica
        """
        last_empty_row = self.image.shape[0]
        last_empty_col = self.image.shape[1]

        # Remove borda da direita
        while np.sum(self.image[last_empty_row - 1, 0:-1]) == 0:
            last_empty_row -= 1

        # Remove borda inferior
        while np.sum(self.image[0:-1, last_empty_col - 1]) == 0:
            last_empty_col -= 1

        self.image = self.image[0:last_empty_row, 0:last_empty_col]
