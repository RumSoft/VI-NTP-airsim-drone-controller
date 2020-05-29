import React, { Component } from "react";
import { Grid, Button } from "@material-ui/core";
import logo from "./logo-xd.gif";
import "./index.scss";
import { Waypoint } from "..";

export default class Sidebar extends Component {
  render() {
    const waypoints = this.props.waypoints || [];
    return (
      <div className="sidebar">
        <img src={logo} className="logo" />

        <h1>Status</h1>
        <p> ////////////////////// </p>

        <h1>Trasa</h1>
        <div>
          {waypoints.map((x, i) => (
            <Waypoint key={`waypoint_${i}`} lngLat={x} />
          ))}
        </div>

        <Grid container className="actions">
          <Button
            className="actions__start"
            variant="contained"
            color="primary"
          >
            Start
          </Button>
          <Button
            className="actions__stop"
            disabled
            variant="contained"
            color="primary"
          >
            Stop
          </Button>
        </Grid>
      </div>
    );
  }
}
