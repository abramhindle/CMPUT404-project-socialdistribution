import React from "react";
import { Input, Comment, Avatar } from "antd";

const { TextArea } = Input;

const ExampleComment = ({ children }) => (
  <Comment
    actions={[<span key="comment-nested-reply-to">Reply to</span>]}
    author={<a>Han Solo</a>}
    avatar={
      <Avatar
        src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"
        alt="Han Solo"
      />
    }
    content={
      <p>
        We supply a series of design principles, practical patterns and high
        quality design resources (Sketch and Axure).
      </p>
    }
  >
    {children}
  </Comment>
);

export default class Post extends React.Component {
  state = {
    value: "",
  };

  onChange = ({ target: { value } }) => {
    this.setState({ value });
  };

  render() {
    const { value } = this.state;

    return (
      <div>
        <TextArea placeholder="Post Title" autoSize />
        <div style={{ margin: "24px 0" }} />
        <TextArea
          value={value}
          placeholder="Write your post"
          onChange={this.onChange}
          autoSize={{ minRows: 3, maxRows: 5 }}
        />
      </div>
    );
  }
}
