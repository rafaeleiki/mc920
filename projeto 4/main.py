import sys
from panoramic_image_generator import PanoramicImageGenerator


def generate_example():
    """
    Gera todas as imagens de exemplo do diretório pictures
    """
    generator = PanoramicImageGenerator('./results/', 5)
    for i in range(1, 6):
        base_filename = "./pictures/foto{0}".format(i)
        generator.generate_image(base_filename + "A.jpg", base_filename + "B.jpg", 'foto{0}'.format(i))


def main():
    """
    """
    if sys.argv[1] == 'example':
        generate_example()
    else:
        (_, image_path1, image_path2, threshold, output_dir, output_filename) = sys.argv
        generator = PanoramicImageGenerator(output_dir, 5)
        generator.generate_image(image_path1, image_path2, output_filename)


if __name__ == '__main__':
    main()
