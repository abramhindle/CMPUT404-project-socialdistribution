import React, { Component } from "react";
import "../styles/Login.scss";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

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
    const valid = this.validateForm();

    if (valid) {
      // TODO: send auth request here based on login/signup
      alert("Successful");
    }
  }

  toggleMethod = () => {
    // toggle between sign-up and sign-in screens
    this.setState({
      signup: !this.state.signup
    })
  }

  validateForm = () => {
    var error = "";

    // TODO: check with backend to see if the username exists
    const usernameExists = false;

    if (!this.state.username) {
      error = "Please fill in the username";
    } else if (!this.state.password) {
      error = "Please fill in the password";
    } else if (this.state.signup && !this.state.passwordReentry) {
      error = "Please confirm your password";
    } else if (usernameExists) {
      error = "Username Exists";
    } else if (this.state.signup && this.state.password != this.state.passwordReentry) {
      error = "Passwords don't match";
    } else if (this.state.password.length < 8) {
      // this is enforced by Django Auth so we need to check here
      error = "Password must be atleast 8 characters long";
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

        <input type="text" name="username" className="login-field" placeholder="Username" onChange={this.handleInputChange} />
        <input type="password" name="password" className="login-field" placeholder="Password" onChange={this.handleInputChange} />

        {
          this.state.signup ?
            <input type="password" name="passwordReentry" className="login-field" placeholder="Re-enter Password" onChange={this.handleInputChange} />
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
            Insert Picture Here
          </Col>
          <Col md={5} className="login-form">
            {this.renderForm()}
            {this.renderSecondaryOption()}
          </Col>
        </Row>
      </Container>
    );
  }
}

export default Login;
