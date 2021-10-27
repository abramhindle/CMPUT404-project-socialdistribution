import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Container, Row, Col, Button, Image, Alert, Stack } from "react-bootstrap";
import Headers from "../components/Headers";
import SideBar from "../components/SideBar";
import Avatar from "../images/avatar.jpg";
import EditIcon from "../images/edit.png";
import {LinkContainer} from "react-router-bootstrap";
import { useHistory } from "react-router-dom";

function ProfilePage() {
  let history = useHistory();

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  useEffect(() => {
    // redirect user to homepage if user is not logged in
    if (!userInfo) {
      history.push("/login");
    }
  }, [history, userInfo]);

  return (
    <Container className="App fluid min-vh-100 min-vw-100 d-flex flex-column p-0">
      <Headers />
      <Row className="flex-grow-1 m-0">
        <Col className="bg-secondary col-md-2 border">
          <SideBar />
        </Col>
        <Col className="justify-content-center">
            <Stack gap={3} style={{marginTop:"7%", marginLeft:"40%"}}>
                <Image src={Avatar} width="20%" height="15%"></Image>
                <Alert style={{marginLeft:"-13%", width:"50%"}}>I'm username</Alert>
                <Alert style={{marginLeft:"-13%", width:"50%"}}>I'm email</Alert>
                <Alert style={{marginLeft:"-13%", width:"50%"}}>I'm Github url</Alert>

                <LinkContainer to="/changeprofile" style={{marginRight:"80%",backgroundColor:"orange"}}>
                  <Button>
                    <img src={EditIcon} style={{width:"20px"}}></img>
                  </Button>
                </LinkContainer>
                
            </Stack>
        </Col>
      </Row>
    </Container>
  );
}

export default ProfilePage;