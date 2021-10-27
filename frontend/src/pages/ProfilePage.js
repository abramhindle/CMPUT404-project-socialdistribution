import React from "react";
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
import Avatar from "../images/avatar.jpg";
import EditIcon from "../images/edit.png";
import { LinkContainer } from "react-router-bootstrap";

function ProfilePage() {
  return (
    <Container className="App fluid min-vh-100 min-vw-100 d-flex flex-column p-0">
      <Headers />
      <Row className="flex-grow-1 m-0">
        <Col className="bg-secondary col-md-2 border">
          <SideBar />
        </Col>
        <Col className="justify-content-center">
          <Stack gap={3} style={{ marginTop: "7%", marginLeft: "40%" }}>
            <Image src={Avatar} width="20%" height="15%"></Image>
            <Alert style={{ marginLeft: "-13%", width: "50%" }}>
              Username: I'm username
            </Alert>
            <Alert style={{ marginLeft: "-13%", width: "50%" }}>
              Display Name: I'm email
            </Alert>
            <Alert style={{ marginLeft: "-13%", width: "50%" }}>
              Github: I'm Github url
            </Alert>

            <LinkContainer
              to="/changeprofile"
              style={{
                marginLeft: "90%",
                marginTop: "10%",
                backgroundColor: "orange",
              }}
            >
              <Button>
                <img src={EditIcon} style={{ width: "20px" }}></img>
              </Button>
            </LinkContainer>
          </Stack>
        </Col>
      </Row>
    </Container>
  );
}

export default ProfilePage;
