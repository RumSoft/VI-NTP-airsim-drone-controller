import math
import time
from threading import Thread
from typing import Optional
from airsim import MultirotorClient, Vector3r

import settings
from telemetry import Telemetry


class Drone(Thread):
    def __init__(self, telemetry: Telemetry):
        super(Drone, self).__init__()
        self.daemon = True

        self.telemetry = telemetry
        self.client: Optional[MultirotorClient] = None
        self._connect()

        self._exit = False

    def run(self):
        while not self._exit:
            try:
                self._process()
            except BufferError:
                pass

    def shutdown(self):
        self._exit = True
        self.client.enableApiControl(False)
        self.client.reset()

    def _process(self):
        self._update_telemetry()
        self._check_progress()
        time.sleep(0.1)

    def _connect(self):
        self.client = MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)

    def start_flight(self):
        self.telemetry.waiting = False
        self.telemetry.state = settings.State.FLYING
        self._send_position()

    def set_target_position(self, x: float, y: float, z: float):
        self.telemetry.target_position = Vector3r(x, y, z)

    def _update_telemetry(self):
        multirotor_state = self.client.getMultirotorState()
        self.telemetry.landed_state = multirotor_state.landed_state
        self.telemetry.ned_position = multirotor_state.kinematics_estimated.position
        self.telemetry.linear_velocity = multirotor_state.kinematics_estimated.linear_velocity
        self.telemetry.gps_position = self.client.getGpsData().gnss.geo_point
        self.telemetry.gps_home = self.client.getHomeGeoPoint()

    def _check_progress(self):
        actual_position = self.telemetry.ned_position
        target_position = self.telemetry.target_position
        if actual_position.distance_to(target_position) < settings.TARGET_BUFFER:
            self._update_target_point()

    def _update_target_point(self):
        route = self.telemetry.route.route
        if len(route) != 0 and not self.telemetry.waiting:
            target = route.popleft()
            self.telemetry.target_position = target
            self.set_yaw()
            self._send_position()

        elif self._is_drone_stopped():
            self.telemetry.state = settings.State.IDLE

    def _is_drone_stopped(self):
        velocity = self.telemetry.linear_velocity.dot(Vector3r(1, 1, 1))

        condition = (len(self.telemetry.route.route) == 0
                     and abs(velocity) < settings.VELOCITY_BUFFER
                     and self.telemetry.landed_state == 1)

        return condition

    def takeoff(self, height: float = 10, velocity: float = 5):
        self.client.armDisarm(True)
        self.client.moveToZAsync(height, velocity)

    def _send_position(self, velocity: float = settings.GROUNDSPEED):
        position: Vector3r = self.telemetry.target_position
        self.client.moveToPositionAsync(
            position.x_val, position.y_val, position.z_val, velocity
        )

    def goto(self, x, y, z, velocity: float = settings.GROUNDSPEED):
        self.client.moveToPositionAsync(
            x, y, z, velocity
        )

    def land(self):
        self.client.landAsync()

    def wait(self):
        self.telemetry.waiting = True
        self.telemetry.route.route.appendleft(self.telemetry.target_position)
        position = self.telemetry.ned_position
        self.set_target_position(
            position.x_val, position.y_val, position.z_val)
        self._send_position()

    def continue_flight(self):
        self.telemetry.waiting = False

    def stop(self):
        self.telemetry.clear_route()

        position = self.telemetry.ned_position
        self.set_target_position(
            position.x_val, position.y_val, position.z_val)
        self._send_position()

        self.telemetry.state = settings.State.IDLE
        self.telemetry.waiting = False

    def set_yaw(self):
        actual_position = self.telemetry.ned_position
        target_position = self.telemetry.target_position
        yaw = math.atan2(target_position.y_val - actual_position.y_val,
                         target_position.x_val - actual_position.x_val)

        self.client.rotateToYawAsync(
            math.degrees(yaw), settings.SET_YAW_TIMEOUT, 1
        ).join()
