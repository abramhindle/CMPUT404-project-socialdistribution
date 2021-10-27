import React, { useState, useEffect } from "react";
import { Form, Button } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import Message from "../components/Message";
import { createPost, postReset } from "../actions/postActions";
import jQuery from "jquery";
import { useHistory } from "react-router-dom";

// form page for making a new post; redirect user to login if they are not logged in
function PostForm() {
  const [title, setTitle] = useState("");
  const [contentType, setContentType] = useState("text/plain");
  const [content, setContent] = useState("");
  const [visibility, setVisibility] = useState("PUBLIC");
  // not ready yet, add when there is a view to GET friends list of author (friend id + friend name)
  const [privateReceiver, setPrivateReceiver] = useState("");

  const [message, setMessage] = useState("");

  const dispatch = useDispatch();

  const postCreate = useSelector((state) => state.postCreate);
  const { error, success, post } = postCreate;

  // reference: https://stackoverflow.com/a/50735730
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  var csrftoken = getCookie("csrftoken");

  const submitHandler = (e) => {
    e.preventDefault();
    if (title == "" || content == "") {
      setMessage("Please fill in title and content to make a post.");
    } else {
      // remove extra message banner
      setMessage();
      console.log(title, content, contentType);
      dispatch(createPost(title, content, contentType, visibility, csrftoken));
    }
  };

  let history = useHistory();

  useEffect(() => {
    // redirect user to homepage if post creation is successful
    if (success) {
      history.push("/");
      dispatch(postReset());
    }
  }, [history, dispatch, success]);

  return (
    <div>
      {message && <Message variant="danger">{message}</Message>}
      {error && <Message variant="danger">{error}</Message>}
      <Form
        className="justfiy-content-center align-center"
        onSubmit={submitHandler}
      >
        <Form.Group className="m-3" controlId="title">
          <Form.Label>Title</Form.Label>
          <Form.Control
            type="title"
            placeholder="Title here"
            onChange={(e) => setTitle(e.target.value)}
          />
        </Form.Group>

        <Form.Group className="m-3">
          <Form.Label>Content Type</Form.Label>
          <Form.Control
            as="select"
            onChange={(e) => {
              setContentType(e.target.value);
            }}
          >
            <option value="text/plain">Plain Text</option>
            <option value="text/markdown">CommonMark</option>
          </Form.Control>
        </Form.Group>

        <Form.Group className="m-3">
          <Form.Label>Visibility</Form.Label>
          <Form.Control
            as="select"
            onChange={(e) => {
              setVisibility(e.target.value);
            }}
          >
            <option value="PUBLIC">Public Post</option>
            {/* Should change to friends later */}
            <option value="FOLLOWERS">Followers Post</option>
            <option value="PRIVATE">Private Post</option>
          </Form.Control>
          {visibility == "PRIVATE" ? (
            <Form.Control
              as="select"
              size="sm"
              className="my-3"
              onChange={(e) => {
                setPrivateReceiver(e.target.value);
              }}
            >
              {/* For this part, need to map to each friend */}
              <option value="friend_id1">Friend1</option>
              <option value="friend_id2">Friend2</option>
            </Form.Control>
          ) : (
            ""
          )}
        </Form.Group>

        <Form.Group className="m-3" controlId="content">
          <Form.Label>Content</Form.Label>
          <Form.Control
            as="textarea"
            rows={5}
            onChange={(e) => setContent(e.target.value)}
          />
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
