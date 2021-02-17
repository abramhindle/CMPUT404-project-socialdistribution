import React, { Component } from 'react';
import '../styles/navbar.css'

class Navbar extends Component {
  render() {
    return (
      <nav id="navbar">
        <h1 id="navbar-title"> <a href="/">Social Distribution</a> </h1>
        <ul>
          <li id="nav-item-1"> <a href="/register">Sign up</a> </li>
          <li id="nav-item-2"> <a href="/login">Log in</a> </li>
          <li id="nav-item-3"> <a href="/me">Me</a> </li>
        </ul>
      </nav>
    )
  }
}

export default Navbar;