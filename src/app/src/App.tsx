import React, { useEffect, useState } from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Author from './api/models/Author';
import Homepage from './pages/Homepage';
import Mainpage from './pages/Mainpage';
import Profile from './pages/Profile';
import Admin from './pages/Admin';
import ErrorPage from './pages/Error';
import api from './api/api';

function App() {
  const [currentUser, setCurrentUser] = useState<Author | undefined>(undefined);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      api.authors
        .getCurrent()
        .then((author) => setCurrentUser(author))
        .catch((error) => {
          localStorage.removeItem('token');
        });
    }
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route
          index
          element={
            currentUser ? (
              <Mainpage currentUser={currentUser} />
            ) : (
              <Homepage setCurrentUser={setCurrentUser} />
            )
          }
        />
        <Route path="/profile/:id" element={<Profile currentUser={currentUser} />} />
        <Route path="*" element={<ErrorPage errorType="NotFound" />} />
        <Route path="/admin" element={<Admin />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
