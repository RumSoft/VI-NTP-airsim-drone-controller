import React, { Component } from "react";

export default class Waypoint extends Component {
  render() {
    const [lng, lat] = this.props.lngLat;
    return <div>{lng}</div>;
  }
}
