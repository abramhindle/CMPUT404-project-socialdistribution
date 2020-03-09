import React from "react";
import PropTypes from "prop-types";
import "../../styles/post/PostPreviewModal.scss";
import Modal from "react-bootstrap/Modal";
import Post from "./Post";

function PostPreviewModal(props) {
  const {
    onHide,
    show,
    postContent,
    imageObjectUrl,
  } = props;

  return (
    <Modal size="lg" onHide={onHide} show={show} className="post-preview-modal">
      <Modal.Header closeButton>
        <Modal.Title>Post Preview</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Post
          username="username"
          postTime={new Date()}
          imageSrc={imageObjectUrl}
          content={postContent}
          previewMode // to prevent it from rendering the menu bar with dropdown and time
        />
      </Modal.Body>
    </Modal>
  );
}

PostPreviewModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onHide: PropTypes.func.isRequired,
  postContent: PropTypes.string.isRequired,
  imageObjectUrl: PropTypes.string.isRequired,
};

export default PostPreviewModal;
