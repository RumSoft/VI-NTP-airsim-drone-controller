import math
import time
from threading import Thread
from typing import Optional
from unittest.mock import MagicMock

import airsim
from airsim import MultirotorClient, Vector3r, Quaternionr

import settings
from telemetry import Telemetry
from collision import Collision


class CollisionType:
    WALL = 'wall'
    TERRAIN = 'terrain'
    BOTH = 'both'
    NONE = 'none'


class Drone(Thread):
    def __init__(self, telemetry: Telemetry):
        super(Drone, self).__init__()
        self.daemon = True

        self.telemetry = telemetry
        self.client: Optional[MultirotorClient] = None
        self._connect()

        self._collision_mode = False
        self._collision_type = CollisionType.NONE
        self._exit = False

    def run(self):
        while not self._exit:
            try:
                self._process()
            except BufferError:
                pass

    def _process(self):
        self._update_telemetry()

        if self.is_collision():
            self._process_collision()
        elif self._collision_mode:
            self.stop_collision()
        else:
            self._check_progress()

        time.sleep(0.1)

    def is_collision(self):
        collision = (self.telemetry.wall_collision.wall_collision
                     or self.telemetry.terrain_collision.terrain_collision)
        return collision

    def _process_collision(self):
        wall_collision = self.telemetry.wall_collision.wall_collision
        terrain_collision = self.telemetry.terrain_collision.terrain_collision

        if wall_collision:
            if terrain_collision:
                self.wall_collision()
                self._collision_type = CollisionType.BOTH
            else:
                self.wall_collision()
                self._collision_type = CollisionType.WALL
        else:
            if terrain_collision:
                self.terain_collision()
                self._collision_type = CollisionType.TERRAIN
            else:
                self._collision_type = CollisionType.NONE

    def wait(self):
        self.telemetry.waiting = True
        self._pause_route()
        self._send_position()

    def continue_flight(self):
        self.telemetry.waiting = False

    def stop(self):
        self.telemetry.route.clear_route()

        position = self.telemetry.ned_position
        self.set_target_position(position.x_val, position.y_val, position.z_val)
        self._send_position()

        self.telemetry.state = settings.State.IDLE

    def set_yaw(self):
        actual_position = self.telemetry.ned_position
        target_position = self.telemetry.target_position
        yaw = math.atan2(target_position.y_val - actual_position.y_val,
                         target_position.x_val - actual_position.x_val)

        self.client.rotateToYawAsync(
            math.degrees(yaw), settings.SET_YAW_TIMEOUT, 1
        ).join()

    def start_flight(self):
        self.telemetry.waiting = False
        self.telemetry.state = settings.State.FLYING
        self._send_position()

    def set_target_position(self, x: float, y: float, z: float):
        self.telemetry.target_position = Vector3r(x, y, z)

    def _connect(self):
        self.client = MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)

    def _update_telemetry(self):
        multirotor_state = self.client.getMultirotorState()

        self.telemetry.landed_state = multirotor_state.landed_state
        self.telemetry.ned_position = multirotor_state.kinematics_estimated.position
        self.telemetry.linear_velocity = multirotor_state.kinematics_estimated.linear_velocity

        self.telemetry.gps_position = self.client.getGpsData().gnss.geo_point
        self.telemetry.gps_home = self.client.getHomeGeoPoint()
        self._get_camera_data()

    def _get_camera_data(self):
        self.client.simSetCameraOrientation(0, Quaternionr(0.0, 0.0, 0.0, 1.0))
        wall_camera_data = self.client.simGetImages(
            [airsim.ImageRequest("0", airsim.ImageType.DepthPlanner, pixels_as_float=True)]
        )
        self.client.simSetCameraOrientation(0, Quaternionr(0.0, -0.7, 0.0, 0.5))
        terrain_camera_data = self.client.simGetImages(
            [airsim.ImageRequest("0", airsim.ImageType.DepthPlanner, pixels_as_float=True)]
        )

        self.telemetry.wall_collision.process_wall_image(wall_camera_data[0])
        self.telemetry.terrain_collision.process_terrain_image(terrain_camera_data[0])

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

    def _send_position(self, velocity: float = settings.GROUNDSPEED):
        position: Vector3r = self.telemetry.target_position
        self.client.moveToPositionAsync(
            position.x_val, position.y_val, position.z_val, velocity
        )

    def _pause_route(self):
        self.telemetry.route.route.appendleft(self.telemetry.target_position)
        position = self.telemetry.ned_position
        self.set_target_position(position.x_val, position.y_val, position.z_val)

    def wall_collision(self):
        if (self._collision_type != CollisionType.WALL
                and self._collision_type != CollisionType.BOTH):
            print('WALL COLLISION STARTED')
            self._collision_mode = True
            self.client.moveToZAsync(-100, settings.COLLISION_SPEED)
            print(f'Target: {-100}')

    def terain_collision(self):
        if self._collision_type != CollisionType.TERRAIN:
            print('BOTTOM STARTED')
            if self.telemetry.ned_position.z_val < -8:
                self._collision_mode = True
                target = self.telemetry.target_position
                actual = self.telemetry.ned_position
                print(f'Target: {target.x_val} {target.y_val} {actual.z_val - 50}')
                self.client.moveToPositionAsync(
                    target.x_val, target.y_val, actual.z_val - 1, settings.COLLISION_SPEED)

    def stop_collision(self):
        print('COLLISION STOPPED')
        self._send_position()
        self._collision_mode = False

    def shutdown(self):
        self._exit = True
        self.client.enableApiControl(False)
        self.client.reset()
