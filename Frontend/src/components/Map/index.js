import React, { Component } from "react";
import { InteractiveMap, Marker } from "react-map-gl";
import { Config } from "../..";
import { DroneService } from "../../services";
import droneIcon from "./drone-icon-arrow.png";
import map from "./map.jpg";
import "./index.scss";

export default class Map extends Component {
  constructor() {
    super();
    this.state = {
      viewport: {
        width: "100%",
        height: "100vh",
        zoom: 17,
      },
      drone: {},
      pooling: {
        delay: 500,
      },
    };

    this.tick = () => {
      DroneService.getState().then((x) => this.setState({ drone: x }));
    };

    //init & move map to drone
    DroneService.getState().then((x) => {
      this.setState({
        viewport: {
          ...this.state.viewport,
          longitude: x.longitude,
          latitude: x.latitude,
        },
        drone: x,
      });
    });

    window.addEventListener("resize", () => {
      this.setState({
        viewport: {
          ...this.state.viewport,
          width: "100%",
          height: "100vh",
        },
      });
    });
  }

  render() {
    const drone = this.state.drone;
    return (
      <div ref={(r) => (this.container = r)}>
        <InteractiveMap
          ref={(r) => (this.map = r)}
          {...this.state.viewport}
          mapStyle={Config.MAPBOX_STYLE}
          mapboxApiAccessToken={Config.MAPBOX_ACCESS_TOKEN}
          onViewportChange={(viewport) => this.setState({ viewport })}
          onContextMenu={(e) => {
            e.preventDefault();
          }}
        >
          <Marker
            latitude={drone.latitude || 0}
            longitude={drone.longitude || 0}
          >
            <img src={droneIcon} className="drone-icon" />
          </Marker>
        </InteractiveMap>
        <canvas
          id="myCanvas"
          ref={(r) => (this.canvas = r)}
          width="1540"
          height="1540"
          hidden
        ></canvas>
        <img id="xddd" ref={(r) => (this.im = r)} src={map} hidden />
      </div>
    );
  }

  componentDidMount() {
    console.log("did mount");
    var ctx = this.canvas.getContext("2d");
    this.im.addEventListener("load", () => {
      ctx.drawImage(this.im, 0, 0);
    });

    this.interval = setInterval(this.tick, this.state.pooling.delay);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  componentDidUpdate(prevProps, prevState) {
    const delay = this.state.pooling.delay;
    if (prevState.pooling.delay !== delay) {
      clearInterval(this.interval);
      this.interval = setInterval(this.tick, delay);
    }
  }
}
