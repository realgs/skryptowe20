import { Link } from "react-router-dom";
import styled from "styled-components";
import { colors } from "../consts/colors";

const StyledHeader = styled.header`
  --navbar-height: 64px;
  height: var(--navbar-height);
  background-color: ${colors.navbarBgColor};
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);

  &.opened .navbar-toggle .icon-bar:first-child,
  &.opened .navbar-toggle .icon-bar:last-child {
    position: absolute;
    margin: 0;
    width: 30px;
  }

  &.opened .navbar-toggle .icon-bar:first-child {
    transform: rotate(45deg);
  }

  &.opened .navbar-toggle .icon-bar:nth-child(2) {
    opacity: 0;
  }

  &.opened .navbar-toggle .icon-bar:last-child {
    transform: rotate(-45deg);
  }

  &.opened .navbar-menu {
    background-color: rgba(0, 0, 0, 0.4);
    opacity: 1;
    visibility: visible;
  }

  &.opened .navbar-links {
    padding: 1em;
    max-height: none;
  }

  @media screen and (min-width: 700px) {
    & .navbar-menu,
    &.opened .navbar-menu {
      visibility: visible;
      opacity: 1;
      position: static;
      display: block;
      height: 100%;
    }

    & .navbar-links,
    &.opened .navbar-links {
      margin: 0;
      padding: 0;
      box-shadow: none;
      position: static;
      flex-direction: row;
      list-style-type: none;
      max-height: max-content;
      width: 100%;
      height: 100%;
    }

    & .navbar-link:last-child {
      margin-right: 0;
    }
  }
`;

const StyledNav = styled.nav`
  max-width: 1000px;
  padding-left: 1.4rem;
  padding-right: 1.4rem;
  margin-left: auto;
  margin-right: auto;

  display: flex;
  justify-content: space-between;
  height: 100%;
  align-items: center;
`;

const HomeLink = styled(Link)`
  color: ${colors.navbarTextColor};
  transition: color 0.2s ease-in-out;
  text-decoration: none;
  display: flex;
  font-weight: 400;
  align-items: center;
  transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out;

  :hover,
  :focus {
    color: ${colors.white};
  }
`;

const StyledButton = styled.button`
  cursor: pointer;
  border: none;
  background-color: transparent;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;

  :hover .icon-bar,
  :focus .icon-bar {
    background-color: ${colors.white};
  }

  @media screen and (min-width: 700px) {
    display: none;
  }
`;

const IconBar = styled.span`
  display: block;
  width: 25px;
  height: 4px;
  margin: 2px;
  transition: background-color 0.2s ease-in-out, transform 0.2s ease-in-out,
    opacity 0.2s ease-in-out;
  background-color: ${colors.navbarTextColor};
`;

const NavbarMenu = styled.div`
  position: fixed;
  top: var(--navbar-height);
  bottom: 0;
  transition: opacity 0.2s ease-in-out, visibility 0.2s ease-in-out;
  opacity: 0;
  visibility: hidden;
  left: 0;
  right: 0;
`;

const NavbarLinks = styled.ul`
  list-style-type: none;
  max-height: 0;
  overflow: hidden;
  position: absolute;
  background-color: ${colors.navbarBgColor};
  display: flex;
  flex-direction: column;
  align-items: center;
  left: 0;
  right: 0;
  margin: 1.4rem;
  border-radius: 5px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
`;

const NavbarItem = styled.li`
  margin: 0.4em;
  width: 100%;
`;

const NavbarLink = styled(Link)`
  color: ${colors.navbarTextColor};
  transition: color 0.2s ease-in-out;
  text-decoration: none;
  display: flex;
  font-weight: 400;
  align-items: center;
  transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out;

  justify-content: center;
  width: 100%;
  padding: 0.4em 0.8em;
  border-radius: 5px;

  :focus,
  :hover {
    color: ${colors.white};
    background-color: ${colors.navbarBgContrast};
  }
`;

const Navbar = ({ name }) => {
  return (
    <StyledHeader id="navbar">
      <StyledNav>
        <HomeLink to="/">{name}</HomeLink>
        <StyledButton
          type="button"
          className="navbar-toggle"
          aria-label="Open navigation menu"
        >
          <IconBar className="icon-bar"></IconBar>
          <IconBar className="icon-bar"></IconBar>
          <IconBar className="icon-bar"></IconBar>
        </StyledButton>
        <NavbarMenu className="navbar-menu">
          <NavbarLinks className="navbar-links">
            <NavbarItem>
              <NavbarLink className="navbar-link" to="/">
                Home
              </NavbarLink>
            </NavbarItem>
            <NavbarItem>
              <NavbarLink className="navbar-link" to="/ratings">
                Ratings
              </NavbarLink>
            </NavbarItem>
            <NavbarItem>
              <NavbarLink className="navbar-link" to="/sales">
                Sales
              </NavbarLink>
            </NavbarItem>
          </NavbarLinks>
        </NavbarMenu>
      </StyledNav>
    </StyledHeader>
  );
};

export default Navbar;
