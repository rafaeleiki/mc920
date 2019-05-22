import numpy as np

WHITE = 0
BLACK = 1


class ConnectedComponent:

    def __init__(self, image, x1, y1, x2, y2):
        """
        Construtor de uma componente conexa
        :param image: imagem analisada
        :param x1: x do ponto de origem do retângulo
        :param y1: y do ponto de origem do retângulo
        :param x2: x do ponto final do retângulo
        :param y2: y do ponto final do retângulo
        """
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
        """
        Calcula a proporção de pixels pretos na componente
        """
        self.black_pixel = np.sum(self.image[self.y1:self.y2, self.x1:self.x2])

        if self.black_pixel == 0:
            self.black_pixel_proportion = 0
        else:
            self.black_pixel_proportion = self.black_pixel / self.area

    def calc_pixels_transitions(self):
        """
        Calcula a proporção de transições de branco para preto na vertical e horizontal
        """
        self.vertical_transitions = 0.0
        self.horizontal_transitions = 0.0

        # Transições verticais
        for row in range(self.y1, self.y2):
            for col in range(self.x1, self.x2 + 1):
                if self.image[row, col] == WHITE and self.image[row + 1, col] == BLACK:
                    self.vertical_transitions += 1

        # Transições horizontais
        for col in range(self.x1, self.x2):
            for row in range(self.y1, self.y2 + 1):
                if self.image[row, col] == WHITE and self.image[row, col + 1] == BLACK:
                    self.horizontal_transitions += 1

        if self.black_pixel == 0:
            self.vertical_proportions = 0
            self.horizontal_proportions = 0
        else:
            self.vertical_proportions = self.vertical_transitions / self.black_pixel
            self.horizontal_proportions = self.horizontal_transitions / self.black_pixel

    def find_words(self, use_threshold=True):
        """
        Encontra as palavras na componente
        :param use_threshold: define se deve ser usado um limiar
        """
        # Encontra os espaços entre as palavras
        self.words = []
        spaces = self.find_word_spaces()
        space_sizes = [space["size"] for space in spaces]

        # Define o limiar adotado
        if use_threshold:
            threshold = np.sum(space_sizes) / len(spaces) + 1
        else:
            threshold = 0

        # Caso os espaços sejam consideravelmente diferentes, é mais de uma palavra
        if len(spaces) > 0 and np.std(space_sizes) * 1.2 >= threshold:
            word_start = self.x1

            # Monta cada palavra a partir dos espaços
            for i in range(len(spaces)):
                if spaces[i]["size"] >= threshold:
                    self.words.append((word_start, spaces[i]["start"] - 1))
                    word_start = spaces[i]["end"]

            # Caso para a palavra após o último espaço
            if word_start != self.x2:
                self.words.append((word_start, self.x2))
        else:
            self.words.append((self.x1, self.x2))

    def find_word_spaces(self):
        """
        Encontra todos os espaços entre as palavras
        """
        spaces = []
        space_count = 0
        start = self.x1 - 1

        # Percorre a componente horizontalmente
        for col in range(self.x1, self.x2 + 1):

            # Verifica se a coluna possui quase nenhum ponto preto
            if np.sum(self.image[self.y1:self.y2, col]) <= BLACK * self.dy * 0.05:
                space_count += 1
            # Encontrou texto após espaços
            else:
                if space_count > 0:
                    spaces.append({
                        "size": space_count,
                        "start": start,
                        "end": start + space_count
                    })
                    space_count = 0
                start = col

        # Para caso a componente acabe em espaços
        if space_count > 0:
            spaces.append({
                "size": space_count,
                "start": start,
                "end": start + space_count
            })

        return spaces

    def draw_component_rectangle(self, rect):
        """
        Desenha um retângulo em volta de uma palavra
        :param rect: retângulo de uma palavra
        """
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
        """
        Desenha um retângulo em volta de cada palavra da componente
        """
        for word in self.words:
            self.draw_component_rectangle(word)

    def is_text(self):
        """
        Classifica a componente como textual dependendo das propriedades de proporção de pixels pretos
        e de transições de branco para preto
        :return:
        """
        return (
                (0.2 <= self.black_pixel_proportion <= 0.6
                 and self.vertical_proportions < 0.8
                 and self.horizontal_proportions < 0.8)
                or
                (self.vertical_proportions > 0.5 and self.horizontal_proportions > 0.5
                    and self.black_pixel_proportion > 0.12)
        )
