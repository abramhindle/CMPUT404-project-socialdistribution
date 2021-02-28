import React, { Component } from "react";
import NoUserHeader from "../components/headers/NoUserHeader";
import UserHeader from "../components/headers/UserHeader";
import { connect } from "react-redux";
import axios from "axios";
// import PostForm from "../components/posts/PostForm";
// import ReactMarkDown from "react-markdown";

class Home extends Component {

  state = {
    currentUser: null,
  }

  componentDidMount = async () => {
    const { authorID } = this.props;
    if (authorID) {
      const doc = await axios.get(`service/author/${authorID.authorID}`)
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

    return (
      <div>
        {this.renderHeader()}
        <h1 id="home-title" style={{ textAlign: "center", fontFamily: "sans-serif", padding: 15 }}>Home</h1>
        {/* <PostForm /> */}
        {/* <ReactMarkDown children="*hello*" /> */}
        {/* <ReactMarkDown># Hello, *world*!</ReactMarkdown> */}
      </div>
    )
  }
}

const mapStateToProps = (state) => ({
  authorID: state.user.authorID
})

export default connect(mapStateToProps)(Home);