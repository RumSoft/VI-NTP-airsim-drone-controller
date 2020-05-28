import { randomBytes } from "crypto";

export default {
  getState: () =>
    Promise.resolve({
      // longitude: -122.138565,
      // latitude: 47.640269,
      latitude: 47.641482 + Math.random() / 1000,
      longitude: -122.140364 + Math.random() / 1000,
      altitude: 30.0,
    }),
};
