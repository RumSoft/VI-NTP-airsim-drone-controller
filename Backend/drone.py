import time
from threading import Thread
from typing import Optional

import airsim
from airsim import MultirotorClient, Quaternionr

from controller import Controller
from collision import CollisionType
import settings
from telemetry import Telemetry


class Drone(Thread):
    def __init__(self, telemetry: Telemetry):
        super(Drone, self).__init__()
        self.daemon = True
        self._exit = False

        self.telemetry = telemetry
        self.client: Optional[MultirotorClient] = None
        self.connect()

        self.controller = Controller(self.client, self.telemetry)
        self.collision_type = CollisionType.NONE

    def run(self):
        while not self._exit:
            try:
                self._process()
            except BufferError:
                pass
            except KeyboardInterrupt:
                self.shutdown()

    def _process(self):
        self.update_telemetry()

        if self.is_collision():
            self.process_collision()
        elif self.telemetry.collision_mode:
            self.stop_collision()
        else:
            self.controller.check_progress()

        time.sleep(0.1)

    def shutdown(self):
        self._exit = True
        self.client.enableApiControl(False)
        self.client.reset()

    def connect(self):
        self.client = MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.client.getBarometerData()

    # region TELEMETRY

    def update_telemetry(self):
        multirotor_state = self.client.getMultirotorState()

        self.telemetry.landed_state = multirotor_state.landed_state
        self.telemetry.ned_position = multirotor_state.kinematics_estimated.position
        self.telemetry.linear_velocity = multirotor_state.kinematics_estimated.linear_velocity

        self.telemetry.gps_position = self.client.getGpsData().gnss.geo_point
        self.telemetry.gps_home = self.client.getHomeGeoPoint()

        self.telemetry.quaternion = self.client.simGetVehiclePose().orientation

        self.get_front_camera_image()
        self.get_bottom_camera_image()

    def get_bottom_camera_image(self):
        self.client.simSetCameraOrientation('0', Quaternionr(0.0, -0.7, 0.0, 0.5))
        bottom_camera_data = self.client.simGetImages(
            [airsim.ImageRequest("0", airsim.ImageType.DepthPlanner, pixels_as_float=True)]
        )
        self.telemetry.terrain_collision.process_image(bottom_camera_data[0])

    def get_front_camera_image(self):
        self.client.simSetCameraOrientation('0', Quaternionr(0.0, 0.0, 0.0, 1.0))
        front_camera_data = self.client.simGetImages(
            [airsim.ImageRequest("0", airsim.ImageType.DepthPlanner, pixels_as_float=True)]
        )
        self.telemetry.wall_collision.process_image(front_camera_data[0])

    # endregion

    # region COLLISION

    def is_collision(self):
        collision = (self.telemetry.wall_collision.collision
                     or self.telemetry.terrain_collision.collision)
        return collision

    def process_collision(self):
        wall_collision = self.telemetry.wall_collision.collision
        terrain_collision = self.telemetry.terrain_collision.collision

        if wall_collision:
            if terrain_collision:
                self.wall_collision()
                self.collision_type = CollisionType.BOTH
            else:
                self.wall_collision()
                self.collision_type = CollisionType.WALL
        else:
            if terrain_collision:
                self.terrain_collision()
                self.collision_type = CollisionType.TERRAIN
            else:
                self.collision_type = CollisionType.NONE

    def wall_collision(self):
        if (self.collision_type != CollisionType.WALL
                and self.collision_type != CollisionType.BOTH):
            self.telemetry.collision_mode = True
            self.client.moveToZAsync(-500, settings.COLLISION_SPEED)

    def terrain_collision(self):
        if self.collision_type != CollisionType.TERRAIN:
            if self.telemetry.ned_position.z_val < -8:
                self.telemetry.collision_mode = True
                target = self.telemetry.target_position
                actual = self.telemetry.ned_position
                self.client.moveToPositionAsync(
                    target.x_val, target.y_val, actual.z_val - 1, settings.COLLISION_SPEED)

    def stop_collision(self):
        self.controller.send_position()
        self.telemetry.collision_mode = False

    # endregion
