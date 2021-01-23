import Select from "react-select";
import makeAnimated from "react-select/animated";
import styled from "styled-components";

const animatedComponents = makeAnimated();

const StyledSelect = styled(Select)`
  width: 250px;
  margin: 0.5rem 0;
`;

export const MultiSelect = ({ selectedValues, handleChange, options }) => {
  return (
    <StyledSelect
      onChange={handleChange}
      value={options.filter((obj) => selectedValues.includes(obj.value))}
      closeMenuOnSelect={false}
      defaultValue={[options[0]]}
      components={animatedComponents}
      isMulti
      options={options}
    />
  );
};

export const SingleSelect = ({ selectedValue, handleChange, options }) => {
  return (
    <Select
      onChange={handleChange}
      value={options.find((obj) => obj.value === selectedValue)}
      classNamePrefix="select"
      defaultValue={options[0]}
      name="color"
      options={options}
    />
  );
};
