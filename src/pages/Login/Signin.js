// Import the react JS packages
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { signInUser } from "../../reducer/userSlice";
import { signIn_api } from "../../api/user_api";
import { Alert, Snackbar } from "@mui/material";
import "./signin.css";

// Define the Login function.
export const SignIn = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");

  const handleClose = () => {
    setSnackbarOpen(false);
  };

  const success = (res) => {
    dispatch(signInUser(res));
    navigate("/");
  };

  const failed = (status) => {
    if (status === 403) {
      setSnackbarMessage(
        "The account has not been approved yet! Please wait for approval"
      );
    } else {
      setSnackbarMessage("Wrong username or password!");
    }
    setSnackbarOpen(true);
  };

  const submit = async (e) => {
    e.preventDefault();
    console.log("Loggin in with", username, password);
    signIn_api(username, password, success, failed);
  };

  return (
    <div>
      <div className="Auth-form-container Signin">
        <form className="Auth-form" onSubmit={submit}>
          <h1>Social Distribution</h1>
          <h3 className="Auth-form-title">Sign In</h3>
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

      <Snackbar
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
        open={snackbarOpen}
        onClose={handleClose}
      >
        <Alert onClose={handleClose} severity="error" sx={{ width: "100%" }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </div>
  );
};

export default SignIn;
