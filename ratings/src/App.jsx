import { useState } from "react";
import moment from "moment";
import styled from "styled-components";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Sales from "./pages/Sales";
import Ratings from "./pages/Ratings";

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
  const [startDate, setStartDate] = useState(moment("2013-05-05"));
  const [endDate, setEndDate] = useState(moment("2013-05-31"));
  const [toggle, setToggle] = useState(false);

  return (
    <Router>
      <Main>
        <Navbar />

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
              />
            </Route>
          </StyledContainer>
        </Switch>
      </Main>
    </Router>
  );
}

export default App;
