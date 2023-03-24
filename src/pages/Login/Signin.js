// Import the react JS packages
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { signInUser } from "../../reducer/userSlice";
import { signIn_api } from "../../api/user_api";
import "./signin.css";

// Define the Login function.
export const SignIn = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  // Create the submit method.

  const success = (res) => {
    dispatch(signInUser(res));
    navigate("/");
  };

  const submit = async (e) => {
    e.preventDefault();
    console.log("Loggin in with", username, password);
    signIn_api(username, password, success);
  };

  return (
    <div className="Auth-form-container">
      <form className="Auth-form" onSubmit={submit}>
        <h1 className="Auth-form-title">Sign In</h1>
        <div className="form-group mt-3">
          <input
            className="form-control mt-1"
            placeholder="Username"
            name="username"
            type="text"
            value={username}
            required
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="form-group mt-3">
          <input
            name="password"
            type="password"
            className="form-control mt-1"
            placeholder="Password"
            value={password}
            required
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div className="d-grid gap-2 mt-3">
          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </div>
        Don't have a account? &nbsp;
        <Link to="/signup">Sign Up Here!</Link>
      </form>
    </div>
  );
};

export default SignIn;
