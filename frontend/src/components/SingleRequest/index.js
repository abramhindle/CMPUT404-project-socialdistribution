import React from "react";
import { Tag, Button, message } from "antd";
import { CheckCircleOutlined, CloseCircleOutlined } from "@ant-design/icons";
import { deleteRequest } from "../../requests/requestFriendRequest";
import { createFollower } from "../../requests/requestFollower";

export default class SingleRequest extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      isRejected: false,
      isAccepted: false,
      ButtonDisabled: false,
      authorID: this.props.authorID,
    };
  }

  componentDidMount() {
    this._isMounted = true;
  }

  componentWillUnmount() {
    this._isMounted = false;
  }

  handleClickClose = () => {
    var n = this.props.actorID.indexOf("/author/");
    var length = this.props.actorID.length;
    let params = {
      actor: this.props.actorID.substring(n + 8, length),
      object: this.props.authorID,
    };
    deleteRequest(params).then((response) => {
      if (response.status === 200) {
        message.success("Request Rejected.");
        //window.location.reload();
      } else {
        message.error("Reject Failed!");
      }
    });
    this.setState((prevState) => {
      return {
        isRejected: true,
        ButtonDisabled: true,
      };
    });
  };

  handleClickAccept = () => {
    var n = this.props.actorID.indexOf("/author/");
    var length = this.props.actorID.length;
    let params = {
      actor: this.props.actorID.substring(n + 8, length),
      object: this.props.authorID,
    };
    createFollower(params).then((response) => {
      if (response.status === 204) {
        message.success("Request Accepted!");
        //window.location.reload();
      } else {
        message.error("Accept Failed!");
      }
    });
    deleteRequest(params).then((response) => {
      if (response.status === 200) {
        message.success("Request Deleted.");
        //window.location.reload();
      } else {
        message.error("Delete Failed!");
      }
    });
    this.setState((prevState) => {
      return {
        isAccepted: true,
        ButtonDisabled: true,
      };
    });
  };

  render() {
    const { isRejected, isAccepted, ButtonDisabled } = this.state;
    return (
      <div>
        <span style={{ float: "right" }}>
          <Button
            disabled={ButtonDisabled}
            icon={<CheckCircleOutlined style={{ color: "#70B668" }} />}
            onClick={this.handleClickAccept}
          ></Button>
          <Button
            style={{ marginLeft: "16px" }}
            disabled={ButtonDisabled}
            icon={<CloseCircleOutlined style={{ color: "#eb2f96" }} />}
            onClick={this.handleClickClose}
          ></Button>
        </span>
        <Tag visible={isRejected}>Request rejected.</Tag>
        <Tag visible={isAccepted}>Request accepted.</Tag>
      </div>
    );
  }
}
