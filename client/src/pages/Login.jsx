import axios from "axios";
import React, { Component } from "react";
import "../styles/login.css";
import { setCurrentUser } from '../redux/user/actions';
import { connect } from 'react-redux'

class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      email: "",
      password: "",
    }
  }

  handleLogin = async () => {
    const { email, password } = this.state;
    if (email && password) {
      console.log({ email, password });
    } else {
      alert("Email and Password Cannot be Empty!")
    }

    try {
      const doc = await axios.post("service/author/login/", { email, password });
      console.log("doc:", doc.data);
      this.props.setCurrentUser(doc.data);
    } catch (error) {
      console.log(error.message);
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

const mapDispatchToProps = (dispatch) => ({
  setCurrentUser: (user) => {
    dispatch(setCurrentUser(user))
  }
})

export default connect(null, mapDispatchToProps)(Login);