import React, { Component } from 'react';

class Navbar extends Component {
  render() {
    return (

      <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
        <div className="container-fluid">
          <a className="navbar-brand" href="/">Social Distribution</a>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div className="navbar-nav">
              <a className="nav-link" href="/">Login</a>
              <a className="nav-link" href="/">Register</a>
            </div>
          </div>
        </div>
      </nav>

    )
  }
}

export default Navbar;