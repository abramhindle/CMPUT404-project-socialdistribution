import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Button, Form } from "react-bootstrap";
import Headers from "../components/Headers";
import Message from "../components/Message";
import { login } from "../actions/userActions";
import { useDispatch, useSelector } from "react-redux";

function LoginPage({ location, history }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const dispatch = useDispatch();

  const redirect = location.search ? location.search.split("=")[1] : "/";

  const userLogin = useSelector((state) => state.userLogin);
  const { error, loading, userInfo } = userLogin;

  useEffect(() => {
    if (userInfo) {
      history.push(redirect);
    }
  }, [history, userInfo, redirect]);

  const submitHandler = (e) => {
    e.preventDefault();
    if (username == "" || password == "") {
      setMessage("Please fill in the username/ password.");
    } else {
      setMessage();
      dispatch(login(username, password));
    }
  };
  return (
    <div>
      <Headers />
      <Form onSubmit={submitHandler}>
        {message && <Message variant="danger">{message}</Message>}
        {error && <Message variant="danger">{error}</Message>}
        <Form.Group>
          <Form.Label
            style={{ color: "orange", marginTop: "100px", marginLeft: "40%" }}
          >
            Username
          </Form.Label>
          <Form.Control
            style={{
              color: "orange",
              marginTop: "5px",
              marginLeft: "40%",
              width: "300px",
            }}
            type="text"
            className="form-control"
            placeholder="Enter username"
            onChange={(e) => setUsername(e.target.value)}
          />
        </Form.Group>

        <Form.Group>
          <Form.Label
            style={{ color: "orange", marginTop: "10px", marginLeft: "40%" }}
          >
            Password
          </Form.Label>
          <Form.Control
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
        </Form.Group>

        <Button
          style={{
            backgroundColor: "orange",
            marginTop: "15px",
            marginLeft: "43%",
          }}
          type="submit"
          className="btn btn-primary btn-block"
        >
          Login
        </Button>

        <Link to="/signup">
          <Button
            style={{
              marginTop: "15px",
              marginLeft: "70px",
            }}
            className="btn btn-primary btn-block"
          >
            Signup
          </Button>
        </Link>
      </Form>
    </div>
  );
}

export default LoginPage;
