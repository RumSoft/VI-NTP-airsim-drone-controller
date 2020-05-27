import React, { Component } from "react";
import { Grid } from "@material-ui/core";
import Map from "../Map";

export default class Layout extends Component {
  render() {
    return (
      <Grid container>
        <Grid item xs={8}>
          <Map />
        </Grid>
        <Grid item xs={4}>
          d
        </Grid>
      </Grid>
    );
  }
}
