import React from "react";
import {
  Container,
  Row,
  Col,
  Button,
  Image,
  Alert,
  Stack,
  Nav,
  Form,
} from "react-bootstrap";
import Headers from "../components/Headers";
import SideBar from "../components/SideBar";
import Avatar from "../images/avatar.jpg";
import { LinkContainer } from "react-router-bootstrap";

function ChangeProfilePage() {
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
            <Form style={{ marginLeft: "-13%", width: "50%" }}>
              <Form.Group className="mb-3" controlId="formBasicUsername">
                <Form.Label>Username</Form.Label>
                <Form.Control
                  type="username"
                  placeholder="This is the original username"
                />
              </Form.Group>

              <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Email</Form.Label>
                <Form.Control
                  type="email"
                  placeholder="This is the original email"
                />
              </Form.Group>

              <Form.Group className="mb-3" controlId="formBasicUsername">
                <Form.Label>Github url</Form.Label>
                <Form.Control
                  type="githuburl"
                  placeholder="This is the original Github url"
                />
              </Form.Group>
            </Form>

            <Stack
              gap={5}
              direction="horizontal"
              style={{ marginLeft: "-4%", marginTop: "-3%" }}
            >
              <LinkContainer
                to="/profile"
                style={{
                  width: "7%",
                  height: "10%",
                  marginTop: "3%",
                  marginRight: "3%",
                }}
              >
                <Nav.Link>
                  <Button style={{ backgroundColor: "orange", width: "" }}>
                    Save
                  </Button>
                </Nav.Link>
              </LinkContainer>

              <LinkContainer
                to="/profile"
                style={{ width: "7%", height: "10%", marginTop: "3%" }}
              >
                <Nav.Link>
                  <Button style={{ backgroundColor: "black", width: "" }}>
                    Cancel
                  </Button>
                </Nav.Link>
              </LinkContainer>
            </Stack>
          </Stack>
        </Col>
      </Row>
    </Container>
  );
}

export default ChangeProfilePage;
