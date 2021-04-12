import React, { useState } from "react";
import { Link } from "react-router";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { postRegister } from "../actions/users";
import _ from "lodash";
import { useHistory } from "react-router-dom";
import { POST_REGISTER } from "../actions/types";

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

function Signup(props) {
    const classes = useStyles();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [passwordCheck, setPasswordCheck] = useState("");
    const [displayName, setDisplayName] = useState("");
    const [github, setGithub] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    const history = useHistory();

    const onTextChange = (e) => {
        switch (e.target.name) {
            case "username":
                setUsername(e.target.value);
                break;
            case "password":
                setPassword(e.target.value);
            break;
            case "passwordCheck":
                setPasswordCheck(e.target.value);
                break;
            case "displayName":
                setDisplayName(e.target.value);
                break;
            case "github":
                setGithub(e.target.value);
                break;
            default:
                break;
        }
    };

    const registerClicked = () => {
        if (password.localeCompare(passwordCheck) !== 0) {
            setErrorMessage("Passwords do not match");
            return;
        }
        const user = { username, password, displayName, github };
        props.postRegister(user);
    };

    React.useEffect(() => {
        if (props.error.status >= 200 && props.error.status <= 300 && props.error.origin === POST_REGISTER) {
            history.push("/login");
        }
    });

    return (
        <div className={classes.root}>
        <div className={classes.logo}></div>
        <h2 className={classes.title}>Sign up for a free account</h2>
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
                name="password"
                type="password"
                onChange={onTextChange}
            />
            <TextField
                id="standard-basic"
                label="Re-enter Password"
                name="passwordCheck"
                type="password"
                onChange={onTextChange}
            />
            <TextField
                id="standard-basic"
                label="Display Name"
                name="displayName"
                onChange={onTextChange}
            />
            <TextField
                id="standard-basic"
                label="Github"
                name="github"
                onChange={onTextChange}
            />
            <Button
                className={classes.register}
                variant="contained"
                color="secondary"
                onClick={registerClicked}
            >
                Register
            </Button>
            <div className={classes.error}>{errorMessage}</div>
            </div>
        </div>
        </div>
    );
}

const mapStateToProps = (state) => ({
  user: state.users.user,
  error: state.errors
});

export default connect(mapStateToProps, { postRegister })(Signup);
