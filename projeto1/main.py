import sys
from image_manager import ImageManager


# Cria imagens filtradas a partir dos arquivos de imagens dados
# Código usado para gerar as imagens de teste
def generate_example_images():
    ImageManager.create_filtered_image('all', '../pictures/baboon.png')
    ImageManager.create_filtered_image('all', '../pictures/poney.png')
    ImageManager.create_filtered_image('all', '../pictures/butterfly.png')
    ImageManager.create_filtered_image('all', '../pictures/city.png')
    ImageManager.create_filtered_image('all', '../pictures/house.png')
    ImageManager.create_filtered_image('all', '../pictures/seagull.png')


def main():
    if sys.argv[1] == 'example':
        generate_example_images()
    else:
        ImageManager.create_filtered_image(*(sys.argv[1::]))


if __name__ == '__main__':
    main()
