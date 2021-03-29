import React from "react";
import { List, message } from "antd";
import { getInboxPost } from "../../requests/requestPost";
import PostDisplay from "../PostDisplay";
import { getPostDataSet } from "../Utils";

export default class InboxPost extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      postDataSet: [],
      authorID: this.props.authorID,
    };
  }

  componentDidMount() {
    this._isMounted = true;
    getInboxPost({
      authorID: this.state.authorID,
    }).then((res) => {
      if (res.status === 200) {
        getPostDataSet(res.data, false).then((value) => {
          this.setState({ postDataSet: value });
        });
      } else {
        message.error("Fail to get posts.");
      }
    });
  }

  componentWillUnmount() {
    this._isMounted = false;
  }

  render() {
    const { postDataSet } = this.state;

    return (
      <div style={{}}>
        <List
          className="posts-list"
          itemLayout="horizontal"
          dataSource={postDataSet}
          renderItem={(item) => (
            <li>
              <PostDisplay
                title={item.title}
                authorName={item.authorName}
                github={item.github}
                content={item.content}
                datetime={item.datetime}
                authorID={this.state.authorID}
                postID={item.postID}
                rawPost={item.rawPost}
                categories={item.categories}
                remote={item.remote}
              />
            </li>
          )}
        />
      </div>
    );
  }
}
