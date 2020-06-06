import sys
import signal

import pymap3d
from flask import Flask, jsonify
from flask_restful import Api, Resource, request
from flask_cors import CORS

from drone import Drone
from telemetry import Telemetry
from settings import State


def exit_handler(signal, frame):
    drone.shutdown()
    print('SHUTTING DOWN')
    sys.exit(0)


class Start(Resource):
    def post(self):
        if telemetry.state == State.IDLE:
            json_data = request.get_json(force=True)
            telemetry.route.prepare_route(json_data, telemetry.gps_home)
            drone.start_flight()
            return 'drone started'
        else:
            error_log = f'Command rejected! Drone is in {telemetry.state} state!'
            return error_log, 400


class Stop(Resource):
    def post(self):
        drone.stop()
        return 'stop called'


class Wait(Resource):
    def post(self):
        drone.wait()
        return 'wait called'


class Continue(Resource):
    def post(self):
        drone.continue_flight()
        return 'continue called'


class DroneState(Resource):
    def get(self):
        gps_position = telemetry.gps_position.__dict__
        gps_position['altitude'] = - telemetry.ned_position.z_val
        target = telemetry.target_position
        lat, lon, alt = pymap3d.ned2geodetic(
            target.x_val, target.y_val, target.z_val,
            telemetry.gps_home.latitude, telemetry.gps_home.longitude, 0
        )
        gps_target = {
            'latitude': lat, 'longitude': lon, 'altitude': alt
        }
        data = {
            'gps_position': gps_position,
            'target_position': gps_target,
            'state': telemetry.state,
            'waiting': telemetry.waiting,
            'collision': drone._collision_mode,
        }
        return jsonify(data)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_handler)

    telemetry = Telemetry()
    drone = Drone(telemetry)
    drone.start()

    app = Flask(__name__)

    api = Api(app)
    api.add_resource(Wait, '/wait')
    api.add_resource(Continue, '/continue')
    api.add_resource(Start, '/start')
    api.add_resource(Stop, '/stop')
    api.add_resource(DroneState, '/drone-state')

    CORS(app)
    app.run(debug=False)

