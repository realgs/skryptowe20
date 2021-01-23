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
import { colors } from "../consts/colors";

const Chart = ({ data, selectedValues }) => {
  function formatXAxis(tickItem) {
    const decimalPoints = 2;
    return tickItem.toFixed(decimalPoints);
  }
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
          angle={-45}
          tickFormatter={formatXAxis}
          textAnchor="end"
          interval="preserveEnd"
          domain={["dataMin - 0.05", "dataMax + 0.05"]}
        />
        <Tooltip />
        <Legend align="left" verticalAlign="top" height={40} />
        {Array.isArray(selectedValues) &&
          selectedValues.map((e, index) => (
            <Line
              key={index}
              type="monotone"
              dataKey={e}
              stroke={colors.chartColors[index]}
              dot={false}
              strokeWidth={2}
            />
          ))}
      </LineChart>
    </>
  );
};

export default Chart;
