from collections import deque
import json

import pymap3d
from airsim import Vector3r, GeoPoint
from settings import State

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


class Telemetry:
    def __init__(self):
        self.target_position: Vector3r = Vector3r(0.0, 0.0, -5.0)
        self.ned_position: Vector3r = Vector3r(0.0, 0.0, 0.0)
        self.gps_position: GeoPoint = GeoPoint()
        self.gps_home: GeoPoint = GeoPoint()
        self.continue_position: Vector3r = Vector3r(0.0, 0.0, 0.0)

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
