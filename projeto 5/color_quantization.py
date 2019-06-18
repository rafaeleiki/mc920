import cv2
from sklearn.cluster import KMeans


class ColorQuantizationImage:

    def __init__(self, image_path):
        self.image = cv2.imread(image_path)

    def color_quantization(self, colors_count):
        (height, width) = self.image.shape[:2]
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)

        # Prepara para uso no K-means
        image = image.reshape((image.shape[0] * image.shape[1], 3))

        clusters = KMeans(n_clusters=colors_count)
        labels = clusters.fit_predict(image)
        quantization = clusters.cluster_centers_.astype("uint8")[labels]

        quantized_image = quantization.reshape((height, width, 3))
        quantized_image = cv2.cvtColor(quantized_image, cv2.COLOR_LAB2BGR)

        cv2.imwrite('./results/result.png', quantized_image)
