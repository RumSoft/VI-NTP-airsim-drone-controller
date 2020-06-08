from typing import Optional

import pymap3d
from airsim import Vector3r, GeoPoint

from route import Route
from collision import WallCollision, TerrainCollision
from settings import State, COLLISION_BUFFER


class Telemetry:
    def __init__(self):
        self.target_position: Vector3r = Vector3r(0.0, 0.0, -10.0)
        self.ned_position: Vector3r = Vector3r(0.0, 0.0, 0.0)
        self.gps_position: GeoPoint = GeoPoint()
        self.gps_home: GeoPoint = GeoPoint()
        self.linear_velocity: Vector3r = Vector3r(0.0, 0.0, 0.0)

        self.wall_collision: Optional[WallCollision] = WallCollision()
        self.terrain_collision: Optional[TerrainCollision] = TerrainCollision()
        self.collision_mode: bool = False

        self.landed_state: int = 0

        self.state: str = State.IDLE
        self.waiting: bool = False
        self.route: Route = Route()

    def prepare_drone_state_data(self):
        gps_position = self.gps_position.__dict__
        gps_position['altitude'] = - self.ned_position.z_val

        gps_target = self.prepare_gps_target()

        drone_state_data = {
            'gps_position': gps_position,
            'target_position': gps_target,
            'state': self.state,
            'waiting': self.waiting,
            'collision': self.collision_mode,
        }
        return drone_state_data

    def prepare_gps_target(self) -> dict:
        target = self.target_position
        lat, lon, alt = pymap3d.ned2geodetic(
            target.x_val, target.y_val, target.z_val,
            self.gps_home.latitude, self.gps_home.longitude, 0
        )
        gps_target = {
            'latitude': lat, 'longitude': lon, 'altitude': alt
        }
        return gps_target
