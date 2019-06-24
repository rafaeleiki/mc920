import cv2
from sklearn.cluster import MiniBatchKMeans


class ColorQuantizationImage:

    def __init__(self, image_path):
        self.image = cv2.imread(image_path)

    def create_quantized(self, output_path, colors_count):
        """
        Cria uma versão nova da imagem com um limite de cores
        :param output_path: caminho do arquivo a ser criado
        :param colors_count: quantidade de cores
        """

        # Prepara para uso no K-means
        (height, width) = self.image.shape[:2]
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
        image = image.reshape((image.shape[0] * image.shape[1], 3))

        # Realiza quantização
        clusters = MiniBatchKMeans(n_clusters=colors_count)
        labels = clusters.fit_predict(image)
        quantization = clusters.cluster_centers_.astype("uint8")[labels]

        # Volta para o espaço RGB
        quantized_image = quantization.reshape((height, width, 3))
        quantized_image = cv2.cvtColor(quantized_image, cv2.COLOR_LAB2BGR)

        # Escreve o arquivo
        cv2.imwrite(output_path, quantized_image)
        print("File \"%s\" created with %d colors" % (output_path, colors_count))
