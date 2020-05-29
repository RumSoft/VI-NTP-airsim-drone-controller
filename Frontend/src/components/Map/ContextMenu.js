import React, { Component } from "react";
import "./ContextMenu.scss";
import { Paper, Button } from "@material-ui/core";

export default class ContextMenu extends Component {
  render() {
    const style = {
      top: this.props.y + "px",
      left: this.props.x + "px",
    };
    return (
      <Paper className="context-menu" style={style} elevation={3}>
        Punkt: 42.012312N, 28.123123E
        {this.props.actions &&
          this.props.actions.map((x, i) => (
            <Button
              key={`btn_${i}`}
              variant="outlined"
              color="primary"
              onClick={x.action}
            >
              {x.title}
            </Button>
          ))}
      </Paper>
    );
  }
}
