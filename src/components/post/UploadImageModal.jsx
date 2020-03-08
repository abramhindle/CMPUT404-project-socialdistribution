import React from "react";
import PropTypes from "prop-types";
import "../../styles/post/UploadImageModal.scss";
import Modal from "react-bootstrap/Modal";

function UploadImageModal(props) {
  const { onHide, show } = props;

  return (
    <Modal onHide={onHide} show={show} className="upload-image-modal">
      <Modal.Header closeButton>
        <Modal.Title>Upload images</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <input
          accept="image/*"
          type="file"
        />
      </Modal.Body>
      <Modal.Footer className="upload-button-wrapper">
        <button
          type="button"
          className="upload-button"
          onClick={onHide}
        >
          Upload
        </button>
      </Modal.Footer>
    </Modal>
  );
}

UploadImageModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onHide: PropTypes.func.isRequired,
};

export default UploadImageModal;
