import cv2
import numpy as np


class ImageFilter:

    def filter(self, matrix, input_file, output_file):
        img_file = cv2.imread(input_file)
        new_img = cv2.filter2D(img_file, -1, matrix)
        cv2.imwrite(output_file, new_img)
        print(f"Arquivo '{output_file}' escrito")

    def filter_a(self):
        matrix = [[0,  0, -1,  0, 0],
                  [0, -1, -2, -1, 0],
                  [-1, -2, 16, -2, -1],
                  [0, -1, -2, -1, 0],
                  [0,  0, -1,  0, 0]]
        matrix = np.array(matrix)
        self.filter(matrix, "../pictures/city.png", "./results/city_a.png")

    def filter_b(self):
        matrix = [[1,  4, 6,  4, 1],
                  [4, 16, 24, 16, 4],
                  [6, 24, 36, 24, 6],
                  [4, 16, 24, 16, 4],
                  [1,  4, 6,  4, 1]]
        matrix = np.array(matrix) / 256
        self.filter(matrix, "../pictures/city.png", "./results/city_b.png")

    def filter_c(self):
        matrix = [[-1, 0, 1],
                  [-2, 0, 2],
                  [-1, 0, 1]]
        matrix = np.array(matrix)
        self.filter(matrix, "../pictures/city.png", "./results/city_c.png")

    def filter_d(self):
        matrix = [[-1, -2, -1],
                  [0, 0, 0],
                  [1, 2, 1]]
        matrix = np.array(matrix)
        self.filter(matrix, "../pictures/city.png", "./results/city_d.png")

    def filter_c_d(self):
        img_file_c = np.float32(cv2.imread("./results/city_c.png"))
        img_file_d = np.float32(cv2.imread("./results/city_d.png"))
        square = np.square(img_file_c) + np.square(img_file_d)
        cv2.imwrite("./results/city_c_d.png", np.sqrt(square))
        print("Arquivo './results/city_c_d.png' escrito")
