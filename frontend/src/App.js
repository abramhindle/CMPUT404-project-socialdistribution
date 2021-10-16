import { BrowserRouter as Router, Route } from "react-router-dom";

import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
function App() {
  return (
    <Router>
      <Route path="/" component={HomePage} exact />
      <Route path="/login" component={LoginPage} exact />
    </Router>
  );
}

export default App;
