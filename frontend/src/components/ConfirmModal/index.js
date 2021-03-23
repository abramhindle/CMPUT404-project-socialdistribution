import React from "react";
import { Modal } from "antd";

export default class ConfirmModal extends React.Component {
  handleModalOk = () => {
    this.props.dosomething();
  };

  handleModalCancel = () => {
    this.props.handleConfirmModalVisiblility();
  };

  render() {
    return (
      <Modal
        title="Confirm"
        visible={this.props.visible}
        onOk={this.handleModalOk}
        onCancel={this.handleModalCancel}
      >
        <p>Are you sure to delete?</p>
      </Modal>
    );
  }
}
