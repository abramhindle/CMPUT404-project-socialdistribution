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
  const [content, setContent] = useState("");

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
      dispatch(createPost(title, content, csrftoken));
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
