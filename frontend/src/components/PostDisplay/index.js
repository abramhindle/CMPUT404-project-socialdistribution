import React from "react";
import { Avatar, Button, Input, Card } from "antd";
import { UserOutlined, LikeOutlined, DislikeOutlined } from "@ant-design/icons";
import CommentArea from "../CommentArea";

export default class PostDisplay extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = { isModalVisible: false };
  }

  handleClickReply = () => {
    this.setState({ isModalVisible: !this.state.isModalVisible });
  };

  handleCommentModalVisiblility = () => {
    this.setState({ isModalVisible: !this.state.isModalVisible });
  };

  handleClickDislike = () => {
    //TODO
  };

  handleClickLike = () => {
    //TPDP
  };

  render() {
    const { title, authorName, content, datetime } = this.props;
    return (
      <div>
        <Card
          title={title}
          extra={
            <span>
              <Avatar icon={<UserOutlined />} />
              <p>{authorName}</p>
            </span>
          }
        >
          <div style={{ margin: "24px", textAlign: "center" }}>{content}</div>
          <p>{datetime}</p>
          <div>
            <Button icon={<LikeOutlined />} onClick={this.handleClickLike} />
            <Button
              icon={<DislikeOutlined onClick={this.handleClickDislike} />}
            />
            <Button
              type="text"
              style={{ color: "#C5C5C5" }}
              onClick={this.handleClickReply}
            >
              Reply to
            </Button>
          </div>
          <CommentArea
            visible={this.state.isModalVisible}
            handleCommentModalVisiblility={this.handleCommentModalVisiblility}
          />
        </Card>
      </div>
    );
  }
}
