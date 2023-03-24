import { Modal, Button, ButtonToolbar } from 'rsuite';
import React, { useLayoutEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getAuthorId } from "../utils/auth";
import axios from "axios";

function LIKESMODAL({ likes }) {
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const getLikes = () => {
    if (likes && likes.length > 0) {
      return likes.items.map((obj) => item(obj))
    }
  }

  const item = (obj) => {
    return obj.author.displayName;
  }

  return (
    <>
      <ButtonToolbar>
        <Button onClick={handleOpen} appearence="subtle"> Likes</Button>
      </ButtonToolbar>

      <Modal open={open} onClose={handleClose}>
        <Modal.Header>
          <Modal.Title>Likes on this post</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {getLikes()}
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