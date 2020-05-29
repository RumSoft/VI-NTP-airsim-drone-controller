import React, { Component } from "react";
import { InteractiveMap, Marker } from "react-map-gl";
import { Config } from "../..";
import { DroneService } from "../../services";
import droneIcon from "./drone-icon-arrow.png";
import map from "./map.jpg";
import "./index.scss";
import { ContextMenuTrigger, ContextMenu, MenuItem } from "react-contextmenu";

export default class Map extends Component {
  constructor(props) {
    super(props);

    this.state = {
      viewport: {
        width: "100%",
        height: "100vh",
        zoom: 17,
        latitude: props.latitude,
        longitude: props.longitude,
      },
    };

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
    const map_context_menu = "map_context_menu";

    return (
      <div ref={(r) => (this.container = r)}>
        <ContextMenuTrigger id={map_context_menu}>
          <InteractiveMap
            ref={(r) => (this.map = r)}
            {...this.state.viewport}
            mapStyle={Config.MAPBOX_STYLE}
            mapboxApiAccessToken={Config.MAPBOX_ACCESS_TOKEN}
            onViewportChange={(viewport) => this.setState({ viewport })}
            onContextMenu={(e) => this.handleRightClickMenu(e)}
          >
            <Marker
              latitude={this.props.latitude}
              longitude={this.props.longitude}
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

          <ContextMenu id={map_context_menu}>
            <MenuItem data={{ foo: "bar" }} onClick={this.handleClick}>
              ContextMenu Item 1
            </MenuItem>
            <MenuItem data={{ foo: "bar" }} onClick={this.handleClick}>
              ContextMenu Item 2
            </MenuItem>
            <MenuItem divider />
            <MenuItem data={{ foo: "bar" }} onClick={this.handleClick}>
              ContextMenu Item 3
            </MenuItem>
          </ContextMenu>
        </ContextMenuTrigger>
      </div>
    );
  }

  componentDidMount() {
    var ctx = this.canvas.getContext("2d");
    this.im.addEventListener("load", () => {
      ctx.drawImage(this.im, 0, 0);
    });
  }

  handleRightClickMenu(event) {
    event.preventDefault();
    console.log("xd");
  }
}
