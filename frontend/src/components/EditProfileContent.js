import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Alert, Row, Col, Form, Button, Image, Nav } from "react-bootstrap";
import Avatar from "../images/avatar.jpg";
import { LinkContainer } from "react-router-bootstrap";
import Message from "../components/Message";
import { editAuthorDetail, editReset } from "../actions/userActions";
import { useHistory } from "react-router-dom";

function EditProfileContent() {
  const [displayname, setDisplayname] = useState("");
  const [github, setGithub] = useState("");

  const [message, setMessage] = useState("");

  const dispatch = useDispatch();

  const userDetailEdit = useSelector((state) => state.userDetailEdit);
  const { error, loading, userInfo } = userDetailEdit;

  const submitHandler = (e) => {
    e.preventDefault();
    if (displayname == "") {
      setMessage("Display name can't be empty.");
    } else {
      console.log(displayname, github);
      dispatch(editAuthorDetail(displayname, github));
    }
  };

  let history = useHistory();

  useEffect(() => {
    // redirect user to profile if edit is successful
    if (userInfo) {
      history.push("/profile");
      window.location.reload();
      dispatch(editReset());
    }
  }, [history, dispatch, userInfo]);

  return (
    <div className="m-5">
      {message && <Message variant="danger">{message}</Message>}
      {error && <Message variant="danger">{error}</Message>}
      <Row className="justify-content-between">
        <Col md={8}>
          <Row className="justify-content-between">
            <Col md={6}>
              <Image src={Avatar} width="100%" className="mb-3" />
            </Col>
          </Row>

          <Form onSubmit={submitHandler}>
            <Form.Group className="my-1" controlId="formBasicEmail">
              <Form.Label>Display Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Display Name"
                onChange={(e) => setDisplayname(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="my-1" controlId="formBasicUsername">
              <Form.Label>Github url</Form.Label>
              <Form.Control
                type="url"
                placeholder="GitHub URL"
                onChange={(e) => setGithub(e.target.value)}
              />
            </Form.Group>
            <Row className="m-3">
              <Col className="d-flex justify-content-center">
                <Button type="submit" style={{ backgroundColor: "orange" }}>
                  Save
                </Button>
              </Col>
              <Col className="d-flex justify-content-center">
                <LinkContainer to="/profile">
                  <Button>Cancel</Button>
                </LinkContainer>
              </Col>
            </Row>
          </Form>
        </Col>
      </Row>
    </div>
  );
}

export default EditProfileContent;
