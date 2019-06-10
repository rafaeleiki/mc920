import cv2
from panoramic_image import PanoramicImage


class Algorithm:

    def set_descriptor(self, extractor, image: PanoramicImage, key_points) -> None:
        key_points, descriptor = extractor.compute(image.image, key_points)
        image.key_points = key_points
        image.descriptor = descriptor

    def match(self, bf, image1: PanoramicImage, image2: PanoramicImage, threshold: int) -> any:
        matches = bf.match(image1.descriptor, image2.descriptor)
        matches = [x for x in matches if x.distance > threshold]
        return matches


class Brief(Algorithm):

    def set_descriptor(self, panoramic_image: PanoramicImage) -> None:
        star = cv2.xfeatures2d.StarDetector_create()
        brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()
        key_points = star.detect(panoramic_image.image, None)
        super().set_descriptor(brief, panoramic_image, key_points)

    def get_matches(self, image1: PanoramicImage, image2: PanoramicImage, threshold: int) -> any:
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        return super().match(bf, image1, image2, threshold)


class Orb(Algorithm):

    def set_descriptor(self, panoramic_image: PanoramicImage) -> None:
        orb = cv2.ORB_create()
        key_points = orb.detect(panoramic_image.image, None)
        super().set_descriptor(orb, panoramic_image, key_points)

    def get_matches(self, image1: PanoramicImage, image2: PanoramicImage, threshold: int) -> any:
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        return super().match(bf, image1, image2, threshold)
