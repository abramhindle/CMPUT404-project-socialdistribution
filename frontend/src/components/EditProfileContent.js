import React from "react";
import { Alert, Row, Col, Form, Button, Image, Nav } from "react-bootstrap";
import Avatar from "../images/avatar.jpg";
import EditIcon from "../images/edit.png";
import { LinkContainer } from "react-router-bootstrap";

function EditProfileContent() {
  return (
    <div className="m-5">
      <Row className="justify-content-between">
        <Col md={8}>
          <Row className="justify-content-between">
            <Col md={6}>
              <Image src={Avatar} width="100%" className="mb-3" />
            </Col>
          </Row>

          <Form>
            <Alert className="my-3">Username: I'm username</Alert>

            <Form.Group className="my-1" controlId="formBasicEmail">
              <Form.Label>Display Name</Form.Label>
              <Form.Control type="displayname" placeholder="Display Name" />
            </Form.Group>

            <Form.Group className="my-1" controlId="formBasicUsername">
              <Form.Label>Github url</Form.Label>
              <Form.Control type="githuburl" placeholder="GitHub URL" />
            </Form.Group>
          </Form>
          <Row className="m-3">
            <Col className="d-flex justify-content-center">
              <LinkContainer
                to="/profile"
                style={{ backgroundColor: "orange" }}
              >
                <Button>Save</Button>
              </LinkContainer>
            </Col>
            <Col className="d-flex justify-content-center">
              <LinkContainer to="/profile">
                <Button>Cancel</Button>
              </LinkContainer>
            </Col>
          </Row>
        </Col>
      </Row>
    </div>
  );
}

export default EditProfileContent;
