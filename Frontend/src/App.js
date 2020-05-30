import React, { Component } from "react";
import { Grid, Button, LinearProgress } from "@material-ui/core";
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
      isBusy: false,
      latitude: 0,
      longitude: 0,
      isDataReady: false,
      waypoints: [],
      state: "flying",
      error: null,
    };
  }

  connect() {
    this.setState({
      isBusy: true,
    });
    this.init();
  }

  //init data fetch with fallback values if no api
  init() {
    this.setState({
      isBusy: true,
    });
    DroneService.getState()
      .then((x) => {
        this.setState(
          {
            isBusy: false,
            error: null,
            isDataReady: true,
            latitude: x.latitude,
            longitude: x.longitude,
            altitude: x.altitude,
          },
          () => this.props.startPooling()
        );
      })
      .catch(() => {
        this.setState({
          isBusy: false,
          error: "couldn't fetch data",
          isDataReady: true,
          latitude: 47.641482, //fallback values
          longitude: -122.140364,
          altitude: -1,
        });
      });
  }

  tick() {
    return DroneService.getState().then((x) => {
      this.setState({
        latitude: x.latitude,
        longitude: x.longitude,
        altitude: x.altitude,
      });
    });
  }

  swap(arr, from, to) {
    arr.splice(from, 1, arr.splice(to, 1, arr[from])[0]);
    return arr;
  }

  // flyTo(wp) {}

  render() {
    return (
      <React.Fragment>
        <Grid container className="layout">
          <Grid item className="map-container">
            {this.state.isDataReady && (
              <Map
                latitude={this.state.latitude}
                longitude={this.state.longitude}
                onWaypointAdd={(wp) =>
                  this.updateWaypoints([
                    ...this.state.waypoints,
                    { ...wp, color: RandomColor() },
                  ])
                }
                // onFlyImmediately={(wp) => this.flyTo(wp)}
                waypoints={this.state.waypoints}
              />
            )}
          </Grid>
          <Grid item className="sidebar-container">
            <Sidebar
              latitude={this.state.latitude}
              longitude={this.state.longitude}
              altitude={this.state.altitude}
              waypoints={this.state.waypoints}
              onWaypointDelete={(idx) =>
                this.updateWaypoints(
                  this.state.waypoints.filter((x, i) => i != idx)
                )
              }
              onWaypointMoveUp={(idx) =>
                this.updateWaypoints(
                  this.swap(this.state.waypoints, idx, idx - 1)
                )
              }
              onWaypointMoveDown={(idx) =>
                this.updateWaypoints(
                  this.swap(this.state.waypoints, idx, idx + 1)
                )
              }
            />
          </Grid>
        </Grid>
        {this.state.error && (
          <div className="error-screen">
            <div className="error-bar">
              <h1>Error ( ͠° ͟ʖ ͡°)</h1>
              <p>{this.state.error}</p>
              <Button
                onClick={() => this.connect()}
                variant="contained"
                color="secondary"
              >
                Reconnect
              </Button>
            </div>
          </div>
        )}
        {this.state.isBusy && <LinearProgress className="loader" />}
      </React.Fragment>
    );
  }

  componentDidMount() {
    this.connect();
  }

  updateWaypoints(wp) {
    this.setState({ waypoints: wp });
    // DroneService.sendRoute(
    //   wp.map((x) => ({
    //     ...x,
    //     altitude: 30,
    //   }))
    // );
  }
}

export default WithPooling(App);
