import React, { Component } from "react";
import "../styles/register.css";

class Register extends Component {
  constructor(props) {
    super(props);
    this.state = {
      email: "",
      username: "",
      github: "",
      password: "",
    }
  }

  handleRegister = () => {
    const { email, username, github, password } = this.state;
    if (email && username && github && password) {
      console.log({ email, username, github, password });
    } else {
      alert("Fill in Everything!");
    }

    // try {
    //    await axios.post("/service/author", { email, username, github, password })
    // } catch (error) {
    //   console.log(error.message);
    // }
  }

  render() {
    const { username, email, password, github, } = this.state;
    return (
      <div id="register-page">
        <h1 id="register-title">Register</h1>
        <input
          id="email"
          type="email"
          placeholder="EMAIL"
          value={email}
          onChange={(e) => this.setState({ email: e.target.value })} />

        <input
          id="username"
          type="text"
          placeholder="USERNAME"
          value={username}
          onChange={(e) => this.setState({ username: e.target.value })} />


        <input
          id="github"
          type="text"
          placeholder="GITHUB"
          value={github}
          onChange={(e) => this.setState({ github: e.target.value })} />

        <input
          id="password"
          type="password"
          placeholder="PASSWORD"
          value={password}
          onChange={(e => this.setState({ password: e.target.value }))} />
        <button id="register-btn" onClick={this.handleRegister}>Register</button>
      </div>
    )
  }
}

export default Register;
