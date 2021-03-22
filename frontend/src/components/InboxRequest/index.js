import React from "react";
import { Button, List, message, Image, Avatar } from "antd";
import { UserOutlined, CheckOutlined, CloseOutlined} from "@ant-design/icons";
import { getRequest } from "../../requests/requestFriendRequest";
import ReactMarkdown from "react-markdown";
import { getAuthorByAuthorID } from "../../requests/requestAuthor";
import SingleRequest from "../SingleRequest";

export default class InboxRequest extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      requestDataSet: [],
      authorID : this.props.authorID,
    };
  }

  componentDidMount() {
    this._isMounted = true;
    console.log("stream1", this.state.authorID);
    getRequest({
      authorID: this.state.authorID,
    }).then((res) => {
      if (res.status === 200) {
        this.getRequestDataSet(res.data).then((value) => {
          this.setState({ requestDataSet: value });
        });
        //const myRequests = this.getRequestDataSet(res.data);
        //this.setState({ requestDataSet: myRequests });
      } else {
        message.error("Fail to get my requests.");
      }
    });

  }

  componentWillUnmount() {
    this._isMounted = false;
  }

  handleClickClose = () => {

  }

  getRequestDataSet = (requestData) => {
    let promise = new Promise(async (resolve, reject) => {
      const requestSet = [];
      for (const element of requestData) {
        
        const res = await getAuthorByAuthorID({ authorID: element.actor });
        console.log("test5", element.actor);
        requestSet.push({
          actorName: res.data.displayName,
          actorID: element.actor,
        });
      }
      resolve(requestSet);
    });
    
    return promise;
  };

  render() {
    const { requestDataSet } = this.state;
    console.log("inboxpost", this.props.authorID);
    return (
      <div style={{}}>
        <List
          className="requests"
          itemLayout="horizontal"
          dataSource={requestDataSet}
          renderItem={(item) => (
            <li>
              <SingleRequest
                authorID={this.state.authorID}
                actorName={item.actorName}
                actorID={item.actorID}
              />
            </li>
          )}
        />
      </div>
    );
  }
}
