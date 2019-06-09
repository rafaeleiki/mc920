import cv2
import numpy as np


class PanoramicImage:

    def __init__(self, image_path):
        self.image = self.original_image = cv2.imread(image_path)
        self.key_points = None
        self.descriptor = None

    def reset_to_original_image(self):
        self.image = self.original_image

    def show(self):
        cv2.imshow('image', self.image)
        # cv2.waitKey(0)

    def to_gray_scale(self):
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def orb(self) -> None:
        orb = cv2.ORB_create()
        key_points = orb.detect(self.image, None)
        self.key_points, self.descriptor = orb.compute(self.image, key_points)

    def compare_orb_match(self, other_image: 'PanoramicImage', threshold: float):
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(self.descriptor, other_image.descriptor)

        # Mantém só as melhores correspondências
        matches = [x for x in matches if x.distance > threshold]
        return matches

    def ransac_matches(self, other_image: 'PanoramicImage', matches, min_matches: int):
        image = self.image
        M = None

        if len(matches) >= min_matches:
            points1 = np.float32([self.key_points[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
            points2 = np.float32([other_image.key_points[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(points1, points2, cv2.RANSAC, 5.0)
            # matchesMask = mask.ravel().tolist()

            last_row = self.image.shape[0] - 1
            last_col = self.image.shape[1] - 1
            pts = np.float32([[0, 0], [0, last_row], [last_col, last_row], [last_col, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            image = cv2.polylines(other_image.image, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

        else:
            print("Not enough matches are found - %d/%d" % (len(matches), min_matches))
            # matchesMask = None

        return image, M

    def panoramic_merge(self, other_image: 'PanoramicImage', M):
        rows_1 = self.image.shape[0]
        cols_1 = self.image.shape[1]
        rows_2 = other_image.image.shape[0]
        cols_2 = other_image.image.shape[1]

        result_image_rows = rows_1
        result_image_cols = cols_1 + cols_2

        result = cv2.warpPerspective(self.image, M, (result_image_cols, result_image_rows))
        result[0:rows_2, 0:cols_2] = other_image.image

        return result

    def image_matches(self, other_image: 'PanoramicImage'):
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(self.descriptor, other_image.descriptor)
        result = np.zeros(shape=(self.image.shape[0], self.image.shape[1] + other_image.image.shape[1]))
        result = cv2.drawMatches(self.image, self.key_points, other_image.image, other_image.key_points, matches, result, flags=2)
        return result
