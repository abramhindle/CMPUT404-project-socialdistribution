import React, { useState, useEffect } from "react";
import {
  Card,
  Button,
  Row,
  Col,
  DropdownButton,
  Dropdown,
  Form,
} from "react-bootstrap";
import Avatar from "../images/avatar.jpg";

// return list of posts within card filtered with parameter (category)
function Posts() {
  // const dispatch = useDispatch();
  // const userLogin = useSelector((state) => state.userLogin);
  const [like, setLike] = useState({ isLike: false, amount: 10 });
  const [comment, setComment] = useState(false);
  const [share, setShare] = useState(false);

  const likePost = () => {
    if (!like.isLike) {
      setLike({ isLike: true, amount: like.amount + 1 });
    } else {
      setLike({ isLike: false, amount: like.amount - 1 });
    }
  };
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

  var isMyPost = true;
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
            {isMyPost ? (
              <DropdownButton
                className="ms-auto mx-1"
                id="bg-vertical-dropdown-1"
              >
                <Dropdown.Item eventKey="1">Edit</Dropdown.Item>
                <Dropdown.Item eventKey="2">Delete</Dropdown.Item>
              </DropdownButton>
            ) : (
              <div></div>
            )}
          </div>
          <Card.Title className="m-3">Title</Card.Title>
          <Card.Text className="m-3">
            Some quick example text to build on the card title and make up the
            bulk of the card's content. asdfhuisdhfuasdhiudshuidshdsuishduhfdui
            sadfhiuasdhfdoiushfaios
          </Card.Text>
          <Row className="justify-content-between m-1">
            <Col className="d-flex align-items-center">
              Likes: {like.amount}&nbsp; &nbsp; &nbsp; Comments: 200
            </Col>
            <Col className="text-end">
              <Button
                className="m-1"
                style={{ width: "7rem" }}
                variant="success"
                onClick={likePost}
              >
                {like.isLike ? "liked" : "like"}
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
                {share ? "shared" : "share"}
              </Button>
            </Col>
          </Row>
        </Card.Body>
      </Card>
      {comment ? (
        <div>
          <Form.Group className="my-2" controlId="content">
            <Form.Control
              as="textarea"
              rows={3}
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
    </div>
  );
}

export default Posts;
