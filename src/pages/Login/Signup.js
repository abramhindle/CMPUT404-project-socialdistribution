// Import the react JS packages
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signUp_api } from "../../api/user_api";

// Define the Login function.
export const SignUp = () => {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [profileImage, setProfileImage] = useState("");
  const [github, setGithub] = useState("");

  // Create the submit method.

  const success = () => {
    alert("Success! Sign Up Requested! Wait for Approval");
    navigate("/");
  };

  const submit = async (e) => {
    e.preventDefault();
    if (password === confirmPassword) {
      console.log("Sign Up with", username, password);
      signUp_api(
        username,
        password,
        displayName,
        profileImage,
        github,
        success
      );
    } else {
      alert("Password does not match!");
      setPassword("");
      setConfirmPassword("");
    }
  };

  return (
    <div className="Auth-form-container">
      <form className="Auth-form" onSubmit={submit}>
        <div className="Auth-form-content">
          <h3 className="Auth-form-title">Sign Up</h3>
          <div className="form-group mt-3">
            <label>Username</label>
            <input
              className="form-control mt-1"
              placeholder="Enter Username"
              name="username"
              type="text"
              value={username}
              required
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="form-group mt-3">
            <label>Password</label>
            <input
              name="password"
              type="password"
              className="form-control mt-1"
              placeholder="Enter password"
              value={password}
              required
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <div className="form-group mt-3">
            <label>Confirm Password</label>
            <input
              name="password"
              type="password"
              className="form-control mt-1"
              placeholder="Confirm password"
              value={confirmPassword}
              required
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
          </div>
          <div className="form-group mt-3">
            <label>DisplayName</label>
            <input
              className="form-control mt-1"
              placeholder="Enter DisplayName"
              name="displayName"
              type="text"
              value={displayName}
              required
              onChange={(e) => setDisplayName(e.target.value)}
            />
          </div>
          <div className="form-group mt-3">
            <label>ProfileImage</label>
            <input
              className="form-control mt-1"
              placeholder="Enter ProfileImage URL"
              name="profileImage"
              type="url"
              value={profileImage}
              required
              onChange={(e) => setProfileImage(e.target.value)}
            />
          </div>
          <div className="form-group mt-3">
            <label>Github</label>
            <input
              className="form-control mt-1"
              placeholder="Enter Github URL"
              name="github"
              type="url"
              value={github}
              required
              onChange={(e) => setGithub(e.target.value)}
            />
          </div>
          <div className="d-grid gap-2 mt-3">
            <button type="submit" className="btn btn-primary">
              Submit
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default SignUp;
