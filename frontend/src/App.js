import React from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";

export default class App extends React.Component {
  Home = () => {
    return (
      <div>
        replace with components, such as top navigate bar, homepage, etc.
      </div>
    );
  };

  render() {
    return (
      <Router>
        {/* add route */}
        <Route exact path="/" component={this.Home} />
        <Route path="/author/:id" render={(props) => <div></div>} />
      </Router>
    );
  }
}
