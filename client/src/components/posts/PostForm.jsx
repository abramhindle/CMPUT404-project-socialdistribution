import React, { Component } from "react";
import { Button, TextField } from "@material-ui/core";
import { connect } from "react-redux";
import "../../styles/postForm.css";
import axios from "axios";

class PostForm extends Component {
  state = {
    show: false,
    title: "",
    source: "http://hello.com",
    origin: "http://hh.com",
    description: "",
    contentType: "text/plain",
    content: "",
    visibility: "PUBLIC",
    unlisted: false,
  }

  componentDidMount = () => {
    console.log("authorID in PostForm (componentDidMount): ", this.props.authorID);
  }

  handleShow = () => {
    const { show } = this.state;
    this.setState({ show: !show });
  }

  handlePost = async () => {
    const {
      title,
      source,
      origin,
      description,
      contentType,
      content,
      visibility,
      unlisted } = this.state;

    const { authorID } = this.props.authorID;
    if (title && description && content) {
      try {
        await axios.post(`service/author/${authorID}/posts/`, { title, source, origin, description, contentType, content, visibility, unlisted });
        this.setState({ show: false });
        window.location = "/aboutme";
      } catch (err) {
        console.log(err.message);
      }
    } else {
      alert("Cannot be empty !");
    }

  }

  render() {
    const { show, title, description, content } = this.state;

    return (
      <div>
        {
          this.props.authorID !== null ?
            <div id="form-control">
              <Button
                id="show-btn"
                variant="outlined"
                color="primary"
                className="btn"
                onClick={this.handleShow}
              >
                {show ? "Cancel" : "Make Post"}
              </Button>
              {
                show ?
                  <div id="post-form">
                    <h4>New Post</h4>
                    <TextField
                      style={{ width: 300 }}
                      id="post-title"
                      label="Title"
                      value={title}
                      onChange={(e) => this.setState({ title: e.target.value })}
                    /><br />
                    <TextField
                      style={{ width: 300 }}
                      id="post-description"
                      label="Description"
                      value={description}
                      onChange={(e) => this.setState({ description: e.target.value })}
                    /><br />
                    <TextField
                      style={{ width: 350 }}
                      id="post-content"
                      label="Content"
                      multiline
                      rows={5}
                      value={content}
                      onChange={(e) => this.setState({ content: e.target.value })}
                    /><br />
                    <Button
                      id="post-btn"
                      style={{ marginTop: 15 }}
                      variant="outlined"
                      color="primary"
                      onClick={this.handlePost}
                    >
                      Post
                    </Button>
                  </div>
                  :
                  null
              }
            </div>
            :
            null
        }
      </div>
    )
  }
}

const mapStateToProps = (state) => ({
  authorID: state.user.authorID
})

export default connect(mapStateToProps)(PostForm);