from collections import deque
import numpy as np
import cv2
from typing import Optional

from airsim import Vector3r, GeoPoint

from route import Route
from settings import State, COLLISION_BUFFER


class DepthCamera:
    def __init__(self, raw_image):
        self.collision = False

        self.image = self._process_raw_image(raw_image)
        self._prepare_image()

        cv2.imshow("Top", self.image)
        cv2.waitKey(1)

    def _detect_collision(self):
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


class Telemetry:
    def __init__(self):
        self.target_position: Vector3r = Vector3r(0.0, 0.0, -10.0)
        self.ned_position: Vector3r = Vector3r(0.0, 0.0, 0.0)
        self.gps_position: GeoPoint = GeoPoint()
        self.gps_home: GeoPoint = GeoPoint()
        self.continue_position: Vector3r = Vector3r(0.0, 0.0, 0.0)
        self.linear_velocity: Vector3r = Vector3r(0.0, 0.0, 0.0)
        self.depth_camera: Optional[DepthCamera] = None
        self.landed_state: int = 0

        self.state: str = State.IDLE
        self.waiting = False
        self.route: Route = Route()
