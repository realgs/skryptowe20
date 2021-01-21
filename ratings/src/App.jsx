import styled from "styled-components";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import { MainContent, Body } from "./layout/Layout";
import Home from "./pages/Home";

const Main = styled.main`
  min-height: 100%;
  min-width: 100%;
  background: #fefefe;
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

function Ratings() {
  return (
    <Body>
      <MainContent>Ratings</MainContent>
    </Body>
  );
}

function Sales() {
  return (
    <Body>
      <MainContent>Sales</MainContent>
    </Body>
  );
}
