import React from "react";
import {  List, message, Avatar} from "antd";
import { UserOutlined } from "@ant-design/icons";
import { getinboxlike } from "../../requests/requestLike";
import { getAuthorByAuthorID } from "../../requests/requestAuthor";

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
    console.log("123", this.state.authorID);
    getinboxlike({ authorID: this.state.authorID }).then((res) => {
      if (res.status === 200) {
        res.data.forEach(element => {
            getAuthorByAuthorID({authorID:element.author}).then((author)=>{
            }
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

    return (
      <div style={{}}>
        {likelist.length === 0 ? (
            ""
        ) : (
            <List
            bordered
            itemLayout="horizontal"
            dataSource={likelist}
            renderItem={(item )=> (
              <List.Item>
                <List.Item.Meta
                  avatar={<Avatar icon={<UserOutlined />} />}
                  title={item.author}
                  description="likes"
                />
              </List.Item>
            )}
          />
      
        )}
      </div>
    );
  }
}
