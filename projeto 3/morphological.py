import cv2
import numpy as np
import subprocess

WHITE = 0
BLACK = 1


class ConnectedComponent:

    def __init__(self, image, x1, y1, x2, y2):
        self.image = image
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.black_pixel = None
        self.black_pixel_proportion = None
        self.vertical_transitions = None
        self.vertical_proportions = None
        self.horizontal_transitions = None
        self.horizontal_proportions = None
        self.calc_pixels_proportions()
        self.calc_pixels_transitions()

    def calc_pixels_proportions(self):
        self.black_pixel = np.sum(self.image[self.y1:self.y2, self.x1:self.x2])
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        self.black_pixel_proportion = self.black_pixel / (dx * dy)

    def calc_pixels_transitions(self):
        self.vertical_transitions = 0.0
        self.horizontal_transitions = 0.0

        for row in range(self.y1, self.y2):
            for col in range(self.x1, self.x2):
                if self.image[row, col] == WHITE and self.image[row + 1, col] == BLACK:
                    self.vertical_transitions += 1

        for col in range(self.x1, self.x2):
            for row in range(self.y1, self.y2):
                if self.image[row, col] == WHITE and self.image[row, col + 1] == BLACK:
                    self.horizontal_transitions += 1

        self.vertical_proportions = self.vertical_transitions / self.black_pixel_proportion
        self.horizontal_proportions = self.horizontal_transitions / self.black_pixel_proportion

    def draw_rectangle(self):
        for col in range(self.x1, self.x2):
            self.image[self.y1, col] = BLACK
            self.image[self.y2, col] = BLACK

        for row in range(self.y1, self.y2):
            self.image[row, self.x1] = BLACK
            self.image[row, self.x2] = BLACK


class Morphological:

    def analyze_text_image(self, path, intermediate_path):
        img = cv2.imread(path, 0)
        img = np.invert(img)

        # Passo 1: dilatação
        kernel1 = np.ones((1, 100), np.uint8)
        result1 = cv2.dilate(img, kernel1)
        cv2.imshow('1', result1)

        # Passo 2: erosão
        result1 = cv2.erode(result1, kernel1)
        cv2.imshow('2', result1)

        # Passo 3: dilatação
        kernel3 = np.ones((200, 1), np.uint8)
        result3 = cv2.dilate(img, kernel3)
        cv2.imshow('3', result3)

        # Passo 4: erosão
        result3 = cv2.erode(result3, kernel3)
        cv2.imshow('4', result3)

        # Passo 5: intersecção
        result5 = cv2.bitwise_and(result1, result3)
        cv2.imshow('5', result5)

        # Passo 6: fechamento
        kernel6 = np.ones((1, 30), np.uint8)
        result6 = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel6)
        result6 = np.invert(result6)
        cv2.imwrite(intermediate_path, result6)

        # Passo 7
        subprocess.call(["gcc", "comp_conexos.c"])
        box_file_path = intermediate_path + ".tmp"
        with open(box_file_path, "w") as box_file:
            subprocess.call(["./a.out", intermediate_path, "./results/text.pbm"], stdout=box_file)

        # Passo 8
        components = []
        normalized_image = img / img.max()

        with open(box_file_path, "r") as box_file:
            process = False

            for line in box_file:
                if process:
                    x1, y1, x2, y2 = [int(string) for string in line.rstrip().split(", ")]
                    components.append(ConnectedComponent(normalized_image, x1, y1, x2, y2))

                elif line.find("Number of connected components") >= 0:
                    process = True

        # Passo 9

        # Passo 10
        for component in components:
            component.draw_rectangle()

        normalized_image = 1 - normalized_image
        normalized_image *= 255
        cv2.imwrite("./results/final.pbm", normalized_image)

        cv2.waitKey(0)
