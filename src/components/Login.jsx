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

  renderLoginForm() {
    return (
      <form>
        <div className="login-message">
          Let's Get Started
        </div>

        <input type="text" name="username" className="login-field" placeholder="Username" onChange={this.handleInputChange} />
        <input type="password" name="password" className="login-field" placeholder="Password" onChange={this.handleInputChange} />
        <input type="password" name="passwordReentry" className="login-field" placeholder="Re-enter Password" onChange={this.handleInputChange} />

        <button className="login-signup-button" type="submit">Sign up</button>
      </form>
    );
  }

  render() {
    return (
      <Container fluid className="login">
        <Row>
          <Col md={7} className="login-description">
            Left
          </Col>
          <Col md={5} className="login-form">
            {this.renderLoginForm()}
          </Col>
        </Row>
      </Container>
    );
  }
}

export default Login;
