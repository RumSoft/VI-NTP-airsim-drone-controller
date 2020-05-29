import React, { Component } from "react";
import "./ContextMenu.scss";
import { Paper, Button } from "@material-ui/core";

export default class ContextMenu extends Component {
  formatLatitude(lat) {
    lat = lat.toFixed(5);
    return lat;
  }
  formatLongitude(long) {
    long = long.toFixed(5);
    return long;
  }

  render() {
    const style = {
      top: this.props.y + "px",
      left: this.props.x + "px",
    };
    return (
      <Paper className="context-menu" style={style} elevation={3}>
        <p className="context-menu__title">Punkt</p>
        <p className="context-menu__coordinates">
          ({this.formatLatitude(this.props.latitude || 0)},{" "}
          {this.formatLongitude(this.props.longitude || 0)})
        </p>

        <div className="context-menu__actions">
          {(this.props.actions || []).map((x, i) => (
            <Button key={`btn_${i}`} variant="contained" color="primary" {...x}>
              {x.title}
            </Button>
          ))}
        </div>
      </Paper>
    );
  }
}
