/* eslint-disable react/jsx-props-no-spreading */
import React, { Component } from "react";
import { useDropzone } from "react-dropzone";
import PropTypes from "prop-types";
import "../../styles/post/UploadImageModal.scss";
import Modal from "react-bootstrap/Modal";

function ImageDropzone(props) {
  const { onDropAccepted, onDropRejected } = props;
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: "image/*",
    multiple: false,
    onDropAccepted,
    onDropRejected,
  });

  return (
    <div className="dropzone" {...getRootProps()}>
      <input {...getInputProps()} />
      {
        isDragActive ? (
          <p>Drop image here ...</p>
        ) : <p>Drag and drop an image here, or click to select an image</p>
      }
    </div>
  );
}

class UploadImageModal extends Component {
  constructor(props) {
    super(props);

    this.state = {
      errorMessage: null,
      imageFile: null,
    };
  }

  handleDropAccept = (file) => {
    this.setState({
      errorMessage: null,
      imageFile: file[0],
    });
  }

  handleDropError = () => {
    this.setState({
      errorMessage: "Please upload a single image file",
      imageFile: null,
    });
  }

  handleUpload = () => {
    const { onUpload } = this.props;
    const { imageFile } = this.state;

    onUpload(imageFile);
    this.hideModal();
  }

  hideModal = () => {
    const { onHide } = this.props;
    onHide(); // the default behaviour

    // need to wait 500ms otherwise the contents will clear out while the modal is still
    // fading away
    setTimeout(() => {
      // clear out the modal contents so that the modal is empty next time
      this.setState({
        errorMessage: null,
        imageFile: null,
      });
    }, 500);
  }

  render() {
    const { show } = this.props;
    const { errorMessage, imageFile } = this.state;
    return (
      <Modal onHide={this.hideModal} show={show} className="upload-image-modal">
        <Modal.Header closeButton>
          <Modal.Title>Upload Image</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <ImageDropzone
            onDropAccepted={this.handleDropAccept}
            onDropRejected={this.handleDropError}
          />
          <div className="error-message">{errorMessage}</div>
          {
            imageFile ? <img className="preview-image" src={URL.createObjectURL(imageFile)} alt="preview" /> : null
          }
        </Modal.Body>
        <Modal.Footer className="upload-button-wrapper">
          <button
            type="button"
            className="upload-button"
            onClick={this.handleUpload}
            disabled={imageFile === null}
          >
            Upload
          </button>
        </Modal.Footer>
      </Modal>
    );
  }
}

ImageDropzone.propTypes = {
  onDropAccepted: PropTypes.func.isRequired,
  onDropRejected: PropTypes.func.isRequired,
};

UploadImageModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onHide: PropTypes.func.isRequired,
  onUpload: PropTypes.func.isRequired,
};

export default UploadImageModal;
