import React, { Component } from "react";
import { Grid } from "@material-ui/core";
import { Map, Sidebar } from "./components";
import { DroneService } from "./services";
import "./app.scss";
import { WithPooling, RandomColor } from "./utils";

// this is super-singleton-class that manages all app from this state
// >:)

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

  //init data fetch with fallback values if no api
  init() {
    DroneService.getState()
      .then((x) => {
        this.setState({
          isDataReady: true,
          latitude: x.latitude,
          longitude: x.longitude,
        });
      })
      .catch(() => {
        this.setState({
          isDataReady: true,
          latitude: 47.641482, //fallback values
          longitude: -122.140364,
        });
      });
  }

  tick() {
    return DroneService.getState().then((x) => {
      this.setState({
        latitude: x.latitude,
        longitude: x.longitude,
      });
    });
  }

  addWaypoint(wp) {
    wp = { ...wp, color: RandomColor() };
    this.setState({ waypoints: [...this.state.waypoints, wp] });
  }

  swap(arr, from, to) {
    arr.splice(from, 1, arr.splice(to, 1, arr[from])[0]);
    return arr;
  }

  // flyTo(wp) {}

  render() {
    return (
      <Grid container className="layout">
        <Grid item className="map-container">
          {this.state.isDataReady && (
            <Map
              latitude={this.state.latitude}
              longitude={this.state.longitude}
              onWaypointAdd={(wp) => this.addWaypoint(wp)}
              // onFlyImmediately={(wp) => this.flyTo(wp)}
              waypoints={this.state.waypoints}
            />
          )}
        </Grid>
        <Grid item className="sidebar-container">
          <Sidebar
            waypoints={this.state.waypoints}
            onWaypointDelete={(idx) => {
              this.setState({
                waypoints: this.state.waypoints.filter((x, i) => i != idx),
              });
            }}
            onWaypointMoveUp={(idx) => {
              this.setState({
                waypoints: this.swap(this.state.waypoints, idx, idx - 1),
              });
            }}
            onWaypointMoveDown={(idx) => {
              this.setState({
                waypoints: this.swap(this.state.waypoints, idx, idx + 1),
              });
            }}
          />
        </Grid>
      </Grid>
    );
  }

  componentDidMount() {}
}

export default WithPooling(App);
