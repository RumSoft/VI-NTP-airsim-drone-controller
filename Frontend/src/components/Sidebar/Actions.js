import React from "react";
import { Button } from "@material-ui/core";
import PlayArrowIcon from "@material-ui/icons/PlayArrow";
import PauseIcon from "@material-ui/icons/Pause";
import StopIcon from "@material-ui/icons/Stop";
import { DroneService } from "../../services";

export default (props) => {
  const isIdle = props.state == "idle";
  const hasWaypoints = !!props.waypoints.length;
  const isFlying = props.state == "flying";
  const isPaused = props.state == "paused";
  return (
    <React.Fragment>
      <Button
        className="actions__start"
        variant="contained"
        color="primary"
        disabled={!hasWaypoints || !isIdle}
        onClick={() =>
          DroneService.start({
            route: props.waypoints.map((x) => [x.latitude, x.longitude, 10]),
          })
        }
      >
        <PlayArrowIcon />
        Start
      </Button>
      <Button
        className="actions__stop"
        variant="contained"
        color="primary"
        disabled={!isFlying}
        onClick={() => DroneService.pause()}
      >
        <PauseIcon />
        Pauza
      </Button>
      <Button
        className="actions__stop"
        variant="contained"
        color="primary"
        disabled={!isPaused || isIdle}
        onClick={() => DroneService.continue()}
      >
        <PlayArrowIcon />
        <small>Kontynuuj</small>
      </Button>
      <Button
        className="actions__stop"
        variant="contained"
        color="primary"
        disabled={!isFlying && !isPaused}
        onClick={() => DroneService.stop()}
      >
        <StopIcon />
        Stop
      </Button>
    </React.Fragment>
  );
};
