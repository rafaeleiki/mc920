import cv2
from dithering import Dithering


def main():
    print("hello")
    image = cv2.imread('../pictures/house.png', 0)
    cv2.imshow('reto', Dithering.floyd_steinberg(image, False))
    cv2.imshow('alternado', Dithering.floyd_steinberg(image))
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
