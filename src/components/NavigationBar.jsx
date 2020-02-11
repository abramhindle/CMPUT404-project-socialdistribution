import React, { Component } from "react";
import "../styles/NavigationBar.scss";
import HomeOutlinedIcon from "@material-ui/icons/HomeOutlined";
import PeopleAltOutlinedIcon from "@material-ui/icons/PeopleAltOutlined";
import NotificationsNoneOutlinedIcon from "@material-ui/icons/NotificationsNoneOutlined";
import PropTypes from "prop-types";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import InputGroup from "react-bootstrap/InputGroup";
import FormControl from "react-bootstrap/FormControl";
import NavDropdown from "react-bootstrap/NavDropdown";
import logo from "../images/logo.svg";

// Example usage: <NavigationBar selected="Friends" />
class NavigationBar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: "Username",
      numNotifications: 2,
    };
  }
  // will implement search later. Disabled eslint for this method for now

  // eslint-disable-next-line class-methods-use-this
  handleSubmit(event) {
    if (event.key === "Enter") {
      // eslint-disable-next-line no-alert
      alert(event.target.value);
    }
  }

  render() {
    const { username, numNotifications } = this.state;
    const { selected } = this.props;
    return (
      <Navbar collapseOnSelect expand="sm" fixed="top" className="navigationBar">
        <Navbar.Brand className="logo">
          <img src={logo} width="85%" alt="app logo" />
        </Navbar.Brand>
        <div className="search-input-container">
          <InputGroup size="sm" className="searchBar">
            <FormControl
              placeholder="Search"
              aria-label="Search"
              aria-describedby="basic-addon1"
            />
          </InputGroup>
        </div>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="mr-auto" />
          <Nav>
            <Nav.Link target="_blank" href="#" active={selected === "Home"}>
              <HomeOutlinedIcon />
            </Nav.Link>
            <Nav.Link target="_blank" href="#" active={selected === "Friends"}>
              <PeopleAltOutlinedIcon />
            </Nav.Link>
            <Nav.Link target="_blank" href="#" active={selected === "Notifications"}>
              <div className="notification-icon-wrapper">
                <NotificationsNoneOutlinedIcon />
                <div className="notification-badge-wrapper">
                  <span className="notification-badge">{numNotifications}</span>
                </div>
              </div>
            </Nav.Link>
          </Nav>
          <Nav>
            <NavDropdown title={username} id="username-dropdown" alignRight>
              <NavDropdown.Item href="#">Profile</NavDropdown.Item>
              <NavDropdown.Item href="#">Settings</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="#">Logout</NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    );
  }
}
NavigationBar.propTypes = {
  selected: PropTypes.string,
};

NavigationBar.defaultProps = {
  selected: "Home",
};

export default NavigationBar;
