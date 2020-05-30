import APIService from "./APIService";

export default class drone {
  static getState() {
    return APIService.get("/drone-state");
  }
}
