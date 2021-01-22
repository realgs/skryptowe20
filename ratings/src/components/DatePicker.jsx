import React, { useState } from "react";
import "react-dates/initialize";
import { SingleDatePicker } from "react-dates";
import moment from "moment";
import styled from "styled-components";
import "react-dates/lib/css/_datepicker.css";
import { colors } from "../consts/colors";

const falseFunc = () => false;

const StyledDatePickerWrapper = styled.div`
  & .SingleDatePicker,
  .SingleDatePickerInput {
    .DateInput {
      height: 40px;
      display: flex;

      .DateInput_input {
        font-size: 1rem;
        border: 0;
        padding: 12px 16px 14px;
      }
    }

    .SingleDatePickerInput__withBorder {
      margin: 0.5em 1em;
      overflow: hidden;

      :hover {
        border: 2px solid ${colors.primary};
      }

      .CalendarDay__selected {
        background: ${colors.primaryDark};
        border: 2px solid ${colors.primary};
      }
    }

    .SingleDatePicker_picker.SingleDatePicker_picker {
      top: 43px;
      left: 2px;
    }
  }
`;

const DatePicker = () => {
  const [focused, setFocused] = useState(false);
  const [date, setDate] = useState(moment());

  return (
    <StyledDatePickerWrapper>
      <SingleDatePicker
        isOutsideRange={falseFunc}
        numberOfMonths={1}
        onDateChange={(date) => {
          console.log(date);
          setDate(date);
        }}
        onFocusChange={({ focused }) => setFocused(focused)}
        focused={focused}
        date={date}
      />
    </StyledDatePickerWrapper>
  );
};

export default DatePicker;
