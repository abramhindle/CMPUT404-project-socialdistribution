import React, { Component } from "react";
import NoUserHeader from "../components/headers/NoUserHeader";
import UserHeader from "../components/headers/UserHeader";
import { connect } from "react-redux";
import axios from "axios";
// import ReactMarkdown from "react-markdown";

class Home extends Component {

  state = {
    userProfile: null,
  }

  componentDidMount = async () => {
    const { authorID } = this.props;
    if (authorID) {
      const doc = await axios.get(`service/author/${authorID.authorID}`)
      this.setState({ userProfile: doc.data })
    }

  }

  renderHeader = () => {
    const { userProfile } = this.state;
    switch (userProfile) {

      case null:
        return <NoUserHeader />

      default:
        return <UserHeader userProfile={userProfile} />

    }
  }

  render() {
    return (
      <div>
        {this.renderHeader()}
        <h1 id="home-title" style={{ textAlign: "center", fontFamily: "sans-serif", padding: 15 }}>Home</h1>
        {/* <ReactMarkdown children="*hello*" /> */}
        {/* <ReactMarkdown># Hello, *world*!</ReactMarkdown> */}
      </div>
    )
  }
}

const mapStateToProps = (state) => ({
  authorID: state.user.authorID
})

export default connect(mapStateToProps)(Home);