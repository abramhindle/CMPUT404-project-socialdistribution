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
    // TODO: send auth request here based on login/signup
    console.log("Submit");
  }

  toggleMethod = () => {
    // toggle between sign-up and sign-in screens
    this.setState({
      signup: !this.state.signup
    })
  }
  

  renderForm() {
    const primaryButtonText = this.state.signup ? "Sign up" : "Sign in";

    return (
      <form onSubmit={this.handleFormSubmit}>
        <div className="login-message">
          {
            this.state.signup ?
              "Let's Get Started!"
            : "Welcome Back!"
          }
        </div>

        <input type="text" name="username" className="login-field" placeholder="Username" onChange={this.handleInputChange} />
        <input type="password" name="password" className="login-field" placeholder="Password" onChange={this.handleInputChange} />

        {
          this.state.signup ?
            <input type="password" name="passwordReentry" className="login-field" placeholder="Re-enter Password" onChange={this.handleInputChange} />
          : null
        }

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
            Left
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
