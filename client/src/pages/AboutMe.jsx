import React, { Component } from 'react';
import { connect } from 'react-redux';
import axios from 'axios';
import UserHeader from '../components/headers/UserHeader';

class AboutMe extends Component {

  constructor(props) {
    super(props);
    this.state = {
      currentUser: null,
    }
  }

  componentDidMount = async () => {
    const { authorID } = this.props;
    if (authorID) {
      const doc = await axios.get(`service/author/${authorID.authorID}`);
      this.setState({ currentUser: doc.data })
    }
  }

  render() {
    const { currentUser } = this.state;
    return (
      <div>
        {
          currentUser !== null ? <UserHeader currentUser={currentUser} /> : null
        }
        <h1 id="aboutme-title" style={{ textAlign: "center", fontFamily: "sans-serif", padding: 15 }}>About Me</h1>
      </div>
    )
  }
}

const mapStateToProps = (state) => ({
  authorID: state.user.authorID
})

export default connect(mapStateToProps)(AboutMe);