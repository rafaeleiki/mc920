import sys
from image_manager import ImageManager


def generate_example():
    """
    Gera todas as imagens de exemplo do diretório pictures
    """


def main():
    """
    """
    ImageManager.analyze_image('./pictures/text.pbm', './results/text_7.pbm')
    ImageManager.analyze_image('./pictures/letter_a.ascii.pbm', './results/a_7.pbm')
    ImageManager.analyze_image('./pictures/fool.ascii.pbm', './results/asc_7.pbm')
    ImageManager.analyze_image('./pictures/math_emporium.pbm', './results/math_7.pbm')
    ImageManager.analyze_image('./pictures/scs.ascii.pbm', './results/scs_7.pbm')


if __name__ == '__main__':
    main()
