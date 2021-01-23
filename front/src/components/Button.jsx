import styled, { css } from "styled-components";
import { colors } from "../consts/colors";

const StyledButton = styled.button`
  display: inline-block;
  border-radius: 3px;
  padding: 0.5rem 0;
  margin: 0.5rem 1rem;
  width: 11rem;
  background: ${colors.primaryLight};
  color: ${colors.white};
  border: none;
  transition: 0.3s ease-in-out;

  :hover,
  :active,
  :focus {
    background: ${colors.primary};
  }

  ${(props) =>
    props.primary &&
    css`
      background: transparent;
      border: 2px solid ${colors.primary};
      color: black;

      :hover,
      :active,
      :focus {
        color: ${colors.white};
        background: ${colors.primary};
      }
    `}
`;

export default StyledButton;
