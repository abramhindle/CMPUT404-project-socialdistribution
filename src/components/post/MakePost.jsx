import React, { Component } from "react";
import "../../styles/post/MakePost.scss";
import ImageOutlinedIcon from "@material-ui/icons/ImageOutlined";
import VisibilityRoundedIcon from "@material-ui/icons/VisibilityRounded";
import TextareaAutosize from "react-textarea-autosize";
import UploadImageModal from "./UploadImageModal";
import PostPreviewModal from "./PostPreviewModal";

class MakePost extends Component {
  constructor(props) {
    super(props);
    this.state = {
      uploadModalVisibility: false,
      previewModalVisibility: false,
      postContent: "",
      postImage: "",
    };
  }

  handleTextChange = (event) => {
    this.setState({ postContent: event.target.value });
  };

  handleImageUpload = (image) => {
    this.setState({ postImage: URL.createObjectURL(image) });
  }

  handleSubmit = (event) => {
    event.preventDefault();

    const { postContent } = this.state;
    // eslint-disable-next-line no-alert
    alert(postContent);
  };

  toggleUploadModalVisibility = () => {
    this.setState((prevState) => ({
      uploadModalVisibility: !prevState.uploadModalVisibility,
    }));
  }

  togglePreviewModalVisibility = () => {
    this.setState((prevState) => ({
      previewModalVisibility: !prevState.previewModalVisibility,
    }));
  }

  render() {
    const {
      uploadModalVisibility,
      previewModalVisibility,
      postContent,
      postImage,
    } = this.state;

    // Marcos, https://stackoverflow.com/questions/2476382/how-to-check-if-a-textarea-is-empty-in-javascript-or-jquery
    const postLength = postContent.replace(/^\s+|\s+$/g, "").length;
    const validPost = postLength > 0 || postImage !== "";

    return (
      <div className="make-post-wrapper">
        <div className="make-post-content">
          <div className="make-post-header">
            <b>NEW POST</b>
            <select className="privacy-select">
              <option selected value="public">
                Anyone
              </option>
              <option value="another author">Specific author</option>
              <option value="friends">Friends</option>
              <option value="mutual friends">Mutual friends</option>
              <option value="local friends">Local friends</option>
              <option value="private">Private</option>
            </select>
          </div>
          <UploadImageModal show={uploadModalVisibility} onHide={this.toggleUploadModalVisibility} onUpload={this.handleImageUpload} />
          <PostPreviewModal show={previewModalVisibility} onHide={this.togglePreviewModalVisibility} postContent={postContent} imageObjectUrl={postImage} />
          <form className="make-post-input-wrapper" action="submit">
            <TextareaAutosize
              placeholder="What's on your mind?"
              className="post-text-area"
              onChange={this.handleTextChange}
            />
            {
              postImage ? (
                <img src={postImage} className="preview-image" alt="preview" />
              ) : null
            }
            <div className="make-post-buttons-wrapper">
              {
                validPost ? (
                  <VisibilityRoundedIcon
                    className="icon"
                    onClick={this.togglePreviewModalVisibility}
                  />
                ) : null
              }

              <ImageOutlinedIcon
                className="icon"
                onClick={this.toggleUploadModalVisibility}
              />
              <button
                type="submit"
                className="post-button"
                onClick={this.handleSubmit}
                disabled={!validPost}
              >
                Post
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  }
}
export default MakePost;
