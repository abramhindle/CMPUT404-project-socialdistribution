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
import Avatar from "../images/avatar.jpg";
import EditIcon from "../images/edit.png";
import { LinkContainer } from "react-router-bootstrap";

function ProfileContent() {
  return (
    <div className="m-5">
      <Row className="justify-content-between">
        <Col md={8}>
          <Row className="justify-content-between">
            <Col md={6}>
              <Image src={Avatar} width="100%" className="my-5" />
            </Col>
            <Col md={2} className="d-flex flex-column mt-auto">
              {/* visible if it's ur own profile */}
              <Button
                className="p-2 my-5"
                style={{ backgroundColor: "orange" }}
              >
                <Image src={EditIcon} width="50%" />
              </Button>
            </Col>
          </Row>
          <Alert>Username: I'm username</Alert>
          <Alert>Display Name: I'm email</Alert>
          <Alert>Github: I'm Github url</Alert>
        </Col>
        <Col md={2}>
          {/* neither following */}
          <Button className="m-2">Add Friend</Button>
          {/* visibile when following or friends */}
          <Button className="m-2" variant="success">
            Following
          </Button>
          <Button className="m-2" variant="danger">
            Unfollow
          </Button>
          {/* visibile when incoming friend request */}
          <Button className="m-2" variant="success">
            Accept Friend Request
          </Button>
          <Button className="m-2" variant="danger">
            Decline Friend Request
          </Button>
        </Col>
      </Row>
    </div>
  );
}

export default ProfileContent;
