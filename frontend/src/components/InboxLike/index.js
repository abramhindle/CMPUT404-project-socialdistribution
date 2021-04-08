import React from "react";
import { List, message, Avatar } from "antd";
import { UserOutlined } from "@ant-design/icons";
import { getinboxlike } from "../../requests/requestLike";
import { getLikeDataSet } from "../Utils";

export default class InboxLike extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      likelist: [],
      authorID: this.props.authorID,
    };
  }

  componentDidMount() {
    this._isMounted = true;
    getinboxlike({ authorID: this.state.authorID }).then((res) => {
      if (res.status === 200) {
        getLikeDataSet(res.data).then((value) => {
          this.setState({ likelist: value });
        });
      } else {
        message.error("Request failed!");
      }
    });
  }

  componentWillUnmount() {
    this._isMounted = false;
  }

  render() {
    const { likelist } = this.state;
    return (
      <div style={{ margin: "0 20%" }}>
        {likelist.length === 0 ? (
          ""
        ) : (
          <List
            bordered
            itemLayout="horizontal"
            dataSource={likelist}
            renderItem={(item) => (
              <List.Item>
                <List.Item.Meta
                  avatar={<Avatar icon={<UserOutlined />} />}
                  title={item.authorName}
                  description={item.summary}
                />
              </List.Item>
            )}
          />
        )}
      </div>
    );
  }
}
