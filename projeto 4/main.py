import sys

from algorithms import Orb, Brief
from panoramic_image_generator import PanoramicImageGenerator


def generate_example(threshold):
    """
    Gera todas as imagens de exemplo do diretório pictures

    """
    # Gera para cada algoritmo todos os resultados
    for algorithm_name in ['orb', 'brief']:
        algorithm = get_algorithm(algorithm_name)
        generator = PanoramicImageGenerator(algorithm, './results/{0}/'.format(algorithm_name), threshold)

        # Gera todas as imagens de exemplo
        for i in range(1, 6):
            base_filename = "./pictures/foto{0}".format(i)
            generator.generate_image(base_filename + "A.jpg", base_filename + "B.jpg", 'foto{0}'.format(i))


def get_algorithm(algorithm_name: str):
    """
    Retorna o algoritmo correspondente ao nome dado
    :param algorithm_name: nome do algoritmo
    :return: objeto do algoritmo a ser usado para gerar o descritor
    """
    if algorithm_name == 'orb':
        return Orb()
    elif algorithm_name == 'brief':
        return Brief()
    else:
        print("Algoritmo inválido; Os possíveis são: orb, brief")
        exit(1)


def main():
    """
    Programa que une duas imagens para criar uma panorâmica. Há duas formas de usar esse programa:
    Opção 1: parâmetros "example THRESHOLD", onde THRESHOLD é um float que indica o limiar para selecionar as correspondências
    Opção 2: parâmetros "in1 in2 algoritmo limiar dir_saida arq_saida", onde:
        1. in1 e in2 são o path para os dois arquivos de imagens;
        2. algoritmo é o nome do algoritmo a ser usado (brief ou orb)
        3. limiar é o valor mínimo da % da diferença da distância para selecionar a correspondência
        4. dir_saida é o diretório de saída do resultado (deve ter / no final)
        5. arq_saida é o nome do arquivo de saída, sem a extensão
    """
    if sys.argv[1] == 'example':
        generate_example(float(sys.argv[2]))
    else:
        (_, image_path1, image_path2, algorithm_name, threshold, output_dir, output_filename) = sys.argv

        algorithm = get_algorithm(algorithm_name)
        generator = PanoramicImageGenerator(algorithm, output_dir, float(threshold))
        generator.generate_image(image_path1, image_path2, output_filename)


if __name__ == '__main__':
    main()
