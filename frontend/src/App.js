import './App.css';
import {
  BrowserRouter as Router, Route, Routes,
}
  from 'react-router-dom';
import Login from './components/auth/Login';
import Signup from './components/auth/Signup';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/login" element={(<Login />)} />
          <Route path="/signup" element={(<Signup />)} />
        </Routes>
      </Router>

    </div>
  );
}

export default App;
