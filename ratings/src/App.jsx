import styled from "styled-components";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import Navbar from "./components/Navbar";
import { MainContent, Body, Sidebar } from "./layout/Layout";

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
            <Route path="/about">
              <About />
            </Route>
            <Route path="/users">
              <Users />
            </Route>
          </StyledContainer>
        </Switch>
      </Main>
    </Router>
  );
}

export default App;

function Home() {
  return (
    <Body>
      <MainContent>ELo</MainContent>
      <Sidebar>Elo</Sidebar>
    </Body>
  );
}

function About() {
  return (
    <Body>
      <MainContent>About</MainContent>
    </Body>
  );
}

function Users() {
  return (
    <Body>
      <MainContent>Users</MainContent>
    </Body>
  );
}
