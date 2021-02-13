import React, { Component } from "react";
import "../styles/login.css";

class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      email: "",
      password: "",
    }
  }

  handleLogin = () => {
    const { email, password } = this.state;
    if (email && password) {
      console.log("email:", this.state.email);
      console.log("password:", this.state.password);
    } else {
      alert("cannot be empty!")
    }

  }

  render() {
    const { email, password } = this.state;
    return (
      <div id="login-page">
        <h1 id="login-title">Login</h1>
        <input
          id="email"
          type="email"
          placeholder="EMAIL"
          value={email}
          onChange={(e) => this.setState({ email: e.target.value })}
        />
        <input
          id="password"
          type="password"
          placeholder="PASSWORD"
          value={password}
          onChange={(e) => this.setState({ password: e.target.value })}
        />
        <button id="login-btn" onClick={this.handleLogin}>Login</button>
      </div>
    )
  }
}

export default Login;