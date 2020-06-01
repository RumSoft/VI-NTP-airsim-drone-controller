import cv2
import numpy as np

from settings import COLLISION_BUFFER


class Collision:
    def __init__(self, raw_image):
        self.collision = False

        self.image = self._process_raw_image(raw_image)
        self._prepare_image()

        self._detect_collision()
        self._show_image()

    def _detect_collision(self):
        print(self.maxes)
        print(self.collision)
        if self.current < COLLISION_BUFFER:
            self.collision = True
        else:
            self.collision = False

    @staticmethod
    def _process_raw_image(raw_image):
        image = np.array(raw_image.image_data_float, dtype=np.float)
        image = image.clip(0, 255)
        image = image.reshape(raw_image.height, raw_image.width)

        processed_image = np.array(image, dtype=np.uint8)
        return processed_image

    def _prepare_image(self):
        self.top, self.bottom = np.vsplit(self.image, 2)

        self.bands = np.hsplit(self.top, [50, 100, 150, 200])
        self.maxes = [np.max(x) for x in self.bands]
        self.current = self.maxes[3]

    def _show_image(self):
        cv2.imshow("Top", self.image)
        cv2.waitKey(1)
