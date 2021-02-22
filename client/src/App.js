import React, { Component } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import AboutMe from './pages/AboutMe';
import UploadImage from './pages/UploadImage';


class App extends Component {

  componentDidMount = async () => { }

  render() {
    return (
      <BrowserRouter>
        <Navbar />
        <Switch>
          <Route exact path="/" component={Home} />
          <Route exact path="/aboutme" component={AboutMe} />
          <Route exact path="/login" component={Login} />
          <Route exact path="/register" component={Register} />
          <Route exact path="/image" component={UploadImage} />
        </Switch>
      </BrowserRouter>
    );
  }
}

export default App;
