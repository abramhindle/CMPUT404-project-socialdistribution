import React, { useState, useEffect } from "react";
import { Container, Row, Col, Button } from "react-bootstrap";
import Headers from "../components/Headers";
import SideBar from "../components/SideBar";
import HomeContent from "../components/HomeContent";
import { Link } from "react-router-dom";

import { useDispatch, useSelector } from "react-redux";

function HomePage() {
  const dispatch = useDispatch();

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  return (
    <Container className="App fluid min-vh-100 min-vw-100 d-flex flex-column p-0">
      <Headers />
      <Row className="flex-grow-1 m-0">
        <Col className="bg-secondary col-md-2 border">
          <SideBar />
        </Col>
        <Col className="justify-content-center">
          <HomeContent />
        </Col>
        <Col md={2} className="text-center mt-5">
          {userInfo ? (
            <Link to="/post">
              <Button variant="primary">Make Post</Button>
            </Link>
          ) : (
            ""
          )}
        </Col>
      </Row>
    </Container>
  );
}

export default HomePage;
