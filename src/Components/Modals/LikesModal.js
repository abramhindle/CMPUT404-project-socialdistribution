import { Modal, Button, ButtonToolbar } from 'rsuite';
import React, { useLayoutEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getAuthorId } from "../utils/auth";
import { reqInstance } from "../utils/axios";

function LIKESMODAL({ postobj }) {
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  const [likes, setLikes] = useState([])
  var navigate = useNavigate()

  useLayoutEffect(() => {
    if (!localStorage.getItem("loggedIn")) {
      navigate("/login");
    } else {
      const author_id = getAuthorId(postobj.author.id);
      const post_id = getAuthorId(postobj.id);
      const url = `posts/authors/${author_id}/posts/${post_id}/likes/`
      reqInstance({ method: "get", url: url }).then((res) => {
        setLikes(res.data);
      });
    }
  }, []);

  const item = (obj) => {
    return obj.author.displayName;
  }

  return (
    <>
      <ButtonToolbar>
        <Button onClick={handleOpen} appearence="subtle">
          {" "}
          Likes
        </Button>
      </ButtonToolbar>

      <Modal open={open} onClose={handleClose}>
        <Modal.Header>
          <Modal.Title>Likes on this post</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {likes.map((obj) => item(obj))}
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={handleClose} appearance="primary">
            Ok
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default LIKESMODAL;
