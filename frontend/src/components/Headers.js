import React from "react";
import { Navbar, Nav, Container } from "react-bootstrap";

function Headers() {
  return (
    <header>
      <Navbar bg="primary" variant="dark" expand="lg" collapseOnSelect>
        <Container>
          <Navbar.Brand href="#home">Social Distribution</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link href="/">Home</Nav.Link>
              <Nav.Link href="#myposts">MyPosts</Nav.Link>
              <Nav.Link href="login">Login</Nav.Link>
              <Nav.Link href="profile">Profile</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </header>
  );
}

export default Headers;
