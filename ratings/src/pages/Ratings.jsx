import { useState, useEffect } from "react";
import { MainContent, Body } from "../layout/Layout";
import StyledButton from "../components/Button";
import DatePicker from "../components/DatePicker";
import moment from "moment";
import fetchFromApi from "../fetchFromApi/fetchFromApi";
import MyTable from "../components/Table";
import Chart from "../components/Chart";

const Ratings = () => {
  const [startDate, setStartDate] = useState(moment("2013-05-02"));
  const [endDate, setEndDate] = useState(moment("2013-05-06"));
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);
  const [load, setLoad] = useState(false);

  useEffect(() => {
    console.log(startDate.format("YYYY-MM-DD"));
    const [start, end] = startDate.isBefore(endDate)
      ? [startDate, endDate]
      : [endDate, startDate];

    fetchFromApi(
      `/api/rates/${start.format("YYYY-MM-DD")}/${end.format("YYYY-MM-DD")}}`
    )(setItems, setIsLoaded, setError);
  }, [load, startDate, endDate]);
  console.log(items, isLoaded, error);

  const reactOnClick = () => {
    setLoad(!load);
  };

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
      <MainContent>
        <DatePicker date={startDate} setDate={setStartDate} />
        <DatePicker date={endDate} setDate={setEndDate} />
        <StyledButton onClick={reactOnClick}>button</StyledButton>
        <StyledButton primary>primary</StyledButton>

        {!error && (
          <MyTable
            columns={tableColumns}
            data={
              items.rates &&
              items.rates.map((e) => ({
                date: e.date,
                usd: e.usd,
                eur: e.eur,
                chf: e.chf,
                interpolated: e.interpolated ? "True" : "False",
              }))
            }
          />
        )}

        <Chart data={items.rates} />
      </MainContent>
    </Body>
  );
};

export default Ratings;
