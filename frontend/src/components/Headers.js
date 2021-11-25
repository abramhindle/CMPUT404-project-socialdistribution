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
  Alert,
  FloatingLabel,
} from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { logout } from "../actions/userActions";
import searchicon from "../images/search.png";
import { Link } from "react-router-dom";
import { unstable_renderSubtreeIntoContainer } from "react-dom/cjs/react-dom.development";

function Headers(props) {
  const dispatch = useDispatch();

  const [searchContent, setSearchContent] = useState(" ");
  const [searchCategory, setSearchCategory] = useState(
    props.searchCategory ? props.searchCategory : "post"
  );

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

          <Nav className="d-flex flex-grow-1 justify-content-center">
            <Col md={6} className="m-1">
              <Form.Control
                id="inlineFormInput"
                placeholder=""
                onChange={(e) => {
                  setSearchContent(e.target.value);
                }}
              />
            </Col>

            <Form
              id="category"
              className="m-1"
              onChange={(e) => setSearchCategory(e.target.value)}
            >
              <Form.Select
                defaultValue={searchCategory ? searchCategory : "post"}
              >
                <option value="post">Post</option>
                <option value="user">User</option>
              </Form.Select>
            </Form>

            <LinkContainer
              className="m-1"
              to={
                searchCategory == "user"
                  ? "/searchuser/" + searchContent
                  : "/searchresult/" + searchContent
              }
              style={{ backgroundColor: "orange" }}
            >
              <Button type="submit">Search</Button>
            </LinkContainer>
          </Nav>

          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav" className="flex-grow-0">
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
