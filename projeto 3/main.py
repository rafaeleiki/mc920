import sys
from image_manager import ImageManager


def generate_example():
    """
    Gera todas as imagens de exemplo do diretório pictures
    """
    ImageManager.analyze_image('./pictures/text.pbm', './results/text_7.pbm')
    ImageManager.analyze_image('./pictures/letter_a.ascii.pbm', './results/a_7.pbm')
    ImageManager.analyze_image('./pictures/fool.ascii.pbm', './results/asc_7.pbm')
    ImageManager.analyze_image('./pictures/math_emporium.pbm', './results/math_7.pbm')
    ImageManager.analyze_image('./pictures/scs.ascii.pbm', './results/scs_7.pbm')

def main():
    """
    """
    use_morphological = sys.argv.index("-a") < 0
    ImageManager.analyze_image(sys.argv[1], sys.argv[2], use_morphological)


if __name__ == '__main__':
    main()
