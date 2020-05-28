import React, { Component } from "react";
import { Grid } from "@material-ui/core";
import Map from "../Map";
import "./index.scss";
import logo from "./logo-xd.gif";

export default class Layout extends Component {
  render() {
    return (
      <Grid container className="layout">
        <Grid item className="map">
          <Map />
        </Grid>
        <Grid item className="sidebar">
          <img src={logo} className="logo" />
          <h1>Status</h1>
          <p> ////////////////////// </p>
          <h1>Trasa</h1>
          <p> ////////////////////// </p>
        </Grid>
      </Grid>
    );
  }
}
