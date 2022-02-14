import './App.css';
import RegistrationForm from './pages/Registration/Registration';
import HomePage from './pages/Feed/HomePage';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import BaseTemplate from './pages/BaseTemplate';
import LoginPage from './pages/Login/Login';


function App() {
  return  (
    <BrowserRouter>
      <Routes>
          <Route path="/" element={<BaseTemplate />} >
          <Route path="homepage" element={<HomePage />} />
          <Route path="login" element={<LoginPage />} />
          <Route path="register" element={<RegistrationForm />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App;
