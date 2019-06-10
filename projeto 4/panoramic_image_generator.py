import cv2
from panoramic_image import PanoramicImage


class PanoramicImageGenerator:

    def __init__(self, result_dir: str, threshold: int):
        self.result_dir = result_dir
        self.threshold = threshold

    def generate_image(self, image_1_path: str, image_2_path: str, result_filename: str):
        image1 = PanoramicImage(image_1_path)
        image2 = PanoramicImage(image_2_path)

        # Passo 1
        gray_image_1 = image1.image = image1.to_gray_scale()
        gray_image_2 = image2.image = image2.to_gray_scale()

        # Passo 2
        image1.orb()
        image2.orb()

        # Passos 3 e 4
        matches = image1.compare_orb_match(image2, self.threshold)

        # Desenha a imagem do passo 8s
        image1.reset_to_original_image()
        image2.reset_to_original_image()

        image_with_lines = image1.image_matches(image2)

        image1.image = gray_image_1
        image2.image = gray_image_2

        # Passo 5
        _, M = image1.ransac_matches(image2, matches, 10)

        # Passos 6 e 7
        image1.reset_to_original_image()
        image2.reset_to_original_image()
        panoramic_image = image1.panoramic_merge(image2, M)

        # Escreve os resultados em arquivo
        base_path = self.result_dir + result_filename
        cv2.imwrite(base_path + '_lines.jpeg', image_with_lines)
        cv2.imwrite(base_path + '_panoramic.jpeg', panoramic_image)
