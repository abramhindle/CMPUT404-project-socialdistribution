import React from "react";
import { Button } from "antd";

export default class Profile extends React.Component {
  state = { authorID: "" };

  render() {
    return (
      <div style={{ margin: "10% 20%" }}>
        {/* logout */}
        <Button type="primary" danger onClick={this.props.logout}>
          Logout
        </Button>
      </div>
    );
  }
}
