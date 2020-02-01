import React, { Component } from "react";
import "../styles/Login.scss";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
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
  

  renderForm() {
    return (
      <form onSubmit={this.handleFormSubmit}>
        <div className="login-message">
          Let's Get Started
        </div>

        <input type="text" name="username" className="login-field" placeholder="Username" onChange={this.handleInputChange} />
        <input type="password" name="password" className="login-field" placeholder="Password" onChange={this.handleInputChange} />
        <input type="password" name="passwordReentry" className="login-field" placeholder="Re-enter Password" onChange={this.handleInputChange} />

        <button className="login-button" type="submit">Sign up</button>
      </form>
    );
  }

  renderSecondaryOption() {
    return(
      <div className="login-secondary-options">
        <span className="login-secondary-options-text"> Already have an account?</span>

        <button className="login-secondary-button" type="submit">Sign in</button>
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
