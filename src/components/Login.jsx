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
      password: ""
    };
  }

  handleInputChange = (event) => {
    this.setState({
      [event.target.name]: event.target.value,
    });
  }

  renderLoginForm() {
    return (
      <div className="login-random">
        <Row className="login-message">
          Login
        </Row>

        <input type="text" name="username" className="login-field" onChange={this.handleInputChange} />
        <input type="text" name="password" className="login-field" onChange={this.handleInputChange} />
      </div>
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
