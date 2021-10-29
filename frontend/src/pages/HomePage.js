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
    <div>
      <Headers />
      <Row className="m-0">
        <Col className="bg-secondary col-md-2 border">
          <SideBar />
        </Col>
        <Col md={10} className="justify-content-center">
          <HomeContent />
        </Col>
      </Row>
    </div>
  );
}

export default HomePage;
