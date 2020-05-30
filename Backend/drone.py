import time
from threading import Thread
from typing import Optional
from airsim import MultirotorClient, Vector3r


from Backend import settings
from Backend.telemetry import Telemetry


class Drone(Thread):
    def __init__(self, telemetry: Telemetry):
        super(Drone, self).__init__()
        self.daemon = True

        self.telemetry = telemetry
        self._exit = False
        self.client: Optional[MultirotorClient] = None

    def run(self):
        while not self._exit:
            self._process()

    def _process(self):
        self._send_position()
        self._update_telemetry()
        self._check_progress()

    def connect(self):
        self.client = MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)

    def set_target_position(self, x: float, y: float, z: float):
        self.telemetry.target_position = Vector3r(x, y, z)

    def _update_telemetry(self):
        self.telemetry.ned_position = \
            self.client.getMultirotorState().kinematics_estimated.position
        self.telemetry.gps_position = self.client.getGpsData().gnss.geo_point

    def _check_progress(self):
        actual_position = self.telemetry.ned_position
        target_position = self.telemetry.target_position
        if actual_position.distance_to(target_position) < settings.TARGET_BUFFER:
            self._update_target_point()

    def _update_target_point(self):
        route = self.telemetry.route.route
        if len(route) != 0:
            self.telemetry.target_position = route.popleft()

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
        self.telemetry.continue_position = self.telemetry.target_position
        position = self.telemetry.ned_position
        self.set_target_position(position.x_val, position.y_val, position.z_val)

    def continue_flight(self):
        self.telemetry.target_position = self.telemetry.continue_position
