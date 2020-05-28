import React, { Component } from "react";
import { InteractiveMap } from "react-map-gl";
import myImage from "./mapka2.jpg";
import { Config } from "../..";
import { DroneService } from "../../services";

export default class Map extends Component {
  constructor() {
    super();
    this.state = {
      viewport: {
        width: "100%",
        height: "100vh",
        zoom: 17,
      },
      drone: {
        position: [47.641482, -122.140364],
      },
      pooling: {
        delay: 300,
      },
    };

    this.tick = () => {
      DroneService.getState();
    };
  }

  render() {
    return (
      <div>
        <InteractiveMap
          ref={(r) => (this.map = r)}
          {...this.state.viewport}
          mapStyle={Config.MAPBOX_STYLE}
          mapboxApiAccessToken={Config.MAPBOX_ACCESS_TOKEN}
          onViewportChange={(viewport) => this.setState({ viewport })}
        />
        <canvas
          id="myCanvas"
          ref={(r) => (this.canvas = r)}
          width="1540"
          height="1540"
          hidden
        ></canvas>
        <img id="xddd" ref={(r) => (this.im = r)} src={myImage} hidden />
      </div>
    );
  }

  componentDidMount() {
    console.log("did mount");
    var ctx = this.canvas.getContext("2d");
    this.im.addEventListener("load", () => {
      ctx.drawImage(this.im, 0, 0);
    });
    console.log("a");

    this.interval = setInterval(this.tick, this.state.pooling.delay);
  }

  componentWillUnmount() {
    console.log("will unmount");
    clearInterval(this.interval);
  }

  componentDidUpdate(prevProps, prevState) {
    console.log("did update");
    if (prevState.pooling.delay !== this.state.pooling.delay) {
      clearInterval(this.interval);
      this.interval = setInterval(this.tick, this.state.pooling.delay);
    }
  }
}
