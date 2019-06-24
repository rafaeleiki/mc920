import sys
from color_quantization import ColorQuantizationImage


def generate_example():
    """
    Gera todas as imagens de exemplo do diretório pictures

    """
    example_image_list = [
        ('baboon', 'png'),
        ('monalisa', 'png'),
        ('peppers', 'png'),
        ('watch', 'png'),
    ]

    # Gera para cada quantidade de cor
    for color_count in [8, 16, 32, 64, 128]:
        for image in example_image_list:
            (file, file_format) = image
            params = {"file": file, "format": file_format, "color_count": color_count}
            generate_image('./pictures/{file}.{format}'.format(**params),
                           './results/{file}_{color_count}.{format}'.format(**params),
                           color_count)


def generate_image(input_path, output_path, colors_count):
    """
    Gera uma imagem mudando suas cores
    :param input_path: arquivo de entrada
    :param output_path: arquivo de saída
    :param colors_count: quantidade de cores
    """
    color_quantization = ColorQuantizationImage(input_path)
    color_quantization.create_quantized(output_path, colors_count)


def main():
    """
    Programa que gera uma versão da imagem com até uma certa quantidade de cores.
    Pode ser usado de 2 formas:
        - python main.py example => gera todas as imagens no diretório "pictures"
        - python mian.py arq_entrada arq_saida cores => gera a imagem na saída dada com o limite de cores fornecido
    """
    if sys.argv[1] == 'example':
        generate_example()
    else:
        (_, input_path, output_path, colors_count) = sys.argv
        colors_count = int(colors_count)
        generate_image(input_path, output_path, colors_count)


if __name__ == '__main__':
    main()
