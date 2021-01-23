import styled from "styled-components";

export const Body = styled.div`
  display: flex;
  padding: 1em;
  flex-grow: 1;
  max-width: 100vw;
  margin: auto;
`;

export const Section = styled.div`
  display: flex;
  flex-direction: column;
  padding: 1em;
`;

export const MainContent = styled(Section)`
  flex-grow: 1;
  min-width: 800px;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

export const Sidebar = styled(Section)`
  min-width: 300px;

  @media (max-width: 768px) {
    display: none;
  }
`;
