import React, { useState, useEffect } from "react";
import {
  Navbar,
  Nav,
  Container,
  Form,
  Button,
  Row,
  Col,
  Image,
} from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { logout } from "../actions/userActions";
import searchicon from "../images/search.png";

function Headers() {
  const dispatch = useDispatch();

  const [searchContent, setSearchContent] = useState(" ");

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  const logoutHandler = () => {
    dispatch(logout());
  };

  return (
    <header>
      <Navbar bg="primary" variant="dark" expand="lg" collapseOnSelect>
        <Container>
          <LinkContainer to="/">
            <Navbar.Brand>Social Distribution</Navbar.Brand>
          </LinkContainer>

          <Col md={8} className="m-1">
            <Form.Control
              id="inlineFormInput"
              placeholder="Search a post"
              onChange={(e) => setSearchContent(e.target.value)}
            />
          </Col>
          <Col className="m-1">
            <LinkContainer
              to="/searchresult"
              style={{ backgroundColor: "orange" }}
            >
              <Button>Search</Button>
            </LinkContainer>
          </Col>

          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ms-auto">
              <LinkContainer to="/profile">
                <Nav.Link>Profile</Nav.Link>
              </LinkContainer>
              {userInfo ? (
                <Nav.Link onClick={logoutHandler}>Logout</Nav.Link>
              ) : (
                <LinkContainer to="/login">
                  <Nav.Link>Login</Nav.Link>
                </LinkContainer>
              )}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </header>
  );
}

export default Headers;
