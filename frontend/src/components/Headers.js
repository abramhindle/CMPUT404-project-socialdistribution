import React from "react";
import { Navbar, Nav, Container } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { logout } from "../actions/userActions";

function Headers() {
  const dispatch = useDispatch();

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  const logoutHandler = () => {
    dispatch(logout());
  };

  return (
    <header>
      <Navbar bg="primary" variant="dark" expand="lg" collapseOnSelect>
        <Container>
          <Navbar.Brand href="/">Social Distribution</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ms-auto">
              <Nav.Item>
                <Nav.Link href="#link">Link</Nav.Link>
              </Nav.Item>
              {userInfo ? (
                <Nav.Link onClick={logoutHandler}>Logout</Nav.Link>
              ) : (
                <Nav.Link href="login">Login</Nav.Link>
              )}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </header>
  );
}

export default Headers;
