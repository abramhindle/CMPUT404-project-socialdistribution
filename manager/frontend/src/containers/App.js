import React from 'react';
import ReactDOM from 'react-dom';

import Navbar from '../components/Navbar/Navbar';

export default function App() {
    return (
        <div 
            className="app"
            style={{ backgroundColor: "#EFEFEF" }}
        >

            <Navbar />
        </div>
    )
}

ReactDOM.render(<App />, document.getElementById('root'));