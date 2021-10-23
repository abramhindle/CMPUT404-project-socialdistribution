import React from "react";

import { Container, Row, Col } from "react-bootstrap";
import Headers from "../components/Headers";
import SideBar from "../components/SideBar";
import HomePost from "../components/HomePost";

function HomePage() {
  return (
    <Container className="App fluid min-vh-100 min-vw-100 d-flex flex-column p-0">
      <Headers />
      <Row className="flex-grow-1 m-0">
        <Col className="bg-secondary col-md-2 border">
          <SideBar />
        </Col>
        <Col>
          <HomePost />
        </Col>
      </Row>
    </Container>
  );
}

export default HomePage;
