import React, { Component } from "react";
import "./index.scss";
import { Button, Icon, Chip, ButtonGroup } from "@material-ui/core";
import DeleteForeverIcon from "@material-ui/icons/DeleteForever";
import ArrowUpwardIcon from "@material-ui/icons/ArrowUpward";
import ArrowDownwardIcon from "@material-ui/icons/ArrowDownward";
var equal = require("fast-deep-equal/react");

export default class Waypoint extends Component {
  render() {
    const lat = (this.props.latitude || 0).toFixed(6);
    const lng = (this.props.longitude || 0).toFixed(6);
    const color = this.props.color || "gray";
    const isFirst = this.props.i == 0;
    const isLast = this.props.i == this.props.n - 1;
    return (
      <div className="waypoint" style={{ borderColor: color }}>
        <div style={{ backgroundColor: color }} className="waypoint__block" />
        <p className="waypoint__label">
          ({lat}, {lng})
        </p>
        <ButtonGroup className="waypoint__actions">
          <Button disabled={isFirst} onClick={() => this.props.onUp?.()}>
            <ArrowUpwardIcon />
          </Button>

          <Button disabled={isLast} onClick={() => this.props.onDown?.()}>
            <ArrowDownwardIcon />
          </Button>
          <Button onClick={() => this.props.onDelete?.()} color="secondary">
            <DeleteForeverIcon />
          </Button>
        </ButtonGroup>
        <div></div>
      </div>
    );
  }
  shouldComponentUpdate(nextProps, nextState) {
    return !equal(nextProps, this.props);
  }
}
