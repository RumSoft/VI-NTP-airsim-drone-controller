from collections import deque

import pymap3d
from airsim import Vector3r, GeoPoint


class Route:
    def __init__(self):
        self.route = deque()
        self.gps_route = []

    def _parse_json_route(self, json_route: dict):
        point_list = json_route['route']
        self.gps_route = [Vector3r(point[0], point[1], point[2]) for point in point_list]

    def _prepare_ned_route(self, home_gps):
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

    def prepare_route(self, json_route: dict, gps_home: GeoPoint):
        home_gps = Vector3r(gps_home.latitude,
                            gps_home.longitude,
                            0.0)
        self._parse_json_route(json_route)
        self._prepare_ned_route(home_gps)

    def clear_route(self):
        self.route = deque()

