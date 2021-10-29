import React, { useState, useEffect } from "react";
import {
  Card,
  Button,
  Row,
  Col,
  DropdownButton,
  Dropdown,
  Form,
  ListGroup,
  ListGroupItem,
} from "react-bootstrap";
import Avatar from "../images/avatar.jpg";
import { useDispatch, useSelector } from "react-redux";
import { deletePost } from "../actions/postActions";
import Message from "../components/Message";

// return list of posts within card filtered with parameter (category)
function Posts(prop) {
  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  const [like, setLike] = useState({ isLike: false, amount: 10 });
  const [comment, setComment] = useState(false);
  const [share, setShare] = useState(false);

  const commentPost = () => {
    if (!comment) {
      setComment(true);
    } else {
      setComment(false);
    }
  };
  const sharePost = () => {
    if (/*your didn't share/create this post &&*/ !share) {
      setShare(true);
      // add a new Post to db
    }
  };

  var post_author_id = "";
  var post_id = "";
  // parse prop.post.id to get author id and post id
  let arr = prop.post.id.split("/");
  for (let i = 0; i < arr.length; i++) {
    if (arr[i] == "author") {
      console.log(arr[i + 1]);
      post_author_id = arr[i + 1];
    } else if (arr[i] == "posts") {
      post_id = arr[i + 1];
    }
  }

  // is this post written by me?
  const isMyPost =
    prop != null && userInfo != null
      ? userInfo.author_id == post_author_id
        ? true
        : false
      : false;

  const CommonMark = require("commonmark");
  const ReactRenderer = require("commonmark-react-renderer");

  const parser = new CommonMark.Parser();
  const renderer = new ReactRenderer();

  var content = prop ? prop.post.content : "";

  if (prop.post.content_type == "text/markdown") {
    const input = content;
    const ast = parser.parse(input);
    content = renderer.render(ast);
  }

  const dispatch = useDispatch();

  const postDelete = useSelector((state) => state.postDelete);
  const { error, success, post } = postDelete;

  const deleteHandler = () => {
    dispatch(deletePost(post_id));
    window.location.reload();
  };

  return (
    <div className="m-5">
      {error && <Message variant="danger">{error}</Message>}
      <Card>
        <Card.Body>
          <div className="d-flex">
            <Card.Img
              className="m-1"
              src={Avatar}
              style={{ width: "6rem", height: "6rem" }}
            />
            <Card.Title className="m-2 justify-content-center">
              {prop.post.author.displayName}
            </Card.Title>
            {isMyPost ? (
              <DropdownButton
                className="ms-auto mx-1"
                id="bg-vertical-dropdown-1"
              >
                <Dropdown.Item eventKey="1">Edit</Dropdown.Item>
                <Dropdown.Item eventKey="2" onClick={deleteHandler}>
                  Delete
                </Dropdown.Item>
              </DropdownButton>
            ) : (
              <div></div>
            )}
          </div>
          <Card.Title className="m-3 text-center">
            <u>{prop.post.title}</u>
          </Card.Title>
          <Card.Text className="mx-3 my-4">{content}</Card.Text>
          <Row className="justify-content-between m-1">
            <Col className="d-flex align-items-center">
              Likes: {prop.post.numLikes}&nbsp; &nbsp; &nbsp; Comments:{" "}
              {prop.post.comments.length}
            </Col>
            <Col className="text-end">
              <Button
                className="m-1"
                style={{ width: "7rem" }}
                variant="success"
              >
                {like.isLike ? "Liked" : "Like"}
              </Button>
              <Button
                className="m-1"
                style={{ width: "7rem" }}
                variant="info"
                onClick={commentPost}
              >
                Comment
              </Button>
              <Button
                className="m-1"
                style={{ width: "7rem" }}
                variant="warning"
                onClick={sharePost}
              >
                {share ? "Shared" : "Share"}
              </Button>
            </Col>
          </Row>
          {comment ? (
            <div class="border rounded p-3">
              <ListGroup>
                {prop.post.comments.map((comment) => (
                  <ListGroup.Item>Edit this later</ListGroup.Item>
                ))}
              </ListGroup>
              <Form.Group className="my-2" controlId="content">
                <Form.Control
                  as="textarea"
                  rows={2}
                  // onChange={(e) => setContent(e.target.value)}
                />
              </Form.Group>
              <div className="d-flex align-items-end justify-content-end px-5">
                <Button className="btn" type="submit" variant="primary">
                  Submit
                </Button>
              </div>
            </div>
          ) : (
            ""
          )}
        </Card.Body>
      </Card>
    </div>
  );
}

export default Posts;
