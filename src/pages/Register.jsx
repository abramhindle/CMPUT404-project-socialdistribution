import React, { Component } from "react";
import axios from "axios";
import "../styles/register.css";
import { setCurrentUser } from "../redux/user/actions"
import { connect } from "react-redux"

class Register extends Component {
  constructor(props) {
    super(props);
    this.state = {
      email: "",
      username: "",
      github: "",
      password: "",
      confirm: "",
    }
  }

  handleRegister = async () => {
    const { email, username, github, password, confirm } = this.state;
    if (email && username && github && password) {
      if (confirm === password) {
        console.log({ email, username, github, password });
        try {
          const doc = await axios.post("service/author/", { email, username, github, password });
          this.props.setCurrentUser(doc.data);

          window.location = "/";
        } catch (error) {
          console.log(error.message);
        }
      } else {
        alert("Password does not match");
      }

    } else {
      alert("Fill in Everything!");
    }
  }

  render() {
    const { username, email, password, github, confirm } = this.state;
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

        <input
          id="confirm"
          type="password"
          placeholder="CONFIRM"
          value={confirm}
          onChange={(e => this.setState({ confirm: e.target.value }))} />
        <button id="register-btn" onClick={this.handleRegister}>Register</button>
      </div>
    )
  }
}

const mapDispatchToProps = (dispatch) => ({
  setCurrentUser: (user) => {
    dispatch(setCurrentUser(user))
  }
})

export default connect(null, mapDispatchToProps)(Register);
