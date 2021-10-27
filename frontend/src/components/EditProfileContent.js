import React from "react";
import { Container, Row, Col, Form, Button, Image, Nav } from "react-bootstrap";
import Avatar from "../images/avatar.jpg";
import EditIcon from "../images/edit.png";
import { LinkContainer } from "react-router-bootstrap";

function EditProfileContent() {
  return (
    <div>
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
          <Form.Control type="email" placeholder="This is the original email" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicUsername">
          <Form.Label>Github url</Form.Label>
          <Form.Control
            type="githuburl"
            placeholder="This is the original Github url"
          />
        </Form.Group>
      </Form>
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
          <Button style={{ backgroundColor: "orange", width: "" }}>Save</Button>
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
    </div>
  );
}

export default EditProfileContent;
