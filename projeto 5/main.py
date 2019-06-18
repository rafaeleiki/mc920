import sys

from color_quantization import ColorQuantizationImage


def generate_example():
    """
    Gera todas as imagens de exemplo do diretório pictures

    """


def main():
    """
    """
    color_quantization = ColorQuantizationImage('./pictures/baboon.png')
    color_quantization.color_quantization(32)


if __name__ == '__main__':
    main()
