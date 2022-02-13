import './App.css';
import RegistrationForm from './pages/Login/Registration';
import HomePage from './pages/Feed/HomePage';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import BaseTemplate from './pages/BaseTemplate';


function App() {
  return  (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<BaseTemplate />} >
          <Route path="" element={<HomePage />} />
          <Route path="login" element={<RegistrationForm />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App;
