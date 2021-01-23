import { useState, useEffect } from "react";
import { MainContent, Body, Sidebar } from "../layout/Layout";
import DatePicker from "../components/DatePicker";
import moment from "moment";
import fetchFromApi from "../fetchFromApi/fetchFromApi";
import MyTable from "../components/Table";
import Chart from "../components/Chart";
import ToggleSwitch from "../components/ToggleSwitch";

const Ratings = () => {
  const [startDate, setStartDate] = useState(moment("2013-05-02"));
  const [endDate, setEndDate] = useState(moment("2013-05-06"));
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);
  const [toggle, setToggle] = useState(false);

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
          Header: "EUR",
          accessor: "eur",
        },
        {
          Header: "CHF",
          accessor: "chf",
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
      </Sidebar>
      <MainContent>
        {error ? (
          <div>Error</div>
        ) : !isLoaded ? (
          <div>Loading</div>
        ) : toggle ? (
          <Chart data={items.rates} />
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
