import styled from "styled-components";
import { MainContent, Body } from "../layout/Layout";

const StyledArticle = styled.article`
  width: 100%;
  margin: 1rem 0;
`;

const Home = () => {
  const openBracket = "{";
  const closeBracket = "}";
  const hostPort = "host:port";

  return (
    <Body>
      <MainContent>
        <h1>The RESTful ratings and sales API</h1>
        <StyledArticle>
          <h3>Endpoints</h3>
          <ul>
            <li>
              <p>Get all rates.</p>
              <pre>http://{hostPort}/api/rates</pre>
            </li>
            <li>
              <p>Get rate from the specified date.</p>
              <pre>
                http://{hostPort}/api/rates/{openBracket}date{closeBracket}
              </pre>
            </li>
            <li>
              <p>Get rates for the specified dates range.</p>
              <pre>
                http://{hostPort}/api/rates/{openBracket}start_date
                {closeBracket}/{openBracket}end_date{closeBracket}
              </pre>
            </li>
            <li>
              <p>Get sales from the specified date and currency*</p>
              <pre>
                http://{hostPort}/api/sales/{openBracket}start_date
                {closeBracket}/{openBracket}currency
                {closeBracket}
              </pre>
            </li>
            <li>
              <p>Get sales from the specified dates range and currency*</p>
              <pre>
                http://{hostPort}/api/sales/{openBracket}start_date
                {closeBracket}/{openBracket}end_date
                {closeBracket}/{openBracket}currency
                {closeBracket}
              </pre>
            </li>
          </ul>
          <p>*currency can be of value: ['pln', 'chf', 'eur', 'usd']</p>
        </StyledArticle>
        <StyledArticle>
          <h3>Other</h3>
          <ul>
            <li>Cache timeout is set to 50.</li>
            <li>Request limits are set to "200 per day" and "50 per hour".</li>
          </ul>
        </StyledArticle>
        <StyledArticle>
          <h4>This API uses Northwind SQLite Database</h4>
          <a href="https://github.com/jpwhite3/northwind-SQLite3">
            https://github.com/jpwhite3/northwind-SQLite3
          </a>
        </StyledArticle>
        <StyledArticle>
          <h4>Visit github:</h4>
          <a href="https://github.com/PRZYPRAWA/skryptowe20/tree/Lab6">
            https://github.com/PRZYPRAWA/skryptowe20/tree/Lab6
          </a>
        </StyledArticle>
      </MainContent>
    </Body>
  );
};

export default Home;
