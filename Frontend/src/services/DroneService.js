import APIService from "./APIService";

export default class {
  static getState() {
    return APIService.get("/drone-state").then((x) => {
      console.log("pos", x.data.gps_position);
      return {
        latitude: x.data.gps_position.latitude || 47.64,
        longitude: x.data.gps_position.longitude || -122.14,
        altitude: x.data.gps_position.altitude || 0,
      };
    });
  }

  static start(routeData) {
    return APIService.post("/start", routeData);
  }
  static stop() {
    return APIService.post("/stop");
  }
}
