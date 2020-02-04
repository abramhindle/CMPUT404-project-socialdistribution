import React, { Component } from "react";
import "../styles/Nav.scss";
import SearchRoundedIcon from "@material-ui/icons/SearchRounded";
import HomeOutlinedIcon from "@material-ui/icons/HomeOutlined";
import PeopleAltOutlinedIcon from "@material-ui/icons/PeopleAltOutlined";
import NotificationsNoneOutlinedIcon from "@material-ui/icons/NotificationsNoneOutlined";
import ExitToAppOutlinedIcon from "@material-ui/icons/ExitToAppOutlined";
import PropTypes from "prop-types";
import logo from "../images/logo.svg";

// Example usage: <Navbar selected="Friends" />
class NavBar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: "Username",
      notification: 1,
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
    const { username, notification } = this.state;
    const { selected } = this.props;
    return (
      <div className="nav">
        <div className="navRow">
          <div className="left-menu">
            <div className="logo-container">
              <img src={logo} width="85%" alt="app logo" />
            </div>
            <div className="search-input-container">
              <SearchRoundedIcon className="searchButton" />
              <input
                className="search-input"
                placeholder="Search"
                onKeyDown={this.handleSubmit}
              />
            </div>
          </div>
          <div className="right-side-menu">
            <div className="icons">
              <a
                className={selected === "Home" ? "Home selected" : "Home"}
                href=" "
              >
                <HomeOutlinedIcon />
                <p>HOME</p>
              </a>
              <a
                className={
                  selected === "Friends" ? "Friends selected" : "Friends"
                }
                href=" "
              >
                <PeopleAltOutlinedIcon />
                <p>FRIENDS</p>
              </a>
              <a
                className={
                  selected === "Notices" ? "Notices selected" : "Notices"
                }
                href=" "
              >
                <div className="icon-wrapper">
                  <NotificationsNoneOutlinedIcon />
                  <div className="badge-wrapper">
                    <span className="badge">{notification}</span>
                  </div>
                </div>
                <p>NOTICES</p>
              </a>
            </div>
            <div className="user">
              <a href=" " className={selected === "Username" ? "selected" : ""}>
                <p>{username}</p>
              </a>
            </div>
            <div className="log-out">
              <a className="logout-div" href=" ">
                <ExitToAppOutlinedIcon />
                <p>LOG OUT</p>
              </a>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
NavBar.propTypes = {
  selected: PropTypes.string,
};

NavBar.defaultProps = {
  selected: "",
};

export default NavBar;
