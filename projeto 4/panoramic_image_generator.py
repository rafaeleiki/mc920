import cv2
from panoramic_image import PanoramicImage


class PanoramicImageGenerator:

    @staticmethod
    def generate_image(image_1_path, image_2_path, threshold, result_path):
        image1 = PanoramicImage(image_1_path)
        image2 = PanoramicImage(image_2_path)

        # Passo 1
        gray_image_1 = image1.image = image1.to_gray_scale()
        gray_image_2 = image2.image = image2.to_gray_scale()

        # Passo 2
        image1.orb()
        image2.orb()

        # Passos 3 e 4
        matches = image1.compare_orb_match(image2, threshold)

        image1.reset_to_original_image()
        image2.reset_to_original_image()
        image_with_lines = image1.image_matches(image2)
        image1.image = gray_image_1
        image2.image = gray_image_2

        _, M = image1.ransac_matches(image2, matches, 10)

        image1.reset_to_original_image()
        image2.reset_to_original_image()
        panoramic_image = image1.panoramic_merge(image2, M)


        cv2.imshow('lines', image_with_lines)
        cv2.imshow('panoramic', panoramic_image)
        cv2.waitKey(0)




