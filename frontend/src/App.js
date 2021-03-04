import React from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";
import LoginComp from "./components/LoginComp";
import "./App.css";
import TopNav from "./components/TopNav";
import Post from "./components/Post";

export default class App extends React.Component {

  state = {
    authorID: "",
  }
  
  saveAuthorIDHome = (id) => {
    this.setState({authorID: id})
    console.log('app', id)
  }

  Home = () => {
    return (
      <div
        style={{
          textAlign: "center",
        }}
      >
        <h1>Welcome To Social Distribution!</h1>
        <LoginComp saveAuthorIDHome={this.saveAuthorIDHome} />
      </div>
    );
  };

  render() {
    return (
      <Router>
        {/* add route */}
        <Route exact path="/" component={this.Home} />
        <Route
          path="/home"
          render={(props) => (
            <div>
              <TopNav authorID={this.state.authorID} {...this.props} {...props}/>
              <Post {...this.props} {...props}/>
            </div>
          )}
        />
      </Router>
    );
  }
}
