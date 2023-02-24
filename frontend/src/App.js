import "./App.css";

import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import PrivateRoute from "./utils/PrivateRoute";
import SignIn from "./Signin";
import Main from "./Main";

function App() {
  return (
    <div>
      <Router>
        <Routes>
          <Route
            path="/"
            element={
              <PrivateRoute>
                <Main />
              </PrivateRoute>
            }
          />
          <Route path="/login" element={<SignIn />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
