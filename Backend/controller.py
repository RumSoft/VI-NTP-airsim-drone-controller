import math

from airsim import MultirotorClient, Vector3r

import settings
from telemetry import Telemetry


class Controller:
    def __init__(self, client: MultirotorClient,
                 telemetry: Telemetry):
        self.client = client
        self.telemetry = telemetry

    def start_flight(self):
        self.telemetry.waiting = False
        self.telemetry.state = settings.State.FLYING
        self.send_position()

    def stop(self):
        self.telemetry.route.clear_route()

        position = self.telemetry.ned_position
        self.set_target_position(position.x_val, position.y_val, position.z_val)
        self.send_position()

        self.telemetry.state = settings.State.IDLE

    def wait(self):
        self.telemetry.waiting = True
        self.pause_route()
        self.send_position()

    def continue_flight(self):
        self.telemetry.waiting = False

    def set_target_position(self, x: float, y: float, z: float):
        self.telemetry.target_position = Vector3r(x, y, z)

    def check_progress(self):
        actual_position = self.telemetry.ned_position
        target_position = self.telemetry.target_position
        if actual_position.distance_to(target_position) < settings.TARGET_BUFFER:
            self.update_target_point()

    def update_target_point(self):
        route = self.telemetry.route.route
        if len(route) != 0 and not self.telemetry.waiting:
            target = route.popleft()
            self.telemetry.target_position = target
            self.set_yaw()
            self.send_position()

        elif self.is_drone_stopped():
            self.telemetry.state = settings.State.IDLE

    def is_drone_stopped(self):
        velocity = self.telemetry.linear_velocity.dot(Vector3r(1, 1, 1))

        condition = (len(self.telemetry.route.route) == 0
                     and abs(velocity) < settings.VELOCITY_BUFFER
                     and self.telemetry.landed_state == 1)

        return condition

    def send_position(self, velocity: float = settings.GROUNDSPEED):
        position: Vector3r = self.telemetry.target_position
        self.client.moveToPositionAsync(
            position.x_val, position.y_val, position.z_val, velocity
        )

    def pause_route(self):
        self.telemetry.route.route.appendleft(self.telemetry.target_position)
        position = self.telemetry.ned_position
        self.set_target_position(position.x_val, position.y_val, position.z_val)

    def set_yaw(self):
        actual_position = self.telemetry.ned_position
        target_position = self.telemetry.target_position
        yaw = math.atan2(target_position.y_val - actual_position.y_val,
                         target_position.x_val - actual_position.x_val)

        self.client.rotateToYawAsync(
            math.degrees(yaw), settings.SET_YAW_TIMEOUT, 1
        ).join()
