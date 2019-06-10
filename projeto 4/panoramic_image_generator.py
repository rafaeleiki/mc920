from algorithms import Algorithm
from panoramic_image import PanoramicImage


class PanoramicImageGenerator:

    def __init__(self, algorithm: Algorithm, result_dir: str, threshold: float):
        self.algorithm = algorithm
        self.result_dir = result_dir
        self.threshold = threshold

    def generate_image(self, image_1_path: str, image_2_path: str, result_filename: str) -> None:
        """
        Gera uma image panorâmica
        :param image_1_path: caminho para a primeira imagem
        :param image_2_path: caminho para a segunda imagem
        :param result_filename: nome base do arquivo de imagem resultante
        """
        image1 = PanoramicImage(image_1_path)
        image2 = PanoramicImage(image_2_path)

        # Passo 1
        gray_image_1 = image1.image = image1.to_gray_scale()
        gray_image_2 = image2.image = image2.to_gray_scale()

        # Passo 2
        self.algorithm.set_descriptor(image1)
        self.algorithm.set_descriptor(image2)

        # Passos 3 e 4
        matches = self.algorithm.get_matches(image1, image2, self.threshold)

        # Desenha a imagem do passo 8s
        # Volta para a imagem colorida antes de desenhar
        image1.reset_to_original_image()
        image2.reset_to_original_image()

        image_with_lines = image1.image_matches(image2)

        image1.image = gray_image_1
        image2.image = gray_image_2

        # Passo 5
        # Se teve a quantidade mínima de matches, continua
        min_matches = 4
        if len(matches) < min_matches:
            print("As imagens não são semelhantes o suficiente, %d (esperado %d)" % (len(matches), min_matches))

        else:
            homography_matrix = image1.ransac_matrix(image2, matches)

            if homography_matrix is None:
                print("Erro na matriz de homografia")
            else:

                # Passos 6 e 7
                image1.reset_to_original_image()
                image2.reset_to_original_image()
                panoramic_image = image1.merge_panoramic(image2, homography_matrix)

                # Escreve os resultados em arquivo
                base_path = self.result_dir + result_filename

                image_with_lines.image_path = base_path + '_lines.jpeg'
                image_with_lines.save()

                panoramic_image.image_path = base_path + '_panoramic.jpeg'
                panoramic_image.crop_borders()
                panoramic_image.save()
