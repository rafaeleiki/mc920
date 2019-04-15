import cv2
import numpy as np


class ImageFilter:

    @staticmethod
    def filter(matrix, input_file, output_file):
        img_file = cv2.imread(input_file)
        new_img = cv2.filter2D(img_file, -1, matrix)
        cv2.imwrite(output_file, new_img)
        ImageFilter.__log_file_creation(output_file)

    @staticmethod
    def filter_a(input_file, output_file):
        matrix = [[0,  0, -1,  0, 0],
                  [0, -1, -2, -1, 0],
                  [-1, -2, 16, -2, -1],
                  [0, -1, -2, -1, 0],
                  [0,  0, -1,  0, 0]]
        matrix = np.array(matrix)
        ImageFilter.filter(matrix, input_file, output_file)

    @staticmethod
    def filter_b(input_file, output_file):
        matrix = [[1,  4, 6,  4, 1],
                  [4, 16, 24, 16, 4],
                  [6, 24, 36, 24, 6],
                  [4, 16, 24, 16, 4],
                  [1,  4, 6,  4, 1]]
        matrix = np.array(matrix) / 256
        ImageFilter.filter(matrix, input_file, output_file)

    @staticmethod
    def filter_c(input_file, output_file):
        matrix = [[-1, 0, 1],
                  [-2, 0, 2],
                  [-1, 0, 1]]
        matrix = np.array(matrix)
        ImageFilter.filter(matrix, input_file, output_file)

    @staticmethod
    def filter_d(input_file, output_file):
        matrix = [[-1, -2, -1],
                  [0, 0, 0],
                  [1, 2, 1]]
        matrix = np.array(matrix)
        ImageFilter.filter(matrix, input_file, output_file)

    @staticmethod
    def filter_c_d(file_1, file_2, output_file):
        img_file_c = np.float32(cv2.imread(file_1))
        img_file_d = np.float32(cv2.imread(file_2))
        square = np.square(img_file_c) + np.square(img_file_d)
        cv2.imwrite(output_file, np.sqrt(square))
        ImageFilter.__log_file_creation(output_file)

    @staticmethod
    def __log_file_creation(file):
        print(f"Arquivo '{file}' escrito")
