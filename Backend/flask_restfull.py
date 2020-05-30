from flask import Flask, jsonify
from flask_restful import reqparse, Api, Resource, request
from flask_cors import CORS

from Backend.drone import Drone
from Backend.telemetry import Telemetry

parser = reqparse.RequestParser()
parser.add_argument('route')


class Start(Resource):
    def post(self):
        json_data = request.get_json(force=True)

        telemetry.prepare_route(json_data)
        drone.start_flight = True
        return 'drone started'


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
