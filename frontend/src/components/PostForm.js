import React from "react";
import { Form, Button } from "react-bootstrap";

function PostForm() {
  return (
    <div>
      <Form className="justfiy-content-center align-center">
        <Form.Group className="m-3" controlId="title">
          <Form.Label>Title</Form.Label>
          <Form.Control type="title" placeholder="Title here" />
        </Form.Group>
        <Form.Group className="m-3" controlId="description">
          <Form.Label>Description</Form.Label>
          <Form.Control as="textarea" rows={5} />
        </Form.Group>
        <div className="d-flex align-items-end justify-content-end px-5">
          <Button className="btn" type="submit" variant="primary">
            Submit
          </Button>
        </div>
      </Form>
    </div>
  );
}

export default PostForm;
