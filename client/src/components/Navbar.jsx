import React, { Component } from 'react';
import '../styles/navbar.css';
import { setCurrentUser } from '../redux/user/actions';
import { connect } from 'react-redux'

class Navbar extends Component {

  constructor(props) {
    super(props);
    this.state = {};
  }

  renderNavItems = () => {
    const { currentUser } = this.props;
    switch (currentUser) {
      case null:
        return (
          <div>
            <li id="nav-item-signup"> <a href="/register">Sign up</a> </li>
            <li id="nav-item-login"> <a href="/login">Log in</a> </li>
          </div>
        );
      default:
        return (
          <div>
            <li id="nav-item-logout" onClick={() => {
              this.props.setCurrentUser(null);
              localStorage.removeItem("state")
            }}><a href="/service/author/logout/">Log out</a> </li>
            <li id="nav-item-3"> <a href="/me">Me</a> </li>
          </div>
        );
    }
  }

  render() {
    return (
      <nav id="navbar">
        <h1 id="navbar-title"> <a href="/">Social Distribution</a> </h1>
        <ul>
          {/* <li id="nav-item-1"> <a href="/register">Sign up</a> </li>
          <li id="nav-item-2"> <a href="/login">Log in</a> </li>
          <li id="nav-item-3"> <a href="/me">Me</a> </li> */}
          {this.renderNavItems()}
        </ul>
      </nav>
    )
  }
}

const mapDispatchToProps = (dispatch) => ({
  setCurrentUser: (user) => {
    dispatch(setCurrentUser(user))
  }
})

const mapStateToProps = (state) => ({
  currentUser: state.user.currentUser
})

export default connect(mapStateToProps, mapDispatchToProps)(Navbar);