import os
from projeto1.image_filter import ImageFilter


# Gera todas as versões da imagem com cada filtro
def generate_filtered_images(file_path):

    # Descobre o nome do arquivo e a extensão
    filename = os.path.basename(file_path)
    filename_parts = os.path.splitext(filename)
    base = "".join(filename_parts[0:-1])
    extension = filename_parts[-1]

    c_filter_file = f"./results/{base}_c{extension}"
    d_filter_file = f"./results/{base}_d{extension}"

    # Gera as imagens com cada um dos filtros
    ImageFilter.filter_a(file_path, f"./results/{base}_a{extension}")
    ImageFilter.filter_b(file_path, f"./results/{base}_b{extension}")
    ImageFilter.filter_c(file_path, c_filter_file)
    ImageFilter.filter_d(file_path, d_filter_file)
    ImageFilter.filter_c_d(c_filter_file, d_filter_file, f"./results/{base}_c_d{extension}")


# Cria imagens filtradas a partir dos arquivos de imagens dados
def main():
    generate_filtered_images("../pictures/baboon.png")
    generate_filtered_images("../pictures/butterfly.png")
    generate_filtered_images("../pictures/city.png")
    generate_filtered_images("../pictures/house.png")
    generate_filtered_images("../pictures/seagull.png")


if __name__ == '__main__':
    main()
