import cv2
import numpy as np
import math
from fuzzy import Fuzzy

from settings import COLLISION_BUFFER


class Collision:
    def __init__(self):
        self.wall_collision = False
        self.terrain_collision = False

        self.image = None
        self.wall_image = None
        self.terrain_image = None
        self.fuzzy = Fuzzy()

    def process_wall_image(self, raw_image):
        self.image = self._process_raw_image(raw_image)
        self._prepare_image()

        self._detect_wall_collision()
        # self._show_image()
        self.wall_image = self.image

        bands_wall = np.hsplit(self.image, 3)
        maxes_wall = [np.average(x)/255 for x in bands_wall]
        self.movement = self.fuzzy.calculate(maxes_wall[0], maxes_wall[1], maxes_wall[2])
        print(self.movement)
        self._show_image()

    def process_terrain_image(self, raw_image):
        self.image = self._process_raw_image(raw_image)
        self._prepare_image()

        self._detect_terrain_collision()
        self.terrain_image = self.image
        # self._show_image()

    def _detect_wall_collision(self):
        if self.current_top == 255 and self.current_bottom > 20:
            self.wall_collision = False
        if self.current_top < COLLISION_BUFFER:
            self.wall_collision = True

    def _detect_terrain_collision(self):
        if self.current_bottom < 2:
            self.terrain_collision = True
        if self.current_bottom > 5:
            self.terrain_collision = False

    @staticmethod
    def _process_raw_image(raw_image):

        image = np.array(raw_image.image_data_float, dtype=np.float)
        image = image.clip(0, 255)
        image = image.reshape(raw_image.height, raw_image.width)
        image = np.delete(image, 1, 1)

        kernel = np.ones((5, 5))/25
        image = cv2.filter2D(image, -1, kernel) * 5
        image[image >= 80] = 255
        image[(image >= 50) & (image < 80)] = 125

        image = cv2.erode(image, kernel, iterations=2)
        image = image.clip(0, 255)

        processed_image = np.array(image, dtype=np.uint8)
        return processed_image

    def _prepare_image(self):
        self.top = np.vsplit(self.image, 2)[0]
        self.bottom = np.vsplit(self.image, 4)[3]

        self.bands_top = np.hsplit(self.top, [50, 100, 150, 200])
        self.maxes_top = [np.max(x) for x in self.bands_top]
        self.current_top = np.min(self.maxes_top[1:3])

        self.bands_bottom = np.hsplit(self.bottom, [50, 100, 150, 200])
        self.maxes_bottom = [np.max(x) for x in self.bands_bottom]
        self.current_bottom = self.maxes_bottom[2]

    def _show_image(self):
        cv2.imshow("Top", self.wall_image)
        cv2.waitKey(1)
