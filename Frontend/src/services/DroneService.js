import APIService from "./APIService";

export default class {
  static getState() {
    return APIService.get("/position").then((x) => ({
      latitude: x.latitude || 47,
      longitude: x.longitude || -120,
      altitude: x.altitude || 0,
    }));
  }
  static sendRoute(route) {
    return APIService.post("/route", route);
  }
  static start() {
    return APIService.post("/start");
  }
  static stop() {
    return APIService.post("/start");
  }
  static connect() {
    console.log("connecting");
    return APIService.post("/connect");
  }
}
