import cv2
from panoramic_image import PanoramicImage


class Algorithm:
    """
    Classe de base para as classes que implementam os algoritmos de descritores
    """

    def set_descriptor(self, extractor, image: PanoramicImage, key_points) -> None:
        key_points, descriptor = extractor.compute(image.image, key_points)
        image.key_points = key_points
        image.descriptor = descriptor

    def match(self, bf, image1: PanoramicImage, image2: PanoramicImage, threshold: float) -> any:
        matches = bf.knnMatch(image1.descriptor, image2.descriptor, k=2)
        matches = [a for (a, b) in matches if a.distance < b.distance * threshold]
        return matches


class Brief(Algorithm):
    """
    Implementa o descritor e o match das imagens usando o algoritmo BRIEF
    """

    def set_descriptor(self, panoramic_image: PanoramicImage) -> None:
        star = cv2.xfeatures2d.StarDetector_create()
        brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()
        key_points = star.detect(panoramic_image.image, None)
        super().set_descriptor(brief, panoramic_image, key_points)

    def get_matches(self, image1: PanoramicImage, image2: PanoramicImage, threshold: float) -> any:
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        return super().match(bf, image1, image2, threshold)


class Orb(Algorithm):
    """
    Implementa o descritor e o match das imagens usando o algoritmo ORB
    """

    def set_descriptor(self, panoramic_image: PanoramicImage) -> None:
        orb = cv2.ORB_create()
        key_points = orb.detect(panoramic_image.image, None)
        super().set_descriptor(orb, panoramic_image, key_points)

    def get_matches(self, image1: PanoramicImage, image2: PanoramicImage, threshold: float) -> any:
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        return super().match(bf, image1, image2, threshold)
