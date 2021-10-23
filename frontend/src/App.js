import { BrowserRouter as Router, Route } from "react-router-dom";

import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import SignUpPage from "./pages/SignUpPage";
import PostPage from "./pages/PostPage";

function App() {
  return (
    <Router>
      <Route path="/" component={HomePage} exact />
      <Route path="/login" component={LoginPage} exact />
      <Route path="/signup" component={SignUpPage} exact />
      <Route path="/post" component={PostPage} exact />
    </Router>
  );
}

export default App;
