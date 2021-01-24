import { useState, useEffect } from "react";
import moment from "moment";
import styled from "styled-components";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Sales from "./pages/Sales";
import Ratings from "./pages/Ratings";
import fetchFromApi from "./fetchFromApi/fetchFromApi";

const Main = styled.main`
  min-height: 100%;
  min-width: 100%;
  background-color: #fefefe;
`;

const StyledContainer = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
`;

function App() {
  const [errorMinMaxDates, setErrorMinMaxDates] = useState(null);
  const [isLoadedMinMaxDates, setIsLoadedMinMaxDates] = useState(false);
  const [itemsMinMaxDates, setItemsMinMaxDates] = useState({});

  const [startDate, setStartDate] = useState(moment("2013-05-05"));
  const [endDate, setEndDate] = useState(moment("2013-05-31"));
  const [toggle, setToggle] = useState(false);

  useEffect(() => {
    fetchFromApi(`/api/dates`)(
      setItemsMinMaxDates,
      setIsLoadedMinMaxDates,
      setErrorMinMaxDates
    );
  }, []);

  return (
    <Router>
      <Main>
        <Navbar name="Ratings/Sales API" />

        <Switch>
          <StyledContainer>
            <Route exact path="/">
              <Home />
            </Route>
            <Route path="/ratings">
              <Ratings
                startDate={startDate}
                setStartDate={setStartDate}
                endDate={endDate}
                setEndDate={setEndDate}
                toggle={toggle}
                setToggle={setToggle}
                itemsMinMaxDates={itemsMinMaxDates}
              />
            </Route>
            <Route path="/sales">
              <Sales
                startDate={startDate}
                setStartDate={setStartDate}
                endDate={endDate}
                setEndDate={setEndDate}
                toggle={toggle}
                setToggle={setToggle}
                itemsMinMaxDates={
                  !errorMinMaxDates && isLoadedMinMaxDates && itemsMinMaxDates
                }
              />
            </Route>
          </StyledContainer>
        </Switch>
      </Main>
    </Router>
  );
}

export default App;
