import React, { useState } from "react";
import PropTypes from "prop-types";
import styled, { css } from "styled-components";
import { colors } from "../consts/colors";

const ToggleSwitchWrapper = styled.div`
  display: flex;
  width: fit-content;
  flex-direction: row;
`;

const StyledLabel = styled.label`
  position: relative;
  padding: 0 0.25rem;
  ${(props) =>
    props.checked &&
    css`
      color: ${colors.navbarTextColor};
    `}
`;

const CheckBoxWrapper = styled.div`
  position: relative;
`;

const CheckBoxLabel = styled.label`
  position: absolute;
  top: 0;
  left: 0;
  width: 42px;
  height: 26px;
  border-radius: 15px;
  background: ${colors.grey};
  cursor: pointer;
  &::after {
    content: "";
    display: block;
    border-radius: 50%;
    width: 18px;
    height: 18px;
    margin: 3px;
    background: #ffffff;
    box-shadow: 1px 3px 3px 1px rgba(0, 0, 0, 0.2);
    transition: 0.2s;
  }
`;

const CheckBox = styled.input`
  opacity: 0;
  z-index: 1;
  border-radius: 15px;
  width: 42px;
  height: 26px;
  &:checked + ${CheckBoxLabel} {
    background: ${colors.primary};
    &::after {
      content: "";
      display: block;
      border-radius: 50%;
      width: 18px;
      height: 18px;
      margin-left: 21px;
      transition: 0.2s;
    }
  }
`;

const ToggleSwitch = ({ optionLabels, checked, setChecked }) => {
  const toggleOnClick = () => setChecked(!checked);

  return (
    <ToggleSwitchWrapper>
      {optionLabels && optionLabels[0] && (
        <StyledLabel checked={checked}>{optionLabels[0]}</StyledLabel>
      )}
      <CheckBoxWrapper>
        <CheckBox id="checkbox" type="checkbox" onClick={toggleOnClick} />
        <CheckBoxLabel htmlFor="checkbox" />
      </CheckBoxWrapper>

      {optionLabels && optionLabels[1] && (
        <StyledLabel checked={!checked}>{optionLabels[1]}</StyledLabel>
      )}
    </ToggleSwitchWrapper>
  );
};

export default ToggleSwitch;
