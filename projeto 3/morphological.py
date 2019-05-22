import cv2
import numpy as np
import subprocess
import math
from connected_component import ConnectedComponent


class Morphological:

    @staticmethod
    def analyze_text_image(image, use_morphological=True):
        """
        Analisa um texto, encontrando palavras e linhas e contornando as palavras
        :param image: imagem a ser analisada
        :param use_morphological: define se deve ser usado o operador morfológico para classificar em palavras
        :return: imagem com os retângulos, quantidade de linhas e quantidade de palavras
        """
        original_image = np.invert(image)
        max_value = original_image.max()
        normalized_image = original_image / max_value

        result1 = Morphological.__steps_1_and_2(original_image)     # Passo 1 e 2: dilatação e erosão horizontal
        result3 = Morphological.__steps_3_and_4(original_image)     # Passo 3 e 4: dilatação e erosão vertical
        result5 = cv2.bitwise_and(result1, result3)                 # Passo 5: intersecção
        result6 = Morphological.__step_6(result5)                   # Passo 6: fechamento
        rectangles_file_path = Morphological.__step_7(result6)      # Passo 7: detecção de componentes

        # Passo 8 e 9: definição de componentes de texto
        components = Morphological.__steps_8_and_9(normalized_image, rectangles_file_path)

        # Passo 10
        words_count = Morphological.__step_10(normalized_image, components, use_morphological)
        lines_count = len(components)

        # Volta a imagem para a escala original
        normalized_image = 1 - normalized_image
        normalized_image *= max_value

        return normalized_image, lines_count, words_count

    @staticmethod
    def __steps_1_and_2(original_image):
        """
        Executa dilatação e erosão horizontal
        :param original_image: imagem a ser aplicada
        :return: resultado da operação
        """
        kernel = np.ones((1, 100), np.uint8)
        image = cv2.dilate(original_image, kernel)     # Passo 1
        image = cv2.erode(image, kernel)               # Passo 2
        return image

    @staticmethod
    def __steps_3_and_4(original_image):
        """
        Executa dilatação e erosão vertical
        :param original_image: imagem a ser aplicada
        :return: resultado da operação
        """
        kernel = np.ones((200, 1), np.uint8)
        image = cv2.dilate(original_image, kernel)  # Passo 3
        image = cv2.erode(image, kernel)            # Passo 4
        return image

    @staticmethod
    def __step_6(result5):
        """
        Executa o fechamento da imagem
        :param result5: imagem a ser aplicada
        :return: resultado da operação
        """
        kernel = np.ones((1, 30), np.uint8)
        image = cv2.morphologyEx(result5, cv2.MORPH_CLOSE, kernel)
        return image

    @staticmethod
    def __step_7(result6):
        """
        Encontra as componentes conexas da imagem
        :param result6: imagem a ser procurada
        :return: path do arquivo com os retângulos de cada componente
        """
        result6 = np.invert(result6)
        intermediate_path = './intermediate.pbm'
        cv2.imwrite(intermediate_path, result6)

        subprocess.call(["gcc", "comp_conexos.c"])
        box_file_path = intermediate_path + ".tmp"
        intermediate_output_path = intermediate_path.replace(".pbm", "_out.pbm")
        with open(box_file_path, "w") as box_file:
            subprocess.call(["./a.out", intermediate_path, intermediate_output_path], stdout=box_file)
        return box_file_path

    @staticmethod
    def __steps_8_and_9(image, rectangles_file_path):
        """
        Classifica as componentes conexas de uma imagem em textuais ou não
        :param image: imagem a ser analisada
        :param rectangles_file_path: caminho do arquivo com os retângulos
        :return: componentes textuais encontradas
        """
        components = []

        with open(rectangles_file_path, "r") as rectangles_file:
            process = False

            for line in rectangles_file:

                # Encontrou a linha que começa os retângulos
                if process:
                    x1, y1, x2, y2 = [int(string) for string in line.rstrip().split(", ")]

                    # Passo 8: calcula as razões de pixels
                    component = ConnectedComponent(image, x1, y1, x2, y2)

                    # Passo 9: classificação como texto
                    if component.is_text():
                        components.append(component)

                # Vai avançando no arquivo até encontrar os retângulos
                elif line.find("Number of connected components") >= 0:
                    process = True

        return components

    @staticmethod
    def __step_10(image, components, use_morphological):
        """
        Encontra as palavras nas linhas
        :param image: imagem procurada
        :param components: componentes conexas textuais
        :param use_morphological: define se deve ser usado o operador morfológico
        :return: quantidade de palavras encontradas
        """
        # Passo 10a: classificação em palavras
        if use_morphological:
            Morphological.__find_words_using_morphological_filter(image, components)
        else:
            Morphological.__find_words_using_algorithm(components)

        # Passo 10b: desenho dos retângulos e contagem das palavras
        words_count = 0
        for component in components:
            component.draw_word_rectangles()
            words_count += len(component.words)

        return words_count

    @staticmethod
    def __find_words_using_morphological_filter(image, components):
        """
        Encontra as palavras na imagem com o operador morfológico
        :param image: imagem a ser procurada
        :param components: componentes textuais
        :return: imagem resultante
        """
        new_image = np.zeros(image.shape)

        for component in components:
            y1 = component.y1
            y2 = component.y2
            x1 = component.x1
            x2 = component.x2

            # Realiza o fechamento e procura as divisões entre palavras
            component_kernel = np.ones((2 * component.dy, math.ceil(component.dy * 0.22 + 0.62)), np.uint8)
            new_image[y1:y2, x1:x2] = cv2.morphologyEx(image[y1:y2, x1:x2], cv2.MORPH_CLOSE, component_kernel)
            component.image = new_image
            component.find_words(False)
            component.image = image

        return new_image

    @staticmethod
    def __find_words_using_algorithm(components):
        """
        Encontra as palavras na imagem usando um limiar
        :param components: componentes conexas textuais
        """
        for component in components:
            component.find_words()
