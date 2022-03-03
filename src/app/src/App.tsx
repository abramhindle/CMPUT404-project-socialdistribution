import React, { useState } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Author from "./api/models/Author";
import Homepage from "./pages/Homepage";
import Mainpage from "./pages/Mainpage";
import Profile from "./pages/Profile";
import ErrorPage from "./pages/Error";

function App() {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [currentUser, setCurrentUser] = useState<Author | undefined>(undefined);

  return (
    <BrowserRouter>
      <Routes>
        <Route
          index
          element={
            currentUser ? <Mainpage currentUser={currentUser} /> : <Homepage />
          }
        />
        <Route
          path="/profile/:id"
          element={<Profile currentUser={currentUser} />}
        />
        <Route path="*" element={<ErrorPage errorType="NotFound" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
