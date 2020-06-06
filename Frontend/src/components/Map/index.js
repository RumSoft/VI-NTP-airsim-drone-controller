import React, { Component } from "react";
import ReactMapGL, {
  InteractiveMap,
  Marker,
  Source,
  Layer,
} from "react-map-gl";
import droneIcon from "./drone-icon-arrow.png";
import "./index.scss";
import ContextMenu from "./ContextMenu";
import config from "../../../config/default";

export default class Map extends Component {
  constructor(props) {
    super(props);

    this.state = {
      viewport: {
        width: "100%",
        height: "100vh",
        zoom: 17,
        latitude: props.gps_position.latitude,
        longitude: props.gps_position.longitude,
      },
      hasRotated: false,
      contextMenu: null,
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
    const contextMenu = this.state.contextMenu;
    const contextMenuLngLat = contextMenu && {
      latitude: contextMenu.latitude,
      longitude: contextMenu.longitude,
    };
    const gps_position = this.props.gps_position;

    const polylineGeoJSON = {
      type: "Feature",
      properties: {},
      geometry: {
        type: "LineString",
        coordinates: [
          ...this.props.waypoints.map((x) => [x.longitude, x.latitude]),
        ],
      },
    };
    return (
      <div className="map">
        <InteractiveMap
          ref={(r) => (this.map = r)}
          {...this.state.viewport}
          maxPitch={0}
          mapStyle="mapbox://styles/dr124/ckb3kyztp0zzn1jmxffpf2ls3"
          mapboxApiAccessToken="pk.eyJ1IjoiZHIxMjQiLCJhIjoiY2tiM2s2b3V3MDlseDJzbnlsMjkwNDlneiJ9.wTcTSVN4wWF2sxSKcwE82g"
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
            latitude={gps_position.latitude}
            longitude={gps_position.longitude}
          >
            <img src={droneIcon} className="drone-icon" />
          </Marker>
          <Source id="polylineLayer" type="geojson" data={polylineGeoJSON}>
            <Layer
              id="lineLayer"
              type="line"
              source="my-data"
              layout={{
                "line-join": "round",
                "line-cap": "round",
              }}
              paint={{
                "line-color": "rgba(3, 170, 238, 1)",
                "line-width": 5,
              }}
            />
          </Source>
        </InteractiveMap>

        {contextMenu && (
          <ContextMenu
            ref={(r) => (this.contextMenu = r)}
            x={contextMenu.x}
            y={contextMenu.y}
            {...contextMenuLngLat}
            actions={[
              {
                title: "Dodaj do trasy",
                onClick: () => {
                  this.props.onWaypointAdd(contextMenuLngLat);
                  this.setState({ contextMenu: null });
                },
              },
            ]}
          />
        )}
      </div>
    );
  }

  componentDidMount() {}

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
        longitude: event.lngLat[0],
        latitude: event.lngLat[1],
      },
    });
  }
}
