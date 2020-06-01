import math
from collections import deque
import json
import numpy as np
import cv2
from typing import Optional

import pymap3d
from airsim import Vector3r, GeoPoint
from settings import State, COLLISION_BUFFER

route = {
    'route': [
        [0.0, 0.0, 10.0],
        [10.0, 0.0, 10.0],
        [60.0, 25.0, 40.0],
        [80.0, -5.0, 40.0],
        [-95.0, -20.0, 40.0],
        [-50.0, -5.0, 25.0],
        [0.0, 0.0, 10.0],
    ]
}
route_fixture = json.dumps(route)


class Route:
    def __init__(self):
        self.route = deque()
        self.gps_route = []

    def parse_route(self, json_route: dict):
        point_list = json_route['route']
        self.gps_route = [Vector3r(point[0], point[1], point[2]) for point in point_list]

    def prepare_route(self, home_gps):
        for point in self.gps_route:
            route_ned_point = self.from_gps_to_ned(
                Vector3r(point.x_val, point.y_val, -point.z_val),
                Vector3r(home_gps.x_val, home_gps.y_val, home_gps.z_val)
            )
            self.route.append(route_ned_point)

    @staticmethod
    def from_gps_to_ned(target_position: Vector3r, home_gps: Vector3r):
        n, e, d = pymap3d.geodetic2ned(
            target_position.x_val, target_position.y_val, target_position.z_val,
            home_gps.x_val, home_gps.y_val, home_gps.z_val
        )
        return Vector3r(n, e, -d)


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

    def prepare_route(self, json_route: dict):
        home_gps = Vector3r(self.gps_home.latitude,
                            self.gps_home.longitude,
                            0.0)
        self.route.parse_route(json_route)
        self.route.prepare_route(home_gps)

    def clear_route(self):
        self.route.route = deque()
