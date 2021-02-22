import React, { Component } from 'react';
import { connect } from 'react-redux';

class AboutMe extends Component {

  constructor(props) {
    super(props);
    this.state = {

    }
  }

  componentDidMount = () => {
    console.log("currentUser:", this.props.currentUser);
  }

  render() {
    return (
      <div>
        <h1 id="aboutme-title" style={{ textAlign: "center", fontFamily: "sans-serif", padding: 15 }}>About Me</h1>
      </div>
    )
  }
}

const mapStateToProps = (state) => ({
  currentUser: state.user.currentUser
})

export default connect(mapStateToProps)(AboutMe);