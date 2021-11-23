import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import Headers from "../components/Headers";
import Message from "../components/Message";
import { register } from "../actions/userActions";
import { useDispatch, useSelector } from "react-redux";
import jQuery from "jquery";
import "./SignUpPage.css";
import { LinkContainer } from "react-router-bootstrap";

function SignUpPage({ location, history }) {
  const [name, setName] = useState("");
  const [display, setDisplay] = useState("");
  const [github, setGithub] = useState("");
  const [password, setPassword] = useState("");
  const [cPwd, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");

  const dispatch = useDispatch();

  const userRegister = useSelector((state) => state.userRegister);
  const { error, userInfo } = userRegister;

  const submitHandler = (e) => {
    e.preventDefault();
    if (password != cPwd) {
      setMessage("Passwords do not match.");
    } else if (name == "" || display == "" || password == "") {
      setMessage("Please fill in all the require information.");
    } else {
      // remove extra message banner
      setMessage();
      dispatch(register(name, display, github, password, cPwd));
    }
  };

  return (
    <div>
      <Headers></Headers>
      {message && <Message variant="danger">{message}</Message>}
      {userInfo && <Message variant="success">{userInfo}</Message>}
      {error && <Message variant="danger">{error}</Message>}
      <Form onSubmit={submitHandler}>
        <div className="form-group">
          <label
            style={{ color: "orange", marginTop: "100px", marginLeft: "40%" }}
          >
            Username
          </label>
          <input
            style={{
              color: "orange",
              marginTop: "5px",
              marginLeft: "40%",
              width: "300px",
            }}
            type="text"
            className="form-control"
            placeholder="Enter username"
            onChange={(e) => setName(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label
            style={{ color: "orange", marginTop: "10px", marginLeft: "40%" }}
          >
            Display Name
          </label>
          <input
            style={{
              color: "orange",
              marginTop: "5px",
              marginLeft: "40%",
              width: "300px",
            }}
            type="text"
            className="form-control"
            placeholder="Enter display name"
            onChange={(e) => setDisplay(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label
            style={{ color: "orange", marginTop: "10px", marginLeft: "40%" }}
          >
            GitHub URL (Optional)
          </label>
          <input
            style={{
              color: "orange",
              marginTop: "5px",
              marginLeft: "40%",
              width: "300px",
            }}
            type="url"
            className="form-control"
            placeholder="Enter GitHub URL"
            onChange={(e) => setGithub(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label
            style={{ color: "orange", marginTop: "10px", marginLeft: "40%" }}
          >
            Password
          </label>
          <input
            style={{
              color: "orange",
              marginTop: "5px",
              marginLeft: "40%",
              width: "300px",
            }}
            type="password"
            className="form-control"
            placeholder="Enter password"
            onChange={(e) => setPassword(e.target.value)}
          />
          <Form.Text className="text-muted m-0">
            <li
              style={{
                marginTop: "5px",
                marginLeft: "40%",
                width: "300px",
              }}
            >
              Password needs to be alphanumeric.
            </li>

            <li
              style={{
                marginLeft: "40%",
                width: "300px",
              }}
            >
              Password needs atleast 8 characters.
            </li>
            <li
              style={{
                marginLeft: "40%",
                width: "300px",
              }}
            >
              Password can't be too common.
            </li>
            <li
              style={{
                marginLeft: "40%",
                width: "300px",
              }}
            >
              Password can't be similar to your other info.
            </li>
          </Form.Text>
        </div>

        <div className="form-group">
          <label
            style={{ color: "orange", marginTop: "10px", marginLeft: "40%" }}
          >
            Confirm password
          </label>
          <input
            style={{
              color: "orange",
              marginTop: "5px",
              marginLeft: "40%",
              width: "300px",
            }}
            type="password"
            className="form-control"
            placeholder="Confirm password"
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </div>
        <Button
          style={{
            backgroundColor: "orange",
            marginTop: "15px",
            marginLeft: "43%",
          }}
          type="submit"
          className="btn btn-primary btn-block"
        >
          Submit
        </Button>

        <LinkContainer
          to="/login"
          style={{ marginTop: "15px", marginLeft: "60px" }}
        >
          <Button className="btn btn-primary btn-block">Login</Button>
        </LinkContainer>
      </Form>
    </div>
  );
}

export default SignUpPage;
