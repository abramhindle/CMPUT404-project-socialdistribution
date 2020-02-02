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

    if (!this.validateForm()) { return };

    if (this.state.signup) {
      auth.registerUser(this.state.username, this.state.password).then((response) => {
        if (response.status === 201) {
          this.setState({
            signup: false,
            username: "",
            password: ""
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
      auth.loginUser(this.state.username, this.state.password).then((response) => {
        if (response.status === 200) {
          // TODO: success: redirect to homepage
          alert("Success")
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
    this.setState({
      signup: !this.state.signup,
      error: ""
    })
  }

  validateForm = () => {
    var error = "";

    if (!this.state.username) {
      error = "Please fill in the username";
    } else if (!this.state.password) {
      error = "Please fill in the password";
    } else if (this.state.signup) {
      if (!this.state.passwordReentry) {
        error = "Please confirm your password";
      } else if (this.state.password !== this.state.passwordReentry) {
        error = "Passwords don't match";
      } else if (this.state.password.length < 8) {
        // this is enforced by Django Auth so we need to check here
        error = "Password must be atleast 8 characters long";
      }
    }

    this.setState({
      error: error,
    });
    
    return !Boolean(error);
  }
  

  renderForm() {
    let formMessage = "Let's Get Started!";
    let primaryButtonText = "Sign up";
    if (!this.state.signup) {
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
          value={this.state.username} 
          autoFocus />

        <input 
          type="password" 
          name="password" 
          className="login-field" 
          placeholder="Password" 
          onChange={this.handleInputChange} 
          value={this.state.password} />

        {
          this.state.signup ?
            <input 
              type="password" 
              name="passwordReentry" 
              className="login-field" 
              placeholder="Re-enter Password" 
              onChange={this.handleInputChange} 
              value={this.state.passwordReentry} />
          : null
        }

        <span className="login-error-message">{this.state.error}</span>
        <button className="login-button" type="submit">{primaryButtonText}</button>
      </form>
    );
  }

  renderSecondaryOption() {
    let secondaryOptionText = "Already have account?";
    let secondaryButtonText = "Sign in";
    if (!this.state.signup) {
      secondaryOptionText = "Don't have an account?";
      secondaryButtonText = "Sign up";
    }

    return(
      <div className="login-secondary-options">
        <span className="login-secondary-options-text">{secondaryOptionText}</span>

        <button className="login-secondary-button" type="submit" onClick={this.toggleMethod}>{secondaryButtonText}</button>
      </div>
    )
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
              <img className="cover-image" src={cover} width="70%" />
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
