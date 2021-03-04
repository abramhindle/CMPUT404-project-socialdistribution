import React, { Component } from "react";
import NoUserHeader from "../components/headers/NoUserHeader";
import UserHeader from "../components/headers/UserHeader";
import { connect } from "react-redux";
import axios from "axios";

class Home extends Component {

  state = {
    currentUser: null,
  }

  componentDidMount = async () => {
    const { authorID } = this.props;
    console.log("authorID in Home (componentDidMount):", authorID);
    if (authorID) {
      const doc = await axios.get(`service/author/${authorID.authorID}/`)
      this.setState({ currentUser: doc.data })
    }
  }

  renderHeader = () => {
    const { currentUser } = this.state;
    switch (currentUser) {

      case null:
        return <NoUserHeader />

      default:
        return <UserHeader currentUser={currentUser} />

    }
  }

  render() {
    const { authorID } = this.props;
    return (
      <div>
        {this.renderHeader()}
        {
          authorID !== null ?
            <h1
              id="home-title-login"
              style={{
                textAlign: "center",
                fontFamily: "sans-serif",
                padding: 15
              }}
            >
              Home
          </h1>
            :
            <h1
              id="home-title-logout"
              style={{
                textAlign: "center",
                fontFamily: "sans-serif",
                padding: 15
              }}
            >
              Please Login
          </h1>
        }

      </div>
    )
  }
}

const mapStateToProps = (state) => ({
  authorID: state.user.authorID
})

export default connect(mapStateToProps)(Home);