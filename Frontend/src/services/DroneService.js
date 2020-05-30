import APIService from "./APIService";

export default class {
  static getState() {
    return APIService.get("/position").then((x) => ({
      latitude: x.data.latitude || 47.64,
      longitude: x.data.longitude || -122.14,
      altitude: x.data.altitude || 0,
    }));
  }

  ///route data is [ [lat,long,alt], ... ]
  static sendRoute(routeData) {
    console.log({ route: routeData });
    return APIService.post("/route", {
      route: routeData,
    });
  }
  static start() {
    return APIService.post("/start");
  }
  static stop() {
    return APIService.post("/start");
  }
  static connect() {
    return APIService.post("/connect");
  }
}
