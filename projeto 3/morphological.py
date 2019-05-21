import cv2
import numpy as np
import subprocess
import math
from connected_component import ConnectedComponent


class Morphological:

    def analyze_text_image(self, input_path, output_path, use_morphologic=True):
        img = cv2.imread(input_path, 0)
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

        intermediate_path = output_path.replace(".pbm", "_intermediate.pbm")
        cv2.imwrite(intermediate_path, result6)

        # Passo 7
        subprocess.call(["gcc", "comp_conexos.c"])
        box_file_path = intermediate_path + ".tmp"
        intermediate_output_path = intermediate_path.replace(".pbm", "_out.pbm")
        with open(box_file_path, "w") as box_file:
            subprocess.call(["./a.out", intermediate_path, intermediate_output_path], stdout=box_file)

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
        if use_morphologic:
            a = self.__find_words_using_morphological_filter(normalized_image, components)
            cv2.imwrite(output_path.replace(".pbm", "_aaa.pbm"), a)
        else:
            self.__find_words_using_algorithm(components)

        # Desenha retângulos e conta palavras
        words_count = 0
        for component in components:
            component.draw_word_rectangles()
            words_count += len(component.words)

        normalized_image = 1 - normalized_image
        normalized_image *= 255
        cv2.imwrite(output_path, normalized_image)

        print("Finished \"{}\", {} words found".format(output_path, words_count))

    def __find_words_using_morphological_filter(self, image, components):
        new_image = np.zeros(image.shape)

        for component in components:
            y1 = component.y1
            y2 = component.y2
            x1 = component.x1
            x2 = component.x2
            component_kernel = np.ones((2 * component.dy, math.ceil(component.dy * 0.22 + 0.62)), np.uint8)
            new_image[y1:y2, x1:x2] = cv2.morphologyEx(image[y1:y2, x1:x2], cv2.MORPH_CLOSE, component_kernel)
            component.image = new_image
            component.find_words(False)
            component.image = image

        return new_image

    def __find_words_using_algorithm(self, components):
        for component in components:
            component.find_words()
