import React, { Component } from "react";
import ReactMapGL, { InteractiveMap, Marker } from "react-map-gl";
import { Config } from "../..";
import droneIcon from "./drone-icon-arrow.png";
import map from "./map.jpg";
import "./index.scss";
import ContextMenu from "./ContextMenu";

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
      hasRotated: false,
      contextMenu: {
        x: 0,
        y: 0,
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
    let contextMenu = this.state.contextMenu;
    return (
      <div className="map">
        <InteractiveMap
          ref={(r) => (this.map = r)}
          {...this.state.viewport}
          maxPitch={0}
          mapStyle={Config.MAPBOX_STYLE}
          mapboxApiAccessToken={Config.MAPBOX_ACCESS_TOKEN}
          onMouseDown={(ev) => {
            this.setState({ contextMenu: null });
          }}
          onViewportChange={(viewport, interactionState) => {
            this.setState({
              viewport,
              hasRotated: interactionState.isRotating || false,
              contextMenu: null,
            });
          }}
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

        {contextMenu && (
          <ContextMenu
            ref={(r) => (this.contextMenu = r)}
            x={contextMenu.x}
            y={contextMenu.y}
            actions={[
              {
                title: "leć",
                action: () => {
                  this.props.onFlyImmediately(contextMenu.lngLat);
                  this.setState({ contextMenu: null });
                },
                disabled: true,
              },
              {
                title: "dodaj punkt",
                action: () => {
                  this.props.onWaypointAdd(contextMenu.lngLat);
                  this.setState({ contextMenu: null });
                },
              },
            ]}
          />
        )}
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
    if (this.state.hasRotated) {
      this.setState({ hasRotated: false });
      return;
    }

    this.setState({
      contextMenu: {
        x: event.center.x,
        y: event.center.y,
        lngLat: event.lngLat,
      },
    });
  }
}
