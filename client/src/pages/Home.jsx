import React, { Component } from "react";
import NoUserHeader from "../components/headers/NoUserHeader";
import UserHeader from "../components/headers/UserHeader";
import { connect } from "react-redux";
import axios from "axios";
// import axios from "axios";

class Home extends Component {

  state = {
    userProfile: null,
  }

  componentDidMount = async () => {
    const { currentUser } = this.props;
    if (currentUser) {
      const doc = await axios.get(`service/author/${currentUser.authorID}`)
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
      </div>
    )
  }
}

const mapStateToProps = (state) => ({
  currentUser: state.user.currentUser
})

export default connect(mapStateToProps)(Home);