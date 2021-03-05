import React, { useState } from "react";
import { Link } from "react-router";
import { connect } from "react-redux";
import { useHistory } from "react-router-dom";

import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";

import { postLogin } from "../actions/users";

const useStyles = makeStyles(() => ({
  root: {},
  logo: {
    height: "150px",
    width: "150px",
    backgroundColor: "#D1305E",
    borderRadius: "10px",
    margin: "40px auto",
  },
  title: {
    textAlign: "center",
  },
  text: {
    display: "flex",
    alignContent: "center",
    justifyContent: "center",
  },
  textField: {
    display: "flex",
    flexDirection: "column",
    width: "30em",
  },
  passwordRecover: {
    float: "right",
  },
  links: {
    margin: "1em 0",
  },
  register: {
    width: "10em",
    margin: "2em auto",
    backgroundColor: "#D1305E",
    fontWeight: "300",
    fontSize: "0.8em",
    textTransform: "none",
  },
  error: {
    textAlign: "center",
    color: "#D1305E",
  },
}));

function Login(props) {
  const classes = useStyles();

  const history = useHistory();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const onTextChange = (e) => {
    switch (e.target.name) {
      case "username":
        setUsername(e.target.value);
        break;
      case "password":
        setPassword(e.target.value);
        break;
      default:
        break;
    }
  };

  const registerClicked = () => {
    const user = { username, password };
    props.postLogin(user);
  };

  React.useEffect(() => {
    if (!_.isEmpty(props.token)) {
      history.push("/feed");
    }
    if (props.error.status === 400) {
      setErrorMessage(props.error.msg.non_field_errors[0]);
    }
  });

  return (
    <div className={classes.root}>
      <div className={classes.logo}></div>
      <h2 className={classes.title}>Welcome Back</h2>
      <div className={classes.text}>
        <div className={classes.textField}>
          <TextField
            id="standard-basic"
            label="Username"
            name="username"
            onChange={onTextChange}
          />
          <TextField
            id="standard-basic"
            label="Password"
            type="password"
            name="password"
            onChange={onTextChange}
          />
          <div className={classes.links}>
            <a href="/signup">Sign Up</a>
            <a href="/" className={[classes.passwordRecover, "test"].join(" ")}>
              Forgot your password?
            </a>
          </div>
          <Button
            className={classes.register}
            variant="contained"
            color="secondary"
            onClick={registerClicked}
          >
            Login
          </Button>
          <div className={classes.error}>{errorMessage}</div>
        </div>
      </div>
    </div>
  );
}

const mapStateToProps = (state) => ({
  token: state.users.token,
  error: state.errors,
});

export default connect(mapStateToProps, { postLogin })(Login);
