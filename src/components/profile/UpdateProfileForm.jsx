import React, { Component } from "react";
import { connect } from "react-redux";
import { Button, TextField } from "@material-ui/core";
import "../../styles/updateProfile.css";
import axios from "axios";

class UpdateProfileForm extends Component {
  state = {
    show: false,
    email: "",
    password: "",
    displayName: "",
    github: "",
  }

  componentDidMount = () => {
    console.log("authorID in UpdateProfileForm: ", this.props.authorID);
  }

  handleUpdate = async () => {
    const { email, password, displayName, github } = this.state;
    const { authorID } = this.props;
    console.log(authorID.authorID);
    if (email || password || displayName || github) {
      try {
        // can update any field
        let data = {}
        if (email) {
          data.email = email;
        }
        if (password) {
          data.password = password;
        }
        if (displayName) {
          data.displayName = displayName;
        }
        if (github) {
          data.github = github;
        }
        await axios.post(`service/author/${authorID.authorID}/`, data);

        console.log(email, password, displayName, github);
        this.handleShow();
        window.location = "/aboutme"
      } catch (err) {
        console.log(err.message);
      }
    } else {
      alert("Nothing to change");
    }
  }

  handleShow = () => {
    const { show } = this.state;
    this.setState({ show: !show });
  }

  render() {
    const { show, email, password, displayName, github } = this.state;
    const { authorID } = this.props;
    return (
      <div id="update-form-root">
        {
          authorID !== null ?
            <div>
              <Button
                className="btn"
                color="primary"
                variant="outlined"
                onClick={this.handleShow}
              >
                {show ? "Cancel" : "Update Profile"}
              </Button>
              {show ?
                <div id="form-update">
                  <TextField
                    style={{ width: 350, marginLeft: 10 }}
                    type="email"
                    id="update-email"
                    label="Your new email"
                    value={email}
                    onChange={(e) => this.setState({ email: e.target.value })}
                  />
                  <br />
                  <TextField
                    style={{ width: 350, marginLeft: 10 }}
                    id="update-password"
                    label="Your new Password"
                    value={password}
                    onChange={(e) => this.setState({ password: e.target.value })}
                  />
                  <br />
                  <TextField
                    style={{ width: 350, marginLeft: 10 }}
                    id="update-diplayname"
                    label="Your new display name"
                    value={displayName}
                    onChange={(e) => this.setState({ displayName: e.target.value })}
                  />
                  <br />
                  <TextField
                    style={{ width: 350, marginLeft: 10 }}
                    id="update-github"
                    label="Your new Github"
                    value={github}
                    onChange={(e) => this.setState({ github: e.target.value })}
                  />
                  <br />
                  <Button
                    id="update-btn"
                    color="primary"
                    variant="outlined"
                    onClick={this.handleUpdate}
                  >
                    Confirm
                  </Button>
                </div> : null
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

export default connect(mapStateToProps)(UpdateProfileForm);