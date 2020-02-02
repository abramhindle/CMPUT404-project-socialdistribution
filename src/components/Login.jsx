import React, { Component } from "react";
import "../styles/Login.scss";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import * as auth from "../services/Authentication";
import cover from "../images/cover.svg";

class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      signup: true,
      error: "",
      username: "",
      password: "",
      passwordReentry: "",
    };
  }

  handleInputChange = (event) => {
    this.setState({
      [event.target.name]: event.target.value,
    });
  }

  handleFormSubmit = (event) => {
    event.preventDefault();

    if (!this.validateForm()) { return; }

    const { signup, username, password } = this.state;

    if (signup) {
      auth.registerUser(username, password).then((response) => {
        if (response.status === 201) {
          this.setState({
            signup: false,
            username: "",
            password: "",
          });
        }
      }).catch((err) => {
        let error = err.response.data;
        error = error.username || error.password1 || error.password2;
        this.setState({
          error: error ? error[0] : "Something went wrong",
        });
      });
    } else {
      auth.loginUser(username, password).then((response) => {
        if (response.status === 200) {
          // TODO: success: redirect to homepage
          // eslint-disable-next-line no-alert
          alert("Success");
        }
      }).catch(() => {
        this.setState({
          error: "Username or Password are incorrect",
        });
      });
    }
  }

  toggleMethod = () => {
    // toggle between sign-up and sign-in screens
    const { signup } = this.state;

    this.setState({
      signup: !signup,
      error: "",
    });
  }

  validateForm = () => {
    const {
      signup, username, password, passwordReentry,
    } = this.state;

    let error = "";
    if (!username) {
      error = "Please fill in the username";
    } else if (!password) {
      error = "Please fill in the password";
    } else if (signup) {
      if (!passwordReentry) {
        error = "Please confirm your password";
      } else if (password !== passwordReentry) {
        error = "Passwords don't match";
      } else if (password.length < 8) {
        // this is enforced by Django Auth so we need to check here
        error = "Password must be atleast 8 characters long";
      }
    }

    this.setState({
      error,
    });

    return !error;
  }

  renderForm() {
    const {
      signup, username, password, passwordReentry, error,
    } = this.state;

    let formMessage = "Let's Get Started!";
    let primaryButtonText = "Sign up";
    if (!signup) {
      formMessage = "Welcome Back!";
      primaryButtonText = "Sign in";
    }

    return (
      <form onSubmit={this.handleFormSubmit}>
        <div className="login-message">
          {formMessage}
        </div>

        <input
          type="text"
          name="username"
          className="login-field"
          placeholder="Username"
          onChange={this.handleInputChange}
          value={username}
        />

        <input
          type="password"
          name="password"
          className="login-field"
          placeholder="Password"
          onChange={this.handleInputChange}
          value={password}
        />

        {
          signup ? (
            <input
              type="password"
              name="passwordReentry"
              className="login-field"
              placeholder="Re-enter Password"
              onChange={this.handleInputChange}
              value={passwordReentry}
            />
          )
            : null
        }

        <span className="login-error-message">{error}</span>
        <button className="login-button" type="submit">{primaryButtonText}</button>
      </form>
    );
  }

  renderSecondaryOption() {
    const { signup } = this.state;

    let secondaryOptionText = "Already have account?";
    let secondaryButtonText = "Sign in";
    if (!signup) {
      secondaryOptionText = "Don't have an account?";
      secondaryButtonText = "Sign up";
    }

    return (
      <div className="login-secondary-options">
        <span className="login-secondary-options-text">{secondaryOptionText}</span>
        <button className="login-secondary-button" type="submit" onClick={this.toggleMethod}>{secondaryButtonText}</button>
      </div>
    );
  }

  render() {
    return (
      <Container fluid className="login">
        <Row>
          <Col md={7} className="login-description">
            <div className="login-heading">
              App Name
            </div>
            <div className="cover-image-wrapper">
              <img className="cover-image" src={cover} width="70%" alt="cover" />
            </div>
          </Col>
          <Col md={5} className="login-form-wrapper">
            {this.renderForm()}
            {this.renderSecondaryOption()}
          </Col>
        </Row>
      </Container>
    );
  }
}

export default Login;
