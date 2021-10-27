import React, { useState } from "react";
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

function ProfilePage() {
  const [edit, setEdit] = useState(false);

  return (
    <Container className="App fluid min-vh-100 min-vw-100 d-flex flex-column p-0">
      <Headers />
      <Row className="flex-grow-1 m-0">
        <Col className="bg-secondary col-md-2 border">
          <SideBar />
        </Col>
        <Col className="justify-content-center">
          {edit ? <EditProfileContent /> : <ProfileContent />}
        </Col>
      </Row>
    </Container>
  );
}

export default ProfilePage;
