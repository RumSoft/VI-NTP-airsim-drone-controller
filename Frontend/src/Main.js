import React, { Component } from "react";
import Layout from "./components/Layout";
import "./Main.css";
import {
  MuiThemeProvider,
  CssBaseline,
  createMuiTheme,
} from "@material-ui/core";

const darkTheme = createMuiTheme({
  palette: {
    type: "dark",
  },
});

export default () => (
  <MuiThemeProvider theme={darkTheme}>
    <CssBaseline />
    <Layout />
  </MuiThemeProvider>
);
