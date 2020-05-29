import React, { Component } from "react";
import { Grid } from "@material-ui/core";
import { Map, Sidebar } from "./components";
import { DroneService } from "./services";
import "./app.scss";
import { WithPooling } from "./utils";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      latitude: 0,
      longitude: 0,
      isDataReady: false,
      waypoints: [],
    };
    this.init();
  }

  init() {
    DroneService.getState().then((x) => {
      this.setState({
        latitude: x.latitude,
        longitude: x.longitude,
        isDataReady: true,
      });
    });
  }

  tick() {
    DroneService.getState().then((x) => {
      this.setState({
        latitude: x.latitude,
        longitude: x.longitude,
      });
    });
  }

  render() {
    return (
      <Grid container className="layout">
        <Grid item className="map-container">
          {this.state.isDataReady && (
            <Map
              latitude={this.state.latitude}
              longitude={this.state.longitude}
              onWaypointAdd={(wp) => {
                this.setState({ waypoints: [...this.state.waypoints, wp] });
              }}
              onFlyImmediately={(wp) => {
                this.setState({ waypoints: [...this.state.waypoints, wp] });
              }}
            />
          )}
        </Grid>
        <Grid item className="sidebar-container">
          <Sidebar waypoints={this.state.waypoints} />
        </Grid>
      </Grid>
    );
  }
}

export default WithPooling(App);
