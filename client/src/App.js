import React, { Component, Suspense } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Navbar from './components/navs/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import AboutMe from './pages/AboutMe';
import UploadImage from './pages/UploadImage';
import NotFound from './components/errors/NotFound';
import ErrorBoundary from './components/errors/ErrorBoundary';


class App extends Component {

  componentDidMount = async () => { }

  render() {
    return (
      <BrowserRouter>
        <ErrorBoundary>
          <Navbar />
          <Suspense fallback={<div style={{ margin: 10 }}>Loading ...</div>}>
            <Switch>
              <Route exact path="/" component={Home} />
              <Route exact path="/aboutme" component={AboutMe} />
              <Route exact path="/login" component={Login} />
              <Route exact path="/register" component={Register} />
              <Route exact path="/image" component={UploadImage} />
              <Route component={NotFound} />
            </Switch>
          </Suspense>
        </ErrorBoundary>
      </BrowserRouter>
    );
  }
}

export default App;
