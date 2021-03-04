import React, { Component } from "react";
// import ReactMarkDown from "react-markdown";

// This component is used to display the Post
class PostCard extends Component {
  state = {
    title: "",
    source: "http://hello.com",
    origin: "http://hh.com",
    description: "",
    contentType: "text/plain",
    content: "",
    visibility: "PUBLIC",
    unlisted: false,
  }

  render() {
    return (
      <div style={{ border: "solid 1px grey" }}>
        <h1>Title: {this.props.post.title}</h1>
        <h2>Description: {this.props.post.description}</h2>
        <p>Content: {this.props.post.content}</p>
      </div>
    )
  }
}

export default PostCard;