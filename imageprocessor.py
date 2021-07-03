import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from collections import Counter


def rgb_to_hex(rgb):
    hexcode = '#' + '%02x%02x%02x' % rgb
    return hexcode.upper()


class ImageProcessor():
    def __init__(self, filename):
        self.image = np.array(Image.open(filename))
        self.rgb_list = self.get_rgb_list()
        self.hex_list = self.get_hex_list()

    def print_image_stats(self):
        print(f"The image is a {self.image.ndim} dimensional array")
        print(f"It's shape is {self.image.shape}")


    def print_image(self):
        plt.imshow(self.image)
        plt.show()

    def get_rgb_list(self):
        image_rgb_list_raw=[]
        for rgb_row in self.image:
            for rgb_element in rgb_row:
                image_rgb_list_raw.append(tuple(rgb_element.tolist()))
        counts = Counter(image_rgb_list_raw)
        image_rgb_list_sorted = list(set(sorted(image_rgb_list_raw, key=counts.get, reverse=True)))
        return image_rgb_list_sorted[:10]

    def get_hex_list(self):
        return [rgb_to_hex(rgbcode) for rgbcode in self.rgb_list]





