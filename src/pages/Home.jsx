import React, { Component } from "react";
import NoUserHeader from "../components/headers/NoUserHeader";
import ObjectCard from '../components/inbox/ObjectCard';
import { connect } from "react-redux";
import axios from "axios";

class Home extends Component {

  state = {
    currentUser: null,
    inbox: []
  }

  componentDidMount = async () => {
    const { authorID } = this.props.authorID;
    if (authorID) {
      const res = await axios.get(`service/author/${authorID}/`)
      this.setState({ currentUser: res.data })
      this.getInbox();
      setInterval(this.getInbox, 1000);
    }
  }

  renderHeader = () => {
    const { currentUser } = this.state;
    if (currentUser === null) {
      return <NoUserHeader />
    } else {
      this.getInbox();
    }
  }

  getInbox = async () => {
    try {
      const { authorID } = this.props.authorID;
      const res = await axios.get(`service/author/${authorID}/inbox/`);
      this.setState({ inbox: res.data.items });
    } catch (e) {
      console.log(e);
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
        <div>
          {
            this.state.inbox.length !== 0 ?
              this.state.inbox.map((item, index) => {
                return <ObjectCard key={index} item={item} />
              })
              :
              null
          }
        </div>
      </div>
    )
  }
}

const mapStateToProps = (state) => ({
  authorID: state.user.authorID
})

export default connect(mapStateToProps)(Home);