import React from "react";
import { Avatar, Button, Card, List, Divider } from "antd";
import { UserOutlined, LikeOutlined, DislikeOutlined } from "@ant-design/icons";
import CommentArea from "../CommentArea";
import { getCommentList } from "../../requests/requestComment";

export default class PostDisplay extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = { isModalVisible: false };
  }

  componentDidMount() {
    getCommentList({ postID: this.props.postID }).then((res) => {
      if (res.status === 200) {
        console.log(res.data);
        this.setState({ comments: res.data });
      }
    });
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
    const { title, authorName, content, datetime, postID } = this.props;
    console.log("post display", this.props.authorID);
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
          <Divider orientation="left">Comments</Divider>
          <List
            bordered
            pagination={true}
            dataSource={this.state.comments}
            renderItem={(item) => (
              <List.Item>
                <Avatar icon={<UserOutlined />} />
                <p>{item.comment}</p>
              </List.Item>
            )}
          />
          <CommentArea
            authorID={this.props.authorID}
            postID={postID}
            visible={this.state.isModalVisible}
            handleCommentModalVisiblility={this.handleCommentModalVisiblility}
          />
        </Card>
      </div>
    );
  }
}
