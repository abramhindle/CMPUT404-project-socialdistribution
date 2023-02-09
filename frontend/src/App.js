import './App.css';
import React, {useState, useEffect} from 'react';

function App() {
    const [currentMsg, setCurrentMsg] = useState(0);

    useEffect(() => {
        fetch('/hello_world').then(res => res.json()).then(data => {
            setCurrentMsg(data.message);
        });
    }, []);

    return (
        <div className="App">
            <header className="App-header">
                <p>The current msg is {currentMsg}.</p>
            </header>
        </div>
    );
}

export default App;
