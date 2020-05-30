import React, { Component } from "react";
import { Grid, Button } from "@material-ui/core";
import logo from "./logo-xd.gif";
import "./index.scss";
import { Waypoint } from "..";
import { DroneService } from "../../services";
import ElevationChart from "./ElevationChart";

export default class Sidebar extends Component {
  render() {
    const waypoints = this.props.waypoints || [];
    return (
      <div className="sidebar">
        <img src={logo} className="logo" />

        <h1>Status</h1>
        <ElevationChart altitude={this.props.altitude + Math.random() * 10} />
        <div className="state">
          <p> lat: {this.props.latitude}</p>
          <p> long: {this.props.longitude}</p>
          <p> alt: {this.props.altitude}</p>
          <p> stan: {"idle"}</p>
        </div>

        <h1>Trasa [Load][Save]</h1>
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
          <Button
            className="actions__start"
            variant="contained"
            color="primary"
            onClick={() =>
              DroneService.start({
                route: waypoints.map((x) => [x.latitude, x.longitude, 30]),
              })
            }
          >
            Start
          </Button>
          <Button
            className="actions__stop"
            variant="contained"
            color="primary"
            onClick={() => DroneService.stop()}
          >
            Stop
          </Button>
        </Grid>
      </div>
    );
  }
}
