import cv2
import numpy as np
import subprocess
import math

WHITE = 0
BLACK = 1


class ConnectedComponent:

    def __init__(self, image, x1, y1, x2, y2):
        self.image = image
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.dx = x2 - x1
        self.dy = y2 - y1
        self.area = self.dx * self.dy
        self.words = []
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
        self.black_pixel_proportion = self.black_pixel / self.area

    def calc_pixels_transitions(self):
        self.vertical_transitions = 0.0
        self.horizontal_transitions = 0.0

        for row in range(self.y1, self.y2):
            for col in range(self.x1, self.x2 + 1):
                if self.image[row, col] == WHITE and self.image[row + 1, col] == BLACK:
                    self.vertical_transitions += 1

        for col in range(self.x1, self.x2):
            for row in range(self.y1, self.y2 + 1):
                if self.image[row, col] == WHITE and self.image[row, col + 1] == BLACK:
                    self.horizontal_transitions += 1

        self.vertical_proportions = self.vertical_transitions / self.black_pixel
        self.horizontal_proportions = self.horizontal_transitions / self.black_pixel

    def find_words(self, use_threshold=True):
        self.words = []
        spaces = self.find_word_spaces()

        space_sizes = [space["size"] for space in spaces]

        if use_threshold:
            threshold = np.sum(space_sizes) / len(spaces) + 1
        else:
            threshold = 0

        if len(spaces) > 0 and np.std(space_sizes) * 1.2 >= threshold:
            word_start = self.x1

            for i in range(len(spaces)):
                if spaces[i]["size"] >= threshold:
                    self.words.append((word_start, spaces[i]["start"] - 1))
                    word_start = spaces[i]["end"]

            if word_start != self.x2:
                self.words.append((word_start, self.x2))
        else:
            self.words.append((self.x1, self.x2))

    def find_word_spaces(self):
        spaces = []
        space_count = 0
        start = self.x1 - 1

        for col in range(self.x1, self.x2 + 1):
            if np.sum(self.image[self.y1:self.y2, col]) <= BLACK * self.dy * 0.05:
                space_count += 1
            else:
                if space_count > 0:
                    spaces.append({
                        "size": space_count,
                        "start": start,
                        "end": start + space_count
                    })
                    space_count = 0
                start = col

        if space_count > 0:
            spaces.append({
                "size": space_count,
                "start": start,
                "end": start + space_count
            })

        return spaces

    def draw_component_rectangle(self, rect):
        x1 = rect[0]
        x2 = rect[1]

        y1 = self.y1
        y2 = self.y2

        for col in range(x1, x2 + 1):
            self.image[y1, col] = BLACK
            self.image[y2, col] = BLACK

        for row in range(y1, y2 + 1):
            self.image[row, x1] = BLACK
            self.image[row, x2] = BLACK

    def draw_word_rectangles(self):
        for word in self.words:
            self.draw_component_rectangle(word)

    def is_text(self):
        return (
                (0.2 <= self.black_pixel_proportion <= 0.6
                 and self.vertical_proportions < 0.8
                 and self.horizontal_proportions < 0.8)
                or
                (self.vertical_proportions > 0.5 and self.horizontal_proportions > 0.5
                    and self.black_pixel_proportion > 0.12)
        ) # rule 6
        # return 0.2 <= self.black_pixel_proportion <= 0.64  # rule 5
        # return self.black_pixel_proportion >= 0.2  # rule 4
        # return self.black_pixel_proportion >= 0.2 and self.vertical_proportions > 0.14  # rule 3
        # return self.area >= 12 and self.vertical_proportions > 0.14  # rule 2
        # return self.vertical_proportions > 0.14 # rule 1


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
        result6 = cv2.morphologyEx(result5, cv2.MORPH_CLOSE, kernel6)
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
                    component = ConnectedComponent(normalized_image, x1, y1, x2, y2)
                    if component.is_text():
                        components.append(component)

                elif line.find("Number of connected components") >= 0:
                    process = True

        # Passo 9 e 10

        # Versão sem operador morfológico
        # words_count = 0
        # for component in components:
        #     component.find_words()
        #     # component.draw_word_rectangles()
        #     words_count += len(component.words)
        # print("Words count: {}".format(words_count))

        # Versão com operador morfológico
        new_image = np.zeros(img.shape)

        for component in components:
            y1 = component.y1
            y2 = component.y2
            x1 = component.x1
            x2 = component.x2
            component_kernel = np.ones((1, math.floor(component.dy * 0.36) + 1), np.uint8)
            new_image[y1:y2, x1:x2] = cv2.morphologyEx(normalized_image[y1:y2, x1:x2], cv2.MORPH_CLOSE, component_kernel)
            component.image = new_image
            component.find_words(False)
            # component.image = new_image
            # component.draw_word_rectangles()

        # words_kernel = np.ones((1, 12), np.uint8)
        # new_image = cv2.morphologyEx(new_image, cv2.MORPH_CLOSE, words_kernel)

        words_count = 0
        for component in components:
            # component.image = new_image
            # component.find_words(False)
            component.image = normalized_image
            component.draw_word_rectangles()
            words_count += len(component.words)
        print("Words count: {}".format(words_count))

        cv2.imwrite(intermediate_path.replace(".pbm", "_test.pbm"), new_image)

        normalized_image = 1 - normalized_image
        normalized_image *= 255
        cv2.imwrite(path.replace(".pbm", "_final.pbm"), normalized_image)
        print("Finished " + path)

        # cv2.waitKey(0)
