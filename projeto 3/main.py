import sys
from image_manager import ImageManager


def generate_example():
    """
    Gera todas as imagens de exemplo do diretório pictures
    """
    ImageManager.analyze_image('./pictures/text.pbm', './results/text.pbm')
    ImageManager.analyze_image('./pictures/letter_a.pbm', './results/letter_a.pbm')
    ImageManager.analyze_image('./pictures/map.pbm', './results/map.pbm')
    ImageManager.analyze_image('./pictures/scs.ascii.pbm', './results/scs.pbm')
    ImageManager.analyze_image('./pictures/paper.pbm', './results/paper.pbm')
    ImageManager.analyze_image('./pictures/rabbit.pbm', './results/rabbit.pbm')


def main():
    """
    Programa que dada uma imagem PBM coloca retângulo ao redor das palavras, conta elas e o número de linhas.
    Parâmetros da linha de comando:
    1. Path do arquivo de entrada ou "example", para gerar todos os exemplos
    2. Path do arquivo de saída
    3. Flag opcional "-a" para usar o algoritmo que considera limiar para classificar palavras
    """
    if sys.argv[1] == 'example':
        generate_example()
    else:
        use_morphological = "-a" not in sys.argv
        ImageManager.analyze_image(sys.argv[1], sys.argv[2], use_morphological)


if __name__ == '__main__':
    main()
