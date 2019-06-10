import sys

from algorithms import Orb, Brief
from panoramic_image_generator import PanoramicImageGenerator


def generate_example(threshold):
    """
    Gera todas as imagens de exemplo do diretório pictures
    """
    for algorithm_name in ['orb', 'brief']:
        algorithm = get_algorithm(algorithm_name)
        generator = PanoramicImageGenerator(algorithm, './results/{0}/'.format(algorithm_name), threshold)
        for i in range(1, 6):
            base_filename = "./pictures/foto{0}".format(i)
            generator.generate_image(base_filename + "A.jpg", base_filename + "B.jpg", 'foto{0}'.format(i))


def get_algorithm(algorithm_name: str):
    if algorithm_name == 'orb':
        return Orb()
    elif algorithm_name == 'brief':
        return Brief()
    else:
        print("Algoritmo inválido; Os possíveis são: orb, brief")
        exit(1)


def main():
    """
    """
    if sys.argv[1] == 'example':
        generate_example(int(sys.argv[2]))
    else:
        (_, image_path1, image_path2, algorithm_name, threshold, output_dir, output_filename) = sys.argv

        algorithm = get_algorithm(algorithm_name)
        generator = PanoramicImageGenerator(algorithm, output_dir, int(threshold))
        generator.generate_image(image_path1, image_path2, output_filename)


if __name__ == '__main__':
    main()
