import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Container, Row, Col } from "react-bootstrap";
import Headers from "../components/Headers";
import SideBar from "../components/SideBar";
import PostForm from "../components/PostForm";

import { useHistory } from "react-router-dom";

function PostPage() {
  let history = useHistory();

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  useEffect(() => {
    // redirect user to homepage if user is not logged in
    if (!userInfo) {
      history.push("/");
    }
  }, [history, userInfo]);

  return (
    <Container className="App fluid min-vh-100 min-vw-100 d-flex flex-column p-0">
      <Headers />
      <Row className="flex-grow-1 m-0">
        <Col className="bg-secondary col-md-2 border">
          <SideBar />
        </Col>
        <Col>
          <PostForm />
        </Col>
      </Row>
    </Container>
  );
}

export default PostPage;
