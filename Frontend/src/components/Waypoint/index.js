import React, { Component } from "react";
import "./index.scss";

export default class Waypoint extends Component {
  render() {
    const lat = (this.props.latitude || 0).toFixed(6);
    const lng = (this.props.longitude || 0).toFixed(6);

    return (
      <div className="waypoint">
        <p style={{ color: this.props.color }}>XX</p>
        {lat}, {lng}
      </div>
    );
  }
}
