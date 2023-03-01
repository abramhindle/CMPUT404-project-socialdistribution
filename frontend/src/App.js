import './App.css';
import {
  BrowserRouter as Router, Route, Routes,
}
  from 'react-router-dom';
import Login from './components/auth/Login';
import Signup from './components/auth/Signup';
import Inbox from './components/inbox/Inbox';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/login" element={(<Login />)} />
          <Route path="/signup" element={(<Signup />)} />
          <Route path="/inbox" element={(<Inbox />)} />
        </Routes>
      </Router>

    </div>
  );
}

export default App;
