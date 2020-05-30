from flask import Flask, jsonify
from flask_restful import reqparse, Api, Resource, request
from flask_cors import CORS

from Backend.drone import Drone
from Backend.telemetry import Telemetry

parser = reqparse.RequestParser()
parser.add_argument('route')


class Connect(Resource):
    def post(self):
        drone.connect()
        return 'connected or tried XD'


class Start(Resource):
    def post(self):
        drone.start()
        return 'start'


class Stop(Resource):
    def post(self):
        return 'not_implemented_yet'


class Route(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        telemetry.route.parse_route(json_data)
        telemetry.route.prepare_route()
        print(telemetry.route.route)
        return 'takeoff called'


class Position(Resource):
    def get(self):
        return jsonify(telemetry.gps_position.__dict__)


if __name__ == '__main__':
    telemetry = Telemetry()
    drone = Drone(telemetry)

    app = Flask(__name__)

    api = Api(app)
    api.add_resource(Connect, '/connect')
    api.add_resource(Start, '/start')
    api.add_resource(Stop, '/stop')
    api.add_resource(Route, '/route')
    api.add_resource(Position, '/position')

    CORS(app)
    app.run(debug=True)
