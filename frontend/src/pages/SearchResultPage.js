import React, { useState, useEffect } from "react";
import { Container, Row, Col, Button, Form, Stack, Alert } from "react-bootstrap";
import Headers from "../components/Headers";
import SideBar from "../components/SideBar";
import searchicon from "../images/search.png";
import { useDispatch, useSelector } from "react-redux";
import { LinkContainer } from "react-router-bootstrap";
import SearchResultItem from "../components/SearchResults";

const SearchResultPage = (props) => {

  const results = [
    {title:"I'm the first result", author: "Author1", textContent:"test"},
    {title:"I'm the second result", author: "Author2", textContent:"test"},
  ]
  var resultList = []
  for(let item of results){
    resultList.push(<SearchResultItem item={item}/>)
  }

  return (
    <Container className="App fluid min-vh-100 min-vw-100 d-flex flex-column p-0">
      <Headers />
      <Row className="flex-grow-1 m-0">
        <Col className="bg-secondary col-md-2 border">
          <SideBar />
        </Col>
        <Col>
                <div>
                <Alert className="m-1" variant="info">
                    Search Results
                </Alert>    
                </div>
                {resultList}
        </Col>
        

      </Row>
    </Container>
  );
}

export default SearchResultPage;
