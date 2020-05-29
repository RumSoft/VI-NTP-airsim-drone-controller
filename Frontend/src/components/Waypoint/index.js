import React, { Component } from "react";

export default class Waypoint extends Component {
  render() {
    return (
      <div>
        <p style={{ color: this.props.color }}>XX</p>
        {this.props.latitude || 0},{this.props.longitude || 0}
      </div>
    );
  }
}
