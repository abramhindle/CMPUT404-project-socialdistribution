import React, { Component } from "react";
import { Button } from "@material-ui/core";
import { connect } from "react-redux";
import "../../styles/postForm.css";

class PostForm extends Component {
  state = {
    show: false,
    title: "Post title",
    source: "",
    origin: "",
    description: "Post description",
    contentType: "text/plain",
    content: "Post content",
    visibility: "PUBLIC",
    unlisted: false,
  }

  componentDidMount = () => {
    // console.log("authorID in PostForm (componentDidMount): ", this.props.authorID);
  }

  handleShow = () => {
    const { show } = this.state;
    this.setState({ show: !show });
  }

  render() {
    const { show } = this.state;

    return (
      <div id="post-form">
        {
          this.props.authorID !== null ?
            <div id="form-control">
              <Button
                id="show-btn"
                variant="outlined"
                color="primary"
                onClick={this.handleShow}
              >
                {show ? "Cancel" : "Make Post"}
              </Button>
              <hr />
              {
                show ? <h3>Show</h3> : null
              }
            </div>
            :
            null
        }
      </div>
    )
  }
}

const mapStateToProps = (state) => ({
  authorID: state.user.authorID
})

export default connect(mapStateToProps)(PostForm);