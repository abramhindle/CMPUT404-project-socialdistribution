import React, { Component } from 'react';
import Navbar from './components/Navbar'


class App extends Component {
  render() {
    return (
      <div className="App">
        <Navbar />
        <h1 style={{ textAlign: "center", fontFamily: "sans-serif", padding: 20 }}>Home</h1>
      </div>
    );
  }
}

export default App;
