import React, { Component } from "react";
import { LineChart, Line, YAxis, CartesianGrid, Tooltip } from "recharts";
const length = 10;

class ElevationChart extends Component {
  chartData = [
    ...new Array(length).fill(1).map((x, i) => ({ name: i, value: 0 })),
  ];
  render() {
    this.chartData = [
      ...this.chartData.slice(-length),
      {
        name: this.chartData.slice(-1)[0].name + 1,
        value: this.props.altitude.toFixed(0) || 0,
      },
    ];
    console.log(this.chartData);
    return (
      <div className="elevation-chart">
        <LineChart
          width={350}
          height={100}
          data={this.chartData}
          margin={{
            top: 5,
            bottom: 5,
            left: 0,
            right: 0,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <YAxis orientation="right" />
          <Tooltip />
          <Line
            activeDot={{ r: 8 }}
            isAnimationActive={false}
            type="monotone"
            dataKey="value"
            stroke="#8884d8"
          />
        </LineChart>
      </div>
    );
  }
}

export default ElevationChart;
