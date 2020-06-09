import React, { Component } from "react";
import { Grid, Button, LinearProgress } from "@material-ui/core";
import { Map, Sidebar } from "./components";
import { DroneService } from "./services";
import { WithPooling, RandomColor } from "./utils";
const { dialog } = require("electron").remote;
import "./app.scss";
import fs from "fs";

// this is super-singleton-class that manages all app from this state
// >:)

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isBusy: false,
      isDataReady: false,
      gps_position: null,
      waypoints: [],
      state: "not connected",
      error: null,
    };
  }

  //init data fetch with fallback values if no api
  connect() {
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
            ...x,
          },
          () => this.props.startPooling()
        );
      })
      .catch(() => {
        this.setState({
          isBusy: false,
          error: "couldn't fetch data",
          isDataReady: false,
          state: "error connecting",
          gps_position: {
            latitude: 47.641482, //fallback values
            longitude: -122.140364,
            altitude: -1,
          },
        });
      });
  }

  tick() {
    return DroneService.getState().then((x) => {
      this.setState({ ...x });
    });
  }

  render() {
    const waypoints = this.state.waypoints;
    const target =
      (this.state.state == "flying" && this.state.target_position) ||
      (waypoints && waypoints[0]) ||
      null;
    return (
      <React.Fragment>
        <Grid container className="layout">
          <Grid item className="map-container">
            {this.state.isDataReady && (
              <Map
                gps_position={this.state.gps_position}
                waypoints={this.state.waypoints}
                onWaypointAdd={(wp) =>
                  this.updateWaypoints([
                    ...this.state.waypoints,
                    { ...wp, color: RandomColor() },
                  ])
                }
                target={target}
              />
            )}
          </Grid>
          <Grid item className="sidebar-container">
            <Sidebar
              gps_position={this.state.gps_position}
              waypoints={waypoints}
              state={(this.state.waiting && "paused") || this.state.state}
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
              SaveWaypoints={() => {
                dialog
                  .showSaveDialog({
                    filters: [{ name: "pliki json", extensions: ["json"] }],
                    properties: ["openFile", "createDirectory"],
                  })
                  .then((result) => {
                    if (result.canceled) return;
                    fs.writeFileSync(
                      result.filePath,
                      JSON.stringify(waypoints)
                    );
                  })
                  .catch((err) => {
                    alert(`błąd zapisu trasy: ${err}`);
                  });
              }}
              OpenLoadWaypoints={() => {
                dialog
                  .showOpenDialog({
                    properties: ["openFile"],
                  })
                  .then((result) => {
                    if (result.canceled) return;
                    let data = fs.readFileSync(
                      result.filePaths[0],
                      "utf-8",
                      "r"
                    );
                    this.setState({ waypoints: JSON.parse(data) });
                  })
                  .catch((err) => {
                    alert(`błąd wczytywania trasy: ${err}`);
                  });
              }}
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
  }

  swap(arr, from, to) {
    arr.splice(from, 1, arr.splice(to, 1, arr[from])[0]);
    return arr;
  }
}

export default WithPooling(App);
