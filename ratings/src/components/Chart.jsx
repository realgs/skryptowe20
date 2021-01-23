import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

const Chart = ({ data }) => {
  return (
    <>
      <LineChart
        width={700}
        height={500}
        data={data}
        margin={{
          top: 20,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" angle={-45} textAnchor="end" height={70} />
        <YAxis
          interval="preserveEnd"
          domain={["dataMin - 0.05", "dataMax + 0.05"]}
        />
        <Tooltip />
        <Legend align="left" verticalAlign="top" height={40} />
        <Line
          type="monotone"
          dataKey="usd"
          stroke="#8884d8"
          dot={false}
          strokeWidth={2}
        />
        <Line
          type="monotone"
          dataKey="chf"
          stroke="#82ca9d"
          dot={false}
          strokeWidth={2}
        />
      </LineChart>
    </>
  );
};

export default Chart;
