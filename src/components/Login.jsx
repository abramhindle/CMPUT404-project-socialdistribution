import React, { Component } from "react";
import "../styles/Login.scss";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

class Login extends Component {
  constructor(props) {
    super(props);
    console.log("test");
  }

  render() {
    return (
      <Container fluid className="login">
        <Row>
          <Col md={7} className="login-description">
            Left
          </Col>
          <Col md={5} className="login-form">
            Right
          </Col>
        </Row>
      </Container>
    );
  }
}

export default Login;
