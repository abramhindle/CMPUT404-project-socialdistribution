import React from "react"
import './App.css';
import 'antd/dist/antd.css';

import { BrowserRouter as Router} from 'react-router-dom';
import BaseRouter from './routes';

class App extends React.Component {
    constructor(props) {
         super();
    }
    /*Define Functions*/
    render() {
        return (
            <div className="App">
                <Router>
                   <BaseRouter/> 
                </Router>
            </div>
        );
    }
}

export default App;
