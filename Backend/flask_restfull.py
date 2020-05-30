import sys
import signal

from flask import Flask, jsonify
from flask_restful import Api, Resource, request
from flask_cors import CORS

from Backend.drone import Drone
from Backend.telemetry import Telemetry
from Backend.settings import State


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
        return 'not_implemented_yet'


class Wait(Resource):
    def post(self):
        drone.wait()
        return 'wait called'


class Continue(Resource):
    def post(self):
        drone.continue_flight()
        return 'continue called'


class Position(Resource):
    def get(self):
        return jsonify(telemetry.gps_position.__dict__)


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
    api.add_resource(Position, '/position')

    CORS(app)
    app.run(debug=True)

