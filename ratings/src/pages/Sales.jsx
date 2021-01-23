import { useState, useEffect, useMemo } from "react";
import { MainContent, Body, Sidebar } from "../layout/Layout";
import DatePicker from "../components/DatePicker";
import fetchFromApi from "../fetchFromApi/fetchFromApi";
import MyTable from "../components/Table";
import Chart from "../components/Chart";
import ToggleSwitch from "../components/ToggleSwitch";
import { SingleSelect } from "../components/Select";

const Sales = ({
  startDate,
  setStartDate,
  endDate,
  setEndDate,
  toggle,
  setToggle,
}) => {
  const decimalPoints = 4;
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);

  const options = [
    { value: "pln", label: "PLN" },
    { value: "chf", label: "CHF" },
    { value: "eur", label: "EUR" },
  ];

  const [selectedValue, setSelectedValue] = useState(options[0].value);
  const handleChange = (e) => {
    console.log(e);
    setSelectedValue(e.value);
  };

  useEffect(() => {
    const [start, end] = startDate.isBefore(endDate)
      ? [startDate, endDate]
      : [endDate, startDate];

    setIsLoaded(false);

    fetchFromApi(
      `/api/sales/${start.format("YYYY-MM-DD")}/${end.format(
        "YYYY-MM-DD"
      )}}/${selectedValue}`
    )(setItems, setIsLoaded, setError);
  }, [startDate, endDate, selectedValue]);

  const tableColumns = useMemo(() => {
    console.log(typeof selectedValue);
    return [
      {
        Header: "Sales",
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
            Header: selectedValue.toLocaleUpperCase(),
            accessor: selectedValue,
          },
        ],
      },
    ];
  }, [selectedValue]);

  return (
    <Body>
      <Sidebar>
        <label>Pick start date:</label>
        <DatePicker date={startDate} setDate={setStartDate} />
        <label>Pick end date:</label>
        <DatePicker date={endDate} setDate={setEndDate} />
        <SingleSelect
          selectedValue={selectedValue}
          handleChange={handleChange}
          options={options}
        />
        <ToggleSwitch
          optionLabels={["Table", "Chart"]}
          checked={toggle}
          setChecked={setToggle}
        />
      </Sidebar>
      <MainContent>
        {error ? (
          <div>Error</div>
        ) : !isLoaded ? (
          <div>Loading</div>
        ) : toggle ? (
          <Chart data={items.sales} selectedValues={["usd", selectedValue]} />
        ) : (
          items.sales && (
            <MyTable
              columns={tableColumns}
              data={
                items.sales
                  ? items.sales.map((e) => {
                      const properties = Object.getOwnPropertyNames(e);
                      properties.forEach((p) => {
                        if (p !== "date") {
                          e[p] = parseFloat(e[p]).toFixed(decimalPoints);
                        }
                      });
                      return e;
                    })
                  : []
              }
            />
          )
        )}
      </MainContent>
    </Body>
  );
};

export default Sales;
