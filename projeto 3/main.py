import sys

from morphological import Morphological


def generate_example():
    """
    Gera todas as imagens de exemplo do diretório pictures
    """


def main():
    """
    """
    m = Morphological()
    m.analyze_text_image('./pictures/text.pbm', './results/text_7.pbm')
    m.analyze_text_image('./pictures/letter_a.ascii.pbm', './results/a_7.pbm')
    m.analyze_text_image('./pictures/fool.ascii.pbm', './results/asc_7.pbm')
    m.analyze_text_image('./pictures/math_emporium.pbm', './results/math_7.pbm')
    m.analyze_text_image('./pictures/scs.ascii.pbm', './results/scs_7.pbm')


if __name__ == '__main__':
    main()
