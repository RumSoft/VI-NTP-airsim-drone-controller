import numpy as np
from abc import ABC
from typing import Optional
from settings import COLLISION_BUFFER


class CollisionType:
    WALL = 'wall'
    TERRAIN = 'terrain'
    BOTH = 'both'
    NONE = 'none'


class AbstractCollision(ABC):
    def __init__(self):
        self.collision: bool = False
        self.image: Optional[np.ndarray] = None

        self.top_distance: int = 255
        self.bottom_distance: int = 255

    def process_image(self, raw_image):
        self.image = self._process_raw_image(raw_image)

        self._prepare_top_collision()
        self._prepare_bottom_collision()

        self._detect_collision()

    @staticmethod
    def _process_raw_image(raw_image):
        image = np.array(raw_image.image_data_float, dtype=np.float)
        image = image.clip(0, 255)
        image = image.reshape(raw_image.height, raw_image.width)

        processed_image = np.array(image, dtype=np.uint8)
        return processed_image

    def _prepare_bottom_collision(self):
        bottom = np.vsplit(self.image, 4)[3]

        bands_bottom = np.hsplit(bottom, [50, 100, 150, 200])
        maxes_bottom = [np.max(x) for x in bands_bottom]
        self.bottom_distance = maxes_bottom[2]

    def _prepare_top_collision(self):
        top = np.vsplit(self.image, 2)[0]

        bands_top = np.hsplit(top, [50, 100, 150, 200])
        maxes_top = [np.max(x) for x in bands_top]
        self.top_distance = np.min(maxes_top[1:3])

    def _detect_collision(self):
        raise NotImplementedError('Not implemented!')


class WallCollision(AbstractCollision):
    def __init__(self):
        super(WallCollision, self).__init__()

    def _detect_collision(self):
        if self.top_distance == 255 and self.bottom_distance > 20:
            self.collision = False
        if self.top_distance < COLLISION_BUFFER:
            self.collision = True


class TerrainCollision(AbstractCollision):
    def __init__(self):
        super(TerrainCollision, self).__init__()

    def _detect_collision(self):
        if self.bottom_distance < 2:
            self.collision = True
        if self.bottom_distance > 5:
            self.collision = False
