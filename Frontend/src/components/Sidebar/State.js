import React from "react";

export default (props) => {
  return (
    <div className="state">
      <p>
        ({props.gps_position.latitude.toFixed(5)},{" "}
        {props.gps_position.longitude.toFixed(5)}), alt:{" "}
        {props.gps_position.altitude.toFixed(1)}
      </p>
      <p> stan: {props.state}</p>
    </div>
  );
};
