import React from "react";
import { Input, Button, Checkbox, Tag } from "antd";
import { sendPost } from "../../requests/requestPost";

const { TextArea } = Input;
const { CheckableTag } = Tag;
const tagsData = ["Movies", "Books", "Music", "Sports"];

export default class Post extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      authorID: "",
      title: "",
      content: "",
      visibility: "PUBLIC",
      description: "",
      categories: [],
      unlisted: false,
    };
  }
  componentDidMount() {
    this._isMounted = true;
    console.log("----", this.state.authorID);
    if (this.state.authorID === "" && this._isMounted) {
      this.setState({ authorID: this.props.authorID });
    }
  }

  componentWillUnmount() {
    this._isMounted = false;
  }

  onTitleChange = ({ target: { value } }) => {
    this.setState({ title: value });
  };

  onDescriptionChange = ({ target: { value } }) => {
    this.setState({ description: value });
  };

  onContentChange = ({ target: { value } }) => {
    this.setState({ content: value });
  };

  onSendClick = () => {
    let today = new Date();
    const date =
      today.getFullYear() +
      "-" +
      (today.getMonth() + 1) +
      "-" +
      today.getDate();

    let params = {
      title: this.state.title,
      source: window.location.href,
      origin: window.location.href,
      description: this.state.description,
      contentType: "text/plain",
      content: this.state.content,
      categories: this.state.categories,
      count: 0,
      size: 0,
      comments:
        "http://127.0.0.1:8000/author/012808163f04427691601a2b56055884/posts/8f0af4f3810c4f97b9674ac5e782beab/comments/",
      published: date,
      visibility: this.state.visibility,
      unlisted: this.state.unlisted,
      authorID: this.state.authorID,
    };
    sendPost(params).then((response) => {
      console.log("post send", response.data);
    });
  };

  onVisibilityChange = (e) => {
    this.setState({ visibility: e.target.checked });
  };

  handleCaterotiesChange = (tag, checked) => {
    const { categories } = this.state;
    const nextSelectedTags = checked
      ? [...categories, tag]
      : categories.filter((t) => t !== tag);
    this.setState({ categories: nextSelectedTags });
  };

  render() {
    const { value, categories } = this.state;

    return (
      <div>
        <h2>Creaet Your Post</h2>
        <TextArea
          onChange={this.onTitleChange}
          placeholder="Post Title"
          autoSize
        />
        <div style={{ margin: "24px 0" }} />
        <TextArea
          onChange={this.onDescriptionChange}
          placeholder="Description"
          autoSize
        />
        <div style={{ margin: "24px 0" }} />
        <TextArea
          value={value}
          placeholder="Write your post"
          onChange={this.onContentChange}
          autoSize={{ minRows: 3, maxRows: 5 }}
        />
        <div style={{ margin: "24px 0" }} />
        <Checkbox defaultChecked onChange={this.onVisibilityChange}>
          Public
        </Checkbox>
        <Button onClick={this.onSendClick}>Send</Button>
        <div>
          <span style={{ marginRight: 8 }}>Categories:</span>
          {tagsData.map((tag) => (
            <CheckableTag
              key={tag}
              checked={categories.indexOf(tag) > -1}
              onChange={(checked) => this.handleCaterotiesChange(tag, checked)}
            >
              {tag}
            </CheckableTag>
          ))}
        </div>
      </div>
    );
  }
}
