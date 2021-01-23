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
  min-width: 100vw;
  display: flex;
  flex-direction: column;
  justify-content: center;
`;

function App() {
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
              <Ratings />
            </Route>
            <Route path="/sales">
              <Sales />
            </Route>
          </StyledContainer>
        </Switch>
      </Main>
    </Router>
  );
}

export default App;
