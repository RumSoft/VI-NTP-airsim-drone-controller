import React, { Component } from "react";
import { Grid } from "@material-ui/core";
import Map from "../Map";
import "./index.scss";

export default class Layout extends Component {
  render() {
    return (
      <Grid container>
        <Grid item xs={8} className="map">
          <Map />
        </Grid>
        <Grid item xs={4} className="sidebar">
          d
        </Grid>
      </Grid>
    );
  }
}
