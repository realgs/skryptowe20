import { useState, useEffect } from "react";
import { MainContent, Body, Sidebar } from "../layout/Layout";
import DatePicker from "../components/DatePicker";
import fetchFromApi from "../fetchFromApi/fetchFromApi";
import MyTable from "../components/Table";
import Chart from "../components/Chart";
import ToggleSwitch from "../components/ToggleSwitch";
import { MultiSelect } from "../components/Select";

const Ratings = ({
  startDate,
  setStartDate,
  endDate,
  setEndDate,
  toggle,
  setToggle,
}) => {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);

  const options = [
    { value: "usd", label: "USD" },
    { value: "chf", label: "CHF" },
    { value: "eur", label: "EUR" },
  ];

  const [selectedValues, setSelectedValues] = useState([options[0].value]);
  const handleChange = (e) => {
    setSelectedValues(Array.isArray(e) ? e.map((x) => x.value) : []);
  };

  useEffect(() => {
    const [start, end] = startDate.isBefore(endDate)
      ? [startDate, endDate]
      : [endDate, startDate];

    fetchFromApi(
      `/api/rates/${start.format("YYYY-MM-DD")}/${end.format("YYYY-MM-DD")}}`
    )(setItems, setIsLoaded, setError);
  }, [startDate, endDate]);

  const tableColumns = [
    {
      Header: "Ratings",
      columns: [
        {
          Header: "Date",
          accessor: "date",
        },
        {
          Header: "USD",
          accessor: "usd",
        },
        {
          Header: "CHF",
          accessor: "chf",
        },
        {
          Header: "EUR",
          accessor: "eur",
        },
        {
          Header: "Interpolated",
          accessor: "interpolated",
        },
      ],
    },
  ];

  return (
    <Body>
      <Sidebar>
        <label>Pick start date:</label>
        <DatePicker date={startDate} setDate={setStartDate} />
        <label>Pick end date:</label>
        <DatePicker date={endDate} setDate={setEndDate} />

        <ToggleSwitch
          optionLabels={["Table", "Chart"]}
          checked={toggle}
          setChecked={setToggle}
        />
        {toggle && (
          <MultiSelect
            selectedValues={selectedValues}
            handleChange={handleChange}
            options={options}
          />
        )}
      </Sidebar>
      <MainContent>
        {error ? (
          <div>Error</div>
        ) : !isLoaded ? (
          <div>Loading</div>
        ) : toggle ? (
          <Chart
            data={items.rates}
            selectedValues={selectedValues}
            xLabel="Date"
            yLabel="Ratings"
          />
        ) : (
          items.rates && (
            <MyTable
              columns={tableColumns}
              data={items.rates.map((e) => ({
                date: e.date,
                usd: e.usd,
                eur: e.eur,
                chf: e.chf,
                interpolated: e.interpolated ? "True" : "False",
              }))}
            />
          )
        )}
      </MainContent>
    </Body>
  );
};

export default Ratings;
