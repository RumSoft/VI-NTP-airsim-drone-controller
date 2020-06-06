import React, { Component } from "react";
import { Grid, Button } from "@material-ui/core";
import logoxd from "./logo-xd.gif";
import logo from "./logo.gif";
import "./index.scss";
import { Waypoint } from "..";
import ElevationChart from "./ElevationChart";
import State from "./State";
import Actions from "./Actions";

export default class Sidebar extends Component {
  render() {
    const waypoints = this.props.waypoints || [];
    const gps_position = this.props.gps_position || {
      latitude: -1,
      longitude: -1,
      altitude: -1,
    };

    return (
      <div className="sidebar">
        <img src={logo} className="logo" />

        <h1>Status</h1>
        <ElevationChart altitude={gps_position.altitude} />
        <State gps_position={gps_position} state={this.props.state} />

        <h1>
          Trasa{" "}
          <span>
            <Button variant="outlined" color="primary">
              save
            </Button>
            <Button variant="outlined" color="secondary">
              load
            </Button>{" "}
          </span>
        </h1>
        <div className="waypoints">
          {waypoints.map((x, i) => (
            <Waypoint
              key={`waypoint_${i}`}
              i={i}
              n={waypoints.length}
              {...x}
              onDelete={() => this.props.onWaypointDelete?.(i)}
              onUp={() => this.props.onWaypointMoveUp?.(i)}
              onDown={() => this.props.onWaypointMoveDown?.(i)}
            />
          ))}
        </div>

        <Grid container className="actions">
          <Actions waypoints={waypoints} state={this.props.state} />
        </Grid>
      </div>
    );
  }
}
