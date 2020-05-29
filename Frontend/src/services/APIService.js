import Axios from "axios";
import config from "../../config/default";

const axios = Axios.create({
  baseURL: config.API_HOST,
  timeout: 1000,
});

export default class {
  static get(url) {
    return axios.get(url).then((x) => x.data);
  }
  static post(url, data) {
    return axios.post(url, data).then((x) => x.data);
  }
}
