import React, { Component } from 'react';
import '../styles/navbar.css'

class Navbar extends Component {
  render() {
    return (
      <nav id="navbar">
        <h1> <a href="/">Social Distribution</a> </h1>
        <ul>
          <li > <a href="/">Sign up</a> </li>
          <li > <a href="/">Log in</a> </li>
          <li> <a href="/">My post</a> </li>
        </ul>
      </nav>
    )
  }
}

export default Navbar;