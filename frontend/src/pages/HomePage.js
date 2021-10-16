import React from "react";

import { Container, Row, Col } from "react-bootstrap";
import Headers from "../components/Headers";
import SideBar from "../components/SideBar";

function HomePage() {
  return (
    <Container className="App fluid min-vh-100 min-vw-100 d-flex flex-column p-0">
      <Headers />
      <Row className="flex-grow-1 m-0">
        <Col className="bg-secondary col-md-2 border">
          <SideBar />
        </Col>
        <Col>
          {/*  replace Hello World with homepage material*/}
          <h1>Hello World</h1>
        </Col>
      </Row>
    </Container>
  );
}

export default HomePage;
