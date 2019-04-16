import sys
from projeto1.image_manager import ImageManager


# Cria imagens filtradas a partir dos arquivos de imagens dados
def generate_example_images():
    ImageManager.create_filtered_image('all', '../pictures/baboon.png')
    ImageManager.create_filtered_image('all', '../pictures/butterfly.png')
    ImageManager.create_filtered_image('all', '../pictures/city.png')
    ImageManager.create_filtered_image('all', '../pictures/house.png')
    ImageManager.create_filtered_image('all', '../pictures/seagull.png')


def main():
    generate_example_images()


if __name__ == '__main__':
    main()
