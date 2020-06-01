from typing import Optional

from airsim import Vector3r, GeoPoint

from route import Route
from collision import Collision
from settings import State, COLLISION_BUFFER


class Telemetry:
    def __init__(self):
        self.target_position: Vector3r = Vector3r(0.0, 0.0, -10.0)
        self.ned_position: Vector3r = Vector3r(0.0, 0.0, 0.0)
        self.gps_position: GeoPoint = GeoPoint()
        self.gps_home: GeoPoint = GeoPoint()
        self.continue_position: Vector3r = Vector3r(0.0, 0.0, 0.0)
        self.linear_velocity: Vector3r = Vector3r(0.0, 0.0, 0.0)
        self.collision: Optional[Collision] = None
        self.landed_state: int = 0

        self.state: str = State.IDLE
        self.waiting = False
        self.route: Route = Route()
