import React, { Component } from "react";
import { Button } from "@material-ui/core";
import { connect } from "react-redux";

class PostForm extends Component {
  state = {
    show: false,
    title: "",
    source: "",
    origin: "",
    description: "",
    contentType: "",
    content: "",
    visibility: "",
    unlisted: "",
  }

  componentDidMount = () => {
    console.log("authorID in PostForm: ", this.props.authorID.authorID);
  }

  handleShow = () => {
    const { show } = this.state;
    this.setState({ show: !show });
  }

  render() {
    const { show } = this.state;

    return (
      <div>
        <Button
          variant="outlined"
          color="primary"
          onClick={this.handleShow}
        >
          {show ? "Cancel" : "Make Post"}
        </Button>
        {
          show ? <h3>Show</h3> : <h3>Close</h3>
        }
      </div>
    )
  }
}

const mapStateToProps = (state) => ({
  authorID: state.user.authorID
})

export default connect(mapStateToProps)(PostForm);