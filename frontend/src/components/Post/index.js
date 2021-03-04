import React from "react";
import { Input, Button, Checkbox, Tag, message, Upload, Modal } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import { sendPost } from "../../requests/requestPost";

const { TextArea } = Input;
const { CheckableTag } = Tag;
const tagsData = ["Movies", "Books", "Music", "Sports"];

function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });
}

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
      previewVisible: false,
      previewImage: "",
      fileList: [],
      previewTitle: "",
    };
  }

  componentDidMount() {
    this._isMounted = true;
    if (this.state.authorID === "" && this._isMounted) {
      this.setState({ authorID: this.props.authorID });
      console.log("post", this.props.authorID);
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

  // image upload
  handleImageCancel = () => this.setState({ previewVisible: false });

  handleImagePreview = async (file) => {
    if (!file.url && !file.preview) {
      file.preview = await getBase64(file.originFileObj);
    }

    this.setState({
      previewImage: file.url || file.preview,
      previewVisible: true,
      previewTitle:
        file.name || file.url.substring(file.url.lastIndexOf("/") + 1),
    });
  };

  handleImageChange = ({ fileList }) => this.setState({ fileList });

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
      published: date,
      visibility: this.state.visibility,
      unlisted: this.state.unlisted,
      authorID: this.state.authorID,
    };
    sendPost(params).then((response) => {
      message.success("post send", response.data);
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
    const {
      value,
      categories,
      previewVisible,
      previewImage,
      fileList,
      previewTitle,
    } = this.state;

    const uploadButton = (
      <div>
        <PlusOutlined />
        <div style={{ marginTop: 8 }}>Upload</div>
      </div>
    );

    return (
      <div style={{ margin: "10% 20%" }}>
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

        {/* Upload image */}
        <div>
          <Upload
            action="https://www.mocky.io/v2/5cc8019d300000980a055e76"
            listType="picture-card"
            fileList={fileList}
            onPreview={this.handleImagePreview}
            onChange={this.handleImageChange}
          >
            {fileList.length >= 8 ? null : uploadButton}
          </Upload>
          <Modal
            visible={previewVisible}
            title={previewTitle}
            footer={null}
            onCancel={this.handleImageCancel}
          >
            <img
              alt="uploadImage"
              style={{ width: "80%" }}
              src={previewImage}
            />
          </Modal>
        </div>
        <div style={{ margin: "24px 0" }} />

        <div style={{ display: "inline" }}>
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
          <Checkbox
            style={{ float: "right" }}
            defaultChecked
            onChange={this.onVisibilityChange}
          >
            Public
          </Checkbox>
        </div>
        <div style={{ margin: "24px auto" }}>
          <Button type="primary" onClick={this.onSendClick}>
            Send
          </Button>
        </div>
      </div>
    );
  }
}
