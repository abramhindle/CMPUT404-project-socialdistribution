import React from "react";
import { Tag, Button, List, message, Image, Avatar } from "antd";
import { UserOutlined, CheckOutlined, CloseOutlined} from "@ant-design/icons";
import { deleteRequest } from "../../requests/requestFriendRequest";
import ReactMarkdown from "react-markdown";
import { getAuthorByAuthorID } from "../../requests/requestAuthor";

export default class SingleRequest extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      isRejected: false,
      isAccepted: false,
      ButtonDisabled: false,
      authorID : this.props.authorID,
    };
  }

  componentDidMount() {
    this._isMounted = true;

  }

  componentWillUnmount() {
    this._isMounted = false;
  }

  handleClickClose = () => {
    console.log("actorID", this.props.actorID);
    console.log("objectID", this.props.authorID);
    let params = {
      actor: this.props.actorID,
      object: this.props.authorID,

    };
    console.log("params.actor:", params.actor);
    deleteRequest(params).then((response) => {
      if (response.status === 200) {
        message.success("Request Rejected.");
        //window.location.reload();
      } else {
        message.error("Reject Failed!");
      }
    });
    this.setState(
      (prevState) => {
        return {
          isRejected: true,
          ButtonDisabled: true,
        };
      });
    
  }

  handleClickAccept = () => {
    this.setState(
      (prevState) => {
        return {
          isAccepted: true,
          ButtonDisabled: true,
        };
      });
    console.log("actorID", this.props.actorID);
    let params = {
      actor: this.props.actorID,
      object: this.props.authorID,

    };
    deleteRequest(params).then((response) => {
      if (response.status === 200) {
        message.success("Request Accepted.");
        //window.location.reload();
      } else {
        message.error("Accept Failed!");
      }
    });
  }


  

  render() {
    const { authorID, actorName, actorID } = this.props;
    const {isRejected, isAccepted, ButtonDisabled, } = this.state;
    console.log("inboxpost", this.props.authorID);
    console.log("isRejected", isRejected);
    console.log("isButtonDisabled", ButtonDisabled);
    return (
      <div style={{}}>
        <Avatar icon={<UserOutlined />} />
        {actorName} wants to follow you.
        <Button style={{float: 'right'}} disabled={ButtonDisabled} type="primary" icon={<CheckOutlined />}>
        </Button>
        <Button style={{float: 'right'}} disabled={ButtonDisabled} type="primary" icon={<CloseOutlined />}
        onClick={this.handleClickClose}>
        </Button>
        <Tag visible={isRejected}>Request rejected.</Tag>
        <Tag visible={isAccepted}>Request accepted.</Tag>
  
      </div>
    );
  }
}
