import React from "react"
import logo from './logo.svg';
import './App.css';

import axios from "axios";

class App extends React.Component {
    constructor(props) {
         super();
    }
    /*Define Functions*/
    

    render() {
        return (
            <div className="App">
              <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
                <p>
                  Welcome to Social Distribution 
                </p>
                <a
                  className="App-link"
                  href="https://reactjs.org"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Learn React
                </a>
              </header>
            </div>
        );
    }
}

export default App;
