import numpy as np


class Dithering:

    @staticmethod
    def floyd_steinberg(image, alternate=True, threshold=128):
        height = image.shape[0]
        width = image.shape[1]

        new_image = np.zeros((height + 1, width + 2), np.float32)
        new_image[0:-1, 1:-1] = image

        for row in range(0, height):

            if not alternate or row % 2 == 0:
                order = 1
                col_range = range(1, width, 1)
            else:
                order = -1
                col_range = range(width, 0, -1)

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
