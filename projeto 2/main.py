import sys
from image_manager import ImageManager


def generate_example():
    ImageManager.create_dithering('../pictures/baboon.png', './results/', 'all', 'baboon')
    ImageManager.create_dithering('../pictures/poney.png', './results/', 'all', 'poney')
    ImageManager.create_dithering('../pictures/butterfly.png', './results/', 'all', 'butterfly')
    ImageManager.create_dithering('../pictures/city.png', './results/', 'all', 'city')
    ImageManager.create_dithering('../pictures/house.png', './results/', 'all', 'house')
    ImageManager.create_dithering('../pictures/seagull.png', './results/', 'all', 'seagull')


def main():
    # type = sys.argv[1]
    type = 'example'

    if type == 'example':
        generate_example()
    else:
        # input_path = sys.argv[2]
        # output_path = sys.argv[3]
        # filename = sys.argv[4]
        input_path = '../pictures/baboon.png'
        output_path = './results/'
        filename = 'baboon'

        ImageManager.create_dithering(input_path, output_path, type, filename)


if __name__ == '__main__':
    main()
