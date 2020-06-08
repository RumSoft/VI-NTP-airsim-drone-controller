import APIService from "./APIService";

export default class {
  static getState() {
    return APIService.get("/drone-state").then((x) => x.data);
  }

  static start(routeData) {
    return APIService.post("/start", routeData);
  }

  static stop() {
    return APIService.post("/stop");
  }

  static pause() {
    return APIService.post("/wait");
  }

  static continue() {
    return APIService.post("/continue");
  }
}
