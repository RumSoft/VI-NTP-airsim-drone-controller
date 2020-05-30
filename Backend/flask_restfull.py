import sys
import signal

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
            telemetry.prepare_route(json_data)
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
        data = {
            'gps_position': telemetry.gps_position.__dict__,
            # 'ned_position': telemetry.ned_position.__dict__,
            # 'gps_home_position': telemetry.gps_home.__dict__,
            # 'ned_target_position': telemetry.target_position.__dict__,
            'state': telemetry.state,
            'waiting': telemetry.waiting,
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
    app.run(debug=True)

