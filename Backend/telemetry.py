from netrc import netrc
from typing import Optional
from collections import deque
import json

import pymap3d
from airsim import Vector3r

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

    def prepare_route(self):
        self.route = deque(
            [
                self.from_gps_to_ned(Vector3r(point.x_val, point.y_val, -point.z_val),
                                     self.gps_route[0])
                for point in self.gps_route
            ]
        )
        self.route.append(Vector3r(0.0, 0.0, 0.0))

    @staticmethod
    def from_gps_to_ned(ned_position: Vector3r, home_gps: Vector3r):
        n, e, d = pymap3d.geodetic2ned(
            ned_position.x_val, ned_position.y_val, ned_position.z_val,
            home_gps.x_val, home_gps.y_val, home_gps.z_val
        )
        return Vector3r(n, e, -d)


class Telemetry:
    def __init__(self):
        self.target_position: Vector3r = Vector3r(0.0, 0.0, -10.0)
        self.ned_position: Vector3r = Vector3r(0.0, 0.0, 0.0)
        self.gps_position: Vector3r = Vector3r(0.0, 0.0, 0.0)
        self.continue_position: Vector3r = Vector3r(0.0, 0.0, 0.0)
        self.route: Route = Route()
