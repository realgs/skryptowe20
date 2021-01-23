import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  BarChart,
  Bar,
} from "recharts";
import { colors } from "../consts/colors";

const Chart = ({ data, selectedValues, xLabel, yLabel }) => {
  function formatXAxis(tickItem) {
    const decimalPoints = 2;
    return tickItem.toFixed(decimalPoints);
  }

  return (
    <>
      {Array.isArray(data) && data.length == 1 ? (
        <BarChart
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
          <XAxis
            dataKey="date"
            angle={-45}
            textAnchor="end"
            height={70}
            label={{ value: xLabel, angle: -45 }}
          />
          <YAxis angle={-45} label={{ value: yLabel, angle: -45 }} />
          <Tooltip />
          <Legend align="left" verticalAlign="top" height={40} />
          {Array.isArray(selectedValues) &&
            selectedValues.map((e, index) => (
              <Bar
                key={index}
                type="monotone"
                dataKey={e}
                fill={colors.chartColors[index]}
                dot={false}
                strokeWidth={2}
              />
            ))}
        </BarChart>
      ) : (
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
          <XAxis
            dataKey="date"
            angle={-45}
            textAnchor="end"
            height={70}
            label={{ value: xLabel, angle: -45 }}
          />
          <YAxis
            label={{ value: yLabel, angle: -45 }}
            angle={-45}
            tickFormatter={formatXAxis}
            textAnchor="end"
            interval="preserveEnd"
            domain={["dataMin", "dataMax"]}
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
      )}
    </>
  );
};

export default Chart;
