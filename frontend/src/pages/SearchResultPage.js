import React, { useState, useEffect } from "react";
import { Container, Row, Col, Button, Form, Stack } from "react-bootstrap";
import Headers from "../components/Headers";
import SideBar from "../components/SideBar";
import searchicon from "../images/search.png";
import { useDispatch, useSelector } from "react-redux";
import { LinkContainer } from "react-router-bootstrap";

const SearchResultPage = (props) => {

  alert("you searched " + props.location.searchContent);

  return (
    <Container className="App fluid min-vh-100 min-vw-100 d-flex flex-column p-0">
      <Headers />
      <Row className="flex-grow-1 m-0">
        <Col className="bg-secondary col-md-2 border">
          <SideBar />
        </Col>
        

      </Row>
    </Container>
  );
}

export default SearchResultPage;
