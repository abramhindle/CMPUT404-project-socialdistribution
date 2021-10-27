import React,{Component} from "react";
import { Card, Button, Row, Col, DropdownButton, Dropdown} from "react-bootstrap";
import Avatar from "../images/avatar.jpg";

// return list of posts within card filtered with parameter (category)
function Posts(){
  return (
    <div className="m-5">
      <Card>
        <Card.Body>
          <div className="d-flex">
            <Card.Img
              className="m-1"
              src={Avatar} 
              style={{ width: "6rem", height: "6rem" }}
            />
            <Card.Title className="m-2 justify-content-center">
              BlahX
            </Card.Title>
            <Card.Title className="my-2 text-muted">@BlahX</Card.Title>
            <DropdownButton className="ms-auto mx-1" id="bg-vertical-dropdown-1">
              <Dropdown.Item eventKey="1">Edit</Dropdown.Item>
              <Dropdown.Item eventKey="2">Delete</Dropdown.Item>
            </DropdownButton>
          </div>
          <Card.Title className="m-3">Title</Card.Title>
          <Card.Text className="m-3">
            Some quick example text to build on the card title and make up the
            bulk of the card's content. asdfhuisdhfuasdhiudshuidshdsuishduhfdui
            sadfhiuasdhfdoiushfaios
          </Card.Text>
          <Row className="justify-content-between m-1">
            <Col className="d-flex align-items-center">
              Likes: 10&nbsp; &nbsp; &nbsp; Comments: 200
            </Col>
            <Col className="text-end">
              <Button
                className="m-1"
                style={{ width: "7rem" }}
                variant="success"
              >
                Like
              </Button>
              <Button className="m-1" style={{ width: "7rem" }} variant="info">
                Comment
              </Button>
              <Button
                className="m-1"
                style={{ width: "7rem" }}
                variant="warning"
              >
                Share
              </Button>
            </Col>
          </Row>
        </Card.Body>
      </Card>
    </div>
  );
}

export default Posts;
