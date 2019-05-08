import sys
from image_manager import ImageManager


def generate_example():
    """
    Gera todas as imagens de exemplo do diretório pictures
    """
    ImageManager.create_dithering('../pictures/baboon.pgm', './results/', 'all', 'baboon')
    ImageManager.create_dithering('../pictures/fiducial.pgm', './results/', 'all', 'fiducial')
    ImageManager.create_dithering('../pictures/monarch.pgm', './results/', 'all', 'monarch')
    ImageManager.create_dithering('../pictures/peppers.pgm', './results/', 'all', 'peppers')
    ImageManager.create_dithering('../pictures/retina.pgm', './results/', 'all', 'retina')
    ImageManager.create_dithering('../pictures/sonnet.pgm', './results/', 'all', 'sonnet')
    ImageManager.create_dithering('../pictures/wedge.pgm', './results/', 'all', 'wedge')
    ImageManager.create_dithering('../pictures/dragon.pgm', './results/', 'all', 'dragon')
    ImageManager.create_dithering('../pictures/beach.pgm', './results/', 'all', 'beach')


def main():
    """
    Aplica técnica(s) de pontilhamento(s) em uma imagem. Parâmetros da linha de comando:
    1. Tipo de técnica, podendo ser: ordered_dithering, bayer, floyd_steinberg, floyd_steinberg_alternate, all, example
    2. Caminho para a imagem de entrada
    3. Caminho para a imagem resultante ou diretório de saída (apenas para a opção "all")
    4. *Usado somente para a opção all* - Nome do arquivo base para gerar as versões de saída
    """
    type = sys.argv[1]

    if type == 'example':
        generate_example()
    else:
        input_path = sys.argv[2]
        output_path = sys.argv[3]
        filename = sys.argv[4] if len(sys.argv) > 5 else ''

        ImageManager.create_dithering(input_path, output_path, type, filename)


if __name__ == '__main__':
    main()
