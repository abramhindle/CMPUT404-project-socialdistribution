import React, { Component } from "react";
import "../styles/register.css";

class Register extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: "",
      email: "",
      password: "",
      confirm: "",
    }
  }

  handleRegister = () => {
    const { username, email, password, confirm } = this.state;
    if (username && email && password && confirm) {
      console.log("username:", this.state.username);
      console.log("email:", this.state.email);
      console.log("password:", this.state.password);
      console.log("confirm:", this.state.confirm);
    } else {
      alert("fill in everything!")
    }

  }

  render() {
    const { username, email, password, confirm } = this.state;
    return (
      <div id="register-page">
        <h1 id="register-title">Register</h1>
        <input
          id="username"
          type="text"
          placeholder="USERNAME"
          value={username}
          onChange={(e) => this.setState({ username: e.target.value })}
        />
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
          onChange={(e => this.setState({ password: e.target.value }))}
        />
        <input
          id="confirm"
          type="password"
          placeholder="CONFIRM PASSWORD"
          value={confirm}
          onChange={(e) => this.setState({ confirm: e.target.value })}
        />
        <button id="register-btn" onClick={this.handleRegister}>Register</button>
      </div>
    )
  }
}

export default Register;
