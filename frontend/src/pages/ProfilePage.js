import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useHistory } from "react-router-dom";
import {
  Container,
  Row,
  Col,
  Button,
  Image,
  Alert,
  Stack,
} from "react-bootstrap";
import Headers from "../components/Headers";
import SideBar from "../components/SideBar";
import { LinkContainer } from "react-router-bootstrap";
import ProfileContent from "../components/ProfileContent";
import EditProfileContent from "../components/EditProfileContent";

function ProfilePage(props) {
  let history = useHistory();

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  useEffect(() => {
    // redirect user to homepage if user is not logged in
    if (!userInfo) {
      history.push("/login");
    }
  }, [history, userInfo]);

  const view_user_id = props.match.params.id;

  return (
    <Container className="App fluid min-vh-100 min-vw-100 d-flex flex-column p-0">
      <Headers />
      <Row className="flex-grow-1 m-0">
        <Col className="bg-secondary col-md-2 border">
          <SideBar />
        </Col>
        <Col className="justify-content-center">
          <ProfileContent view_user_id={view_user_id}/>
        </Col>
      </Row>
    </Container>
  );
}

export default ProfilePage;
