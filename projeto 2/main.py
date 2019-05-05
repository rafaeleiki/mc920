import sys
from image_manager import ImageManager


def generate_example():
    ImageManager.create_dithering('../pictures/baboon.pgm', './results/', 'all', 'baboon')
    ImageManager.create_dithering('../pictures/fiducial.pgm', './results/', 'all', 'fiducial')
    ImageManager.create_dithering('../pictures/monarch.pgm', './results/', 'all', 'monarch')
    ImageManager.create_dithering('../pictures/peppers.pgm', './results/', 'all', 'peppers')
    ImageManager.create_dithering('../pictures/retina.pgm', './results/', 'all', 'retina')
    ImageManager.create_dithering('../pictures/sonnet.pgm', './results/', 'all', 'sonnet')
    ImageManager.create_dithering('../pictures/wedge.pgm', './results/', 'all', 'wedge')


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
